from __future__ import annotations
import argparse
import math
import time
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Any
import numpy as np
from .io import write_csv, write_json
from .metrics import evaluate_predictions, ideal_min_entropy, min_entropy_from_guessing_power
from .plotting import plot_sample_scaling_curve, plot_sample_thresholds
from .progress import ProgressTimer, format_duration
from .scaling import fit_power_law
from .sources import lookup_indices, sample_noisy_lookup

def parse_int_list(values: list[int] | None, fallback: list[int]) -> list[int]:
    return fallback if values is None else values

def coverage_guessing_power(order: int, delta: float, n: int) -> float:
    coverage = 1.0 - (1.0 - 2.0 ** (-order)) ** n
    return 0.5 + (0.5 - delta) * coverage

def coverage_required_samples(order: int, delta: float, epsilon: float) -> int:
    target_h = ideal_min_entropy(delta) + epsilon
    target_p = 2.0 ** (-target_h)
    if target_p <= 0.5:
        return 0
    required_coverage = (target_p - 0.5) / (0.5 - delta)
    required_coverage = min(max(required_coverage, 0.0), 1.0)
    if required_coverage >= 1.0:
        return math.inf
    miss_probability = 1.0 - required_coverage
    unseen_probability = 1.0 - 2.0 ** (-order)
    return math.ceil(math.log(miss_probability) / math.log(unseen_probability))

def fit_lookup_majority(x: np.ndarray, y: np.ndarray, *, subset: tuple[int, ...], order: int) -> tuple[np.ndarray, np.ndarray, float]:
    table_size = 2 ** order
    idx = lookup_indices(x, subset)
    counts = np.bincount(idx, minlength=table_size)
    votes = np.bincount(idx, weights=y.astype(np.float64), minlength=table_size)
    table = np.ones(table_size, dtype=np.int8)
    table[votes < 0.0] = -1
    seen = counts > 0
    return (table, seen, float(np.mean(seen)))

def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[int(row['source_order_k']), int(row['train_samples'])].append(row)
    summary: list[dict[str, Any]] = []
    value_keys = ['raw_accuracy', 'p_ml', 'accessible_min_entropy', 'entropy_gap', 'coverage_fraction', 'oracle_coverage_guessing_power', 'oracle_coverage_min_entropy']
    for (order, train_samples), group in sorted(grouped.items()):
        first = group[0]
        item: dict[str, Any] = {'source_family': first['source_family'], 'source_order_k': order, 'table_size': first['table_size'], 'rule_complexity_proxy': first['rule_complexity_proxy'], 'model_family': first['model_family'], 'p': first['p'], 'delta': first['delta'], 'train_samples': train_samples, 'test_samples': first['test_samples'], 'seeds': len(group), 'ideal_min_entropy': first['ideal_min_entropy']}
        for key in value_keys:
            vals = [float(row[key]) for row in group]
            item[f'{key}_mean'] = mean(vals)
            item[f'{key}_std'] = stdev(vals) if len(vals) > 1 else 0.0
        summary.append(item)
    return summary

def collect_thresholds(summary: list[dict[str, Any]], *, epsilon: float) -> list[dict[str, Any]]:
    by_order: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in summary:
        by_order[int(row['source_order_k'])].append(row)
    out: list[dict[str, Any]] = []
    for order, group in sorted(by_order.items()):
        group = sorted(group, key=lambda row: int(row['train_samples']))
        first = group[0]
        ideal_h = float(first['ideal_min_entropy'])
        learned = None
        for row in group:
            gap = abs(float(row['accessible_min_entropy_mean']) - ideal_h)
            if gap <= epsilon:
                learned = row
                break
        item: dict[str, Any] = {'source_family': first['source_family'], 'source_order_k': order, 'table_size': int(first['table_size']), 'epsilon_bits': epsilon, 'ideal_min_entropy': ideal_h, 'learned': int(learned is not None), 'required_samples': '', 'learned_accessible_min_entropy': '', 'learned_entropy_gap_abs': '', 'oracle_coverage_required_samples': coverage_required_samples(order, float(first['delta']), epsilon)}
        if learned is not None:
            item.update({'required_samples': int(learned['train_samples']), 'learned_accessible_min_entropy': float(learned['accessible_min_entropy_mean']), 'learned_entropy_gap_abs': abs(float(learned['accessible_min_entropy_mean']) - ideal_h)})
        out.append(item)
    return out

def row_for_run(*, args: argparse.Namespace, seed: int, order: int, train_samples: int, subset: tuple[int, ...], table: np.ndarray, metrics: dict[str, float], coverage_fraction: float, train_time_s: float, eval_time_s: float) -> dict[str, Any]:
    oracle_p = coverage_guessing_power(order, args.delta, train_samples)
    return {'source_family': 'noisy_boolean_lookup', 'source_order_k': order, 'source_subset': ' '.join(map(str, subset)), 'table_size': 2 ** order, 'rule_complexity_proxy': 2 ** order, 'p': args.p, 'delta': args.delta, 'theoretical_guessing_power': 1.0 - args.delta, 'ideal_min_entropy': metrics['ideal_min_entropy'], 'model_family': 'oracle_coordinate_lookup_majority', 'trainable_parameters': 2 ** order, 'train_samples': train_samples, 'test_samples': args.test_samples, 'seed': seed, 'coverage_fraction': coverage_fraction, 'oracle_coverage_guessing_power': oracle_p, 'oracle_coverage_min_entropy': min_entropy_from_guessing_power(oracle_p), 'raw_accuracy': metrics['raw_accuracy'], 'p_ml': metrics['p_ml'], 'accessible_min_entropy': metrics['accessible_min_entropy'], 'entropy_gap': metrics['entropy_gap'], 'train_time_s': train_time_s, 'eval_time_s': eval_time_s, 'table_checksum': int(np.sum(table.astype(np.int64)))}

