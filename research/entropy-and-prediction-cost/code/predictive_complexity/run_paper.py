from __future__ import annotations
import argparse
from collections import defaultdict
import hashlib
import math
from pathlib import Path
import platform
import time
import numpy as np
from .estimation import collision_estimate, coverage_power, entropy_from_power, expected_majority_power, moment_variance, table_statistics
from .io import write_csv, write_json
from .stationary import fit_sparse_walsh, fwht, make_feedback, population_guessing_power, renyi_entropy
FAMILIES = ('copy', 'parity', 'lookup')

def rng_for(seed: int, *coordinates: int) -> np.random.Generator:
    return np.random.default_rng(np.random.SeedSequence([seed, *coordinates]))

def summarize(rows: list[dict], group_keys: tuple[str, ...], values: tuple[str, ...]) -> list[dict]:
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for row in rows:
        groups[tuple((row[k] for k in group_keys))].append(row)
    summary = []
    for key, group in sorted(groups.items()):
        record = dict(zip(group_keys, key))
        record['trials'] = len(group)
        for value in values:
            samples = np.array([row[value] for row in group], dtype=float)
            record[value + '_mean'] = float(samples.mean())
            record[value + '_sd'] = float(samples.std(ddof=1)) if len(group) > 1 else 0.0
            record[value + '_sem'] = record[value + '_sd'] / math.sqrt(len(group))
        summary.append(record)
    return summary

def spectra(out: Path, delta: float, seed: int) -> dict:
    rows = []
    p = 5
    arrays = {}
    error = 0.0
    for family_id, family in enumerate(FAMILIES):
        source = make_feedback(p, family, delta, rng_for(seed, 1, family_id))
        arrays[family + '_g'] = source.g
        arrays[family + '_probabilities'] = source.block_probabilities(2 * p)
        for n in range(1, 17):
            probabilities = source.block_probabilities(n)
            for alpha in (1.0, 2.0, math.inf):
                observed = renyi_entropy(probabilities, alpha)
                h = renyi_entropy(np.array([delta, 1 - delta]), alpha)
                expected = min(n, p) + max(0, n - p) * h
                error = max(error, abs(observed - expected))
                rows.append(dict(family=family, p=p, n=n, alpha=str(alpha), entropy=observed, formula=expected))
    np.savez_compressed(out / 'spectra.npz', **arrays)
    write_csv(out / 'spectra.csv', rows)
    return {'p': p, 'maximum_absolute_entropy_error': error}

def capacity(out: Path, p: int, delta: float, trials: int, train_n: int, seed: int) -> dict:
    rows = []
    m = 1 << p - 1
    budgets = sorted(set([1 << k for k in range(p)] + [3 * (1 << k) for k in range(p - 2)]))
    for trial in range(trials):
        for family_id, family in enumerate(FAMILIES):
            source = make_feedback(p, family, delta, rng_for(seed, 2, trial, family_id, 0))
            contexts, labels = source.sample(train_n, rng_for(seed, 2, trial, family_id, 1))
            test_c, _ = source.sample(32768, rng_for(seed, 2, trial, family_id, 2))
            exact_spectrum = fwht(1 - 2 * source.g.astype(np.int64))
            exact_order = np.argsort(-np.abs(exact_spectrum), kind='stable')
            for terms in budgets:
                learned = fit_sparse_walsh(contexts, labels, p, terms)
                power = population_guessing_power(source, learned)
                sparse = np.zeros(m, dtype=np.int64)
                sparse[exact_order[:terms]] = exact_spectrum[exact_order[:terms]]
                known_power = population_guessing_power(source, (fwht(sparse) < 0).astype(np.int8))
                test_agreement = np.mean(learned[test_c & m - 1] == source.g[test_c & m - 1])
                test_power = delta + (1 - 2 * delta) * float(test_agreement)
                rows.append(dict(trial=trial, family=family, p=p, delta=delta, train_n=train_n, terms=terms, guessing_power=power, entropy=entropy_from_power(power), recovered_advantage=(power - 0.5) / (0.5 - delta), independent_trajectory_power=test_power, known_rule_power=known_power))
        if (trial + 1) % 10 == 0 or trial == trials - 1:
            print(f'stationary trials: {trial + 1}/{trials}', flush=True)
    write_csv(out / 'capacity.csv', rows)
    summary = summarize(rows, ('family', 'terms'), ('guessing_power', 'entropy', 'recovered_advantage', 'independent_trajectory_power', 'known_rule_power'))
    write_csv(out / 'capacity_summary.csv', summary)
    discrepancies = [row['independent_trajectory_power'] - row['guessing_power'] for row in rows]
    return {'p': p, 'train_n': train_n, 'trials': trials, 'budgets': budgets, 'trajectory_minus_exact_mean': float(np.mean(discrepancies)), 'trajectory_minus_exact_rms': float(np.sqrt(np.mean(np.square(discrepancies))))}

