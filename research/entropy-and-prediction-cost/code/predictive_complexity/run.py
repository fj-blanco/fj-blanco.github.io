from __future__ import annotations
import argparse
import time
from pathlib import Path
from typing import Any
import numpy as np
from .io import summarize, write_csv, write_json
from .learners import fit_walsh_projection
from .metrics import evaluate_predictions, ideal_min_entropy
from .plotting import plot_accessibility_curve
from .progress import ProgressTimer, format_duration
from .sources import sample_noisy_parity
from .walsh import model_budget

def parse_int_list(values: list[int] | None, fallback: list[int]) -> list[int]:
    return fallback if values is None else values

def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run noisy Walsh predictive-complexity experiments.')
    parser.add_argument('--out', type=Path, default=Path('results/smoke'))
    parser.add_argument('--p', type=int, default=8)
    parser.add_argument('--orders', type=int, nargs='+', default=None)
    parser.add_argument('--degrees', type=int, nargs='+', default=None)
    parser.add_argument('--delta', type=float, default=0.1)
    parser.add_argument('--train-samples', type=int, default=4000)
    parser.add_argument('--test-samples', type=int, default=4000)
    parser.add_argument('--seeds', type=int, nargs='+', default=[0, 1])
    parser.add_argument('--batch-size', type=int, default=1024)
    parser.add_argument('--subset-mode', choices=['prefix', 'random'], default='prefix', help='How to choose the parity subset for each source order.')
    parser.add_argument('--plot', action='store_true', help='Write accessibility_curve.png after the run.')
    return parser

def validate_args(args: argparse.Namespace) -> None:
    if args.p <= 0:
        raise ValueError('p must be positive')
    if not 0 <= args.delta < 0.5:
        raise ValueError('delta must satisfy 0 <= delta < 0.5')
    if args.train_samples <= 0 or args.test_samples <= 0:
        raise ValueError('sample counts must be positive')
    if args.batch_size <= 0:
        raise ValueError('batch size must be positive')

def row_for_run(*, args: argparse.Namespace, seed: int, order: int, degree: int, subset: tuple[int, ...], metrics: dict[str, float], train_time_s: float, eval_time_s: float) -> dict[str, Any]:
    budget = model_budget(args.p, degree)
    return {'source_family': 'noisy_walsh_parity', 'source_order_k': order, 'source_subset': ' '.join(map(str, subset)), 'p': args.p, 'delta': args.delta, 'theoretical_guessing_power': 1.0 - args.delta, 'ideal_min_entropy': metrics['ideal_min_entropy'], 'model_family': 'walsh_energy_projection', 'model_degree_D': degree, 'model_budget_B': budget, 'trainable_parameters': budget, 'contains_rule': int(degree >= order), 'train_samples': args.train_samples, 'test_samples': args.test_samples, 'seed': seed, 'raw_accuracy': metrics['raw_accuracy'], 'p_ml': metrics['p_ml'], 'accessible_min_entropy': metrics['accessible_min_entropy'], 'entropy_gap': metrics['entropy_gap'], 'train_time_s': train_time_s, 'eval_time_s': eval_time_s}

def run_experiment(args: argparse.Namespace) -> list[dict[str, Any]]:
    orders = parse_int_list(args.orders, [1, 2, 3])
    degrees = parse_int_list(args.degrees, list(range(max(orders) + 1)))
    for order in orders:
        if order < 0 or order > args.p:
            raise ValueError('every order must satisfy 0 <= order <= p')
    for degree in degrees:
        if degree < 0 or degree > args.p:
            raise ValueError('every degree must satisfy 0 <= degree <= p')
    args.out.mkdir(parents=True, exist_ok=True)
    config = {'p': args.p, 'orders': orders, 'degrees': degrees, 'delta': args.delta, 'ideal_min_entropy': ideal_min_entropy(args.delta), 'train_samples': args.train_samples, 'test_samples': args.test_samples, 'seeds': args.seeds, 'batch_size': args.batch_size, 'subset_mode': args.subset_mode}
    write_json(args.out / 'config.json', config)
    rows: list[dict[str, Any]] = []
    total = len(args.seeds) * len(orders) * len(degrees)
    current = 0
    progress = ProgressTimer(total)
    print(f'Walsh sweep: runs={total} p={args.p} orders={orders} degrees={degrees} train={args.train_samples} test={args.test_samples}')
    for seed in args.seeds:
        seed_rng = np.random.default_rng(seed)
        subsets = {order: None for order in orders}
        for order in orders:
            if args.subset_mode == 'random':
                subset_seed = int(seed_rng.integers(0, 2 ** 32 - 1))
                subset_rng = np.random.default_rng(subset_seed)
            else:
                subset_rng = seed_rng
            x_train, y_train, source = sample_noisy_parity(args.train_samples, args.p, order, args.delta, subset_rng, subset=subsets[order], subset_mode=args.subset_mode)
            subsets[order] = source.subset
            test_rng = np.random.default_rng(seed + 10000 * (order + 1))
            x_test, y_test, _ = sample_noisy_parity(args.test_samples, args.p, order, args.delta, test_rng, subset=source.subset, subset_mode=args.subset_mode)
            for degree in degrees:
                current += 1
                started = time.perf_counter()
                model = fit_walsh_projection(x_train, y_train, degree=degree, batch_size=args.batch_size)
                train_time_s = time.perf_counter() - started
                started = time.perf_counter()
                y_pred = model.predict(x_test, batch_size=args.batch_size)
                eval_time_s = time.perf_counter() - started
                metrics = evaluate_predictions(y_test, y_pred, args.delta)
                row = row_for_run(args=args, seed=seed, order=order, degree=degree, subset=source.subset, metrics=metrics, train_time_s=train_time_s, eval_time_s=eval_time_s)
                rows.append(row)
                print(f"[{current:03d}/{total:03d}] seed={seed} k={order} D={degree} B={row['model_budget_B']} H_A={row['accessible_min_entropy']:.4f} p_ml={row['p_ml']:.4f} fit={format_duration(train_time_s)} eval={format_duration(eval_time_s)} {progress.status(current)}")
    write_csv(args.out / 'nice.csv', rows)
    summary = summarize(rows)
    write_csv(args.out / 'summary.csv', summary)
    if args.plot:
        plot_accessibility_curve(args.out / 'summary.csv', args.out / 'accessibility_curve.png')
        plot_accessibility_curve(args.out / 'summary.csv', args.out / 'accessibility_curve.pdf')
    return rows

def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()
    validate_args(args)
    run_experiment(args)
if __name__ == '__main__':
    main()