def run(args: argparse.Namespace) -> list[dict[str, Any]]:
    orders = parse_int_list(args.orders, [4, 5, 6, 7, 8])
    train_grid = parse_int_list(args.train_samples, [16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024, 1536, 2048])
    for order in orders:
        if order < 0 or order > args.p:
            raise ValueError('every order must satisfy 0 <= order <= p')
    for train_samples in train_grid:
        if train_samples <= 0:
            raise ValueError('training sample counts must be positive')
    if args.test_samples <= 0:
        raise ValueError('test samples must be positive')
    if not 0 <= args.delta < 0.5:
        raise ValueError('delta must satisfy 0 <= delta < 0.5')
    if args.epsilon <= 0:
        raise ValueError('epsilon must be positive')
    args.out.mkdir(parents=True, exist_ok=True)
    write_json(args.out / 'config.json', {'p': args.p, 'orders': orders, 'train_samples': train_grid, 'test_samples': args.test_samples, 'delta': args.delta, 'ideal_min_entropy': ideal_min_entropy(args.delta), 'epsilon_bits': args.epsilon, 'seeds': args.seeds, 'subset_mode': args.subset_mode})
    rows: list[dict[str, Any]] = []
    total = len(args.seeds) * len(orders) * len(train_grid)
    current = 0
    progress = ProgressTimer(total)
    print(f'Sample-scaling sweep: runs={total} p={args.p} orders={orders} train_grid={train_grid[0]}..{train_grid[-1]} test={args.test_samples} epsilon={args.epsilon}')
    for seed in args.seeds:
        seed_rng = np.random.default_rng(seed)
        for order in orders:
            source_rng = np.random.default_rng(int(seed_rng.integers(0, 2 ** 32 - 1)))
            _, _, source = sample_noisy_lookup(1, args.p, order, args.delta, source_rng, subset_mode=args.subset_mode)
            train_rng = np.random.default_rng(seed + 100003 * (order + 1))
            x_train_full, y_train_full, _ = sample_noisy_lookup(max(train_grid), args.p, order, args.delta, train_rng, subset=source.subset, table=source.table, subset_mode=args.subset_mode)
            test_rng = np.random.default_rng(seed + 1000003 * (order + 1))
            x_test, y_test, _ = sample_noisy_lookup(args.test_samples, args.p, order, args.delta, test_rng, subset=source.subset, table=source.table, subset_mode=args.subset_mode)
            for train_samples in train_grid:
                current += 1
                x_train = x_train_full[:train_samples]
                y_train = y_train_full[:train_samples]
                started = time.perf_counter()
                table_hat, _, coverage_fraction = fit_lookup_majority(x_train, y_train, subset=source.subset, order=order)
                train_time_s = time.perf_counter() - started
                started = time.perf_counter()
                y_pred = table_hat[lookup_indices(x_test, source.subset)]
                eval_time_s = time.perf_counter() - started
                metrics = evaluate_predictions(y_test, y_pred, args.delta)
                row = row_for_run(args=args, seed=seed, order=order, train_samples=train_samples, subset=source.subset, table=source.table, metrics=metrics, coverage_fraction=coverage_fraction, train_time_s=train_time_s, eval_time_s=eval_time_s)
                rows.append(row)
                print(f"[{current:03d}/{total:03d}] seed={seed} k={order} N={train_samples} coverage={coverage_fraction:.3f} H_A={row['accessible_min_entropy']:.4f} p_ml={row['p_ml']:.4f} fit={format_duration(train_time_s)} eval={format_duration(eval_time_s)} {progress.status(current)}")
    write_csv(args.out / 'nice.csv', rows)
    summary = summarize(rows)
    write_csv(args.out / 'summary.csv', summary)
    thresholds = collect_thresholds(summary, epsilon=args.epsilon)
    write_csv(args.out / 'sample_thresholds.csv', thresholds)
    fit = fit_power_law(thresholds, x_key='table_size', y_key='required_samples', label='sample_size_vs_lookup_table_entries')
    write_json(args.out / 'scaling_fit.json', fit)
    if args.plot:
        plot_sample_scaling_curve(args.out / 'summary.csv', args.out / 'sample_scaling.png')
        plot_sample_scaling_curve(args.out / 'summary.csv', args.out / 'sample_scaling.pdf')
        plot_sample_thresholds(args.out / 'sample_thresholds.csv', args.out / 'sample_thresholds.png', fit)
        plot_sample_thresholds(args.out / 'sample_thresholds.csv', args.out / 'sample_thresholds.pdf', fit)
    return rows

def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run sample-size scaling experiments for noisy lookup rules.')
    parser.add_argument('--out', type=Path, default=Path('results/sample_scaling'))
    parser.add_argument('--p', type=int, default=10)
    parser.add_argument('--orders', type=int, nargs='+', default=None)
    parser.add_argument('--train-samples', type=int, nargs='+', default=None)
    parser.add_argument('--test-samples', type=int, default=20000)
    parser.add_argument('--delta', type=float, default=0.1)
    parser.add_argument('--epsilon', type=float, default=0.03)
    parser.add_argument('--seeds', type=int, nargs='+', default=[0, 1, 2, 3, 4])
    parser.add_argument('--subset-mode', choices=['prefix', 'random'], default='prefix', help='How to choose the lookup subset for each source order.')
    parser.add_argument('--plot', action='store_true', help='Write sample scaling plots.')
    return parser

def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()
    run(args)
if __name__ == '__main__':
    main()