def value_vs_prediction(out: Path, orders: list[int], delta: float, trials: int, seed: int) -> dict:
    rows = []
    theory = []
    ideal = entropy_from_power(1 - delta)
    for order in orders:
        m = 1 << order
        grid = sorted(set((int(round(2 ** x)) for x in np.arange(4, order + 3.01, 0.5))))
        max_n = max(grid)
        reference = {n: expected_majority_power(n, m, delta) for n in grid}
        for n in grid:
            theory.append(dict(m=m, n=n, majority_power=reference[n], coverage_power=coverage_power(n, m, delta), moment_variance=moment_variance(n, m, delta)))
        for trial in range(trials):
            rng = rng_for(seed, 3, order, trial)
            rule = rng.integers(0, 2, size=m, dtype=np.int8)
            contexts = rng.integers(m, size=max_n, dtype=np.int64)
            labels = rule[contexts] ^ (rng.random(max_n) < delta).astype(np.int8)
            for n in grid:
                c, y = (contexts[:n], labels[:n])
                estimate = collision_estimate(c, y, m)
                _, votes = table_statistics(c, y, m)
                learned = (votes < 0).astype(np.int8)
                power = delta + (1 - 2 * delta) * float(np.mean(learned == rule))
                error = estimate.entropy - ideal
                rows.append(dict(trial=trial, m=m, n=n, delta=delta, estimate=estimate.entropy, squared_error=error * error, raw_moment=estimate.raw_moment, pairs=estimate.context_pairs, lower=estimate.lower, upper=estimate.upper, interval_covers=int(estimate.lower <= ideal <= estimate.upper), prediction_power=power, prediction_entropy=entropy_from_power(power), recovered_advantage=(power - 0.5) / (0.5 - delta)))
        print(f'independent-context trials: M={m}, {trials} rules, {len(grid)} budgets', flush=True)
    write_csv(out / 'estimation.csv', rows)
    write_csv(out / 'estimation_theory.csv', theory)
    values = ('estimate', 'squared_error', 'raw_moment', 'pairs', 'interval_covers', 'prediction_power', 'prediction_entropy', 'recovered_advantage')
    summary = summarize(rows, ('m', 'n'), values)
    write_csv(out / 'estimation_summary.csv', summary)
    return {'orders': orders, 'trials': trials, 'noise_parameter_given_to_estimator': False}

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('paper/data'))
    parser.add_argument('--seed', type=int, default=20261005)
    parser.add_argument('--delta', type=float, default=0.1)
    parser.add_argument('--capacity-trials', type=int, default=30)
    parser.add_argument('--estimation-trials', type=int, default=200)
    parser.add_argument('--p', type=int, default=10)
    parser.add_argument('--train-n', type=int, default=8192)
    parser.add_argument('--orders', type=int, nargs='+', default=[8, 10, 12, 14, 16])
    args = parser.parse_args()
    if args.seed < 0 or not 0 < args.delta < 0.5 or args.p < 2 or (args.train_n < 1):
        parser.error('invalid seed, noise, memory, or training size')
    if min(args.capacity_trials, args.estimation_trials) < 2 or min(args.orders) < 2:
        parser.error('at least two trials and orders >= 2 are required')
    args.out.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    report = {'seed': args.seed, 'delta': args.delta, 'python': platform.python_version(), 'numpy': np.__version__, 'spectra': spectra(args.out, args.delta, args.seed), 'capacity': capacity(args.out, args.p, args.delta, args.capacity_trials, args.train_n, args.seed), 'estimation': value_vs_prediction(args.out, args.orders, args.delta, args.estimation_trials, args.seed)}
    report['elapsed_seconds'] = time.perf_counter() - started
    root = Path(__file__).parent
    report['code_sha256'] = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in ('stationary.py', 'estimation.py', 'run_paper.py')}
    write_json(args.out / 'config.json', report)
    print(f"Finished in {report['elapsed_seconds']:.1f} s; data in {args.out}", flush=True)
if __name__ == '__main__':
    main()
