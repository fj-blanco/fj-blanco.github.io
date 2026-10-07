from __future__ import annotations
import argparse
import time
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Any
import numpy as np
from .io import write_csv, write_json
from .metrics import evaluate_predictions, ideal_min_entropy
from .plotting import plot_dense_budget_curve
from .progress import ProgressTimer, format_duration
from .sources import sample_noisy_parity
from .walsh import combinations_up_to_degree, walsh_features

def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Dense random-feature budget sweep for one noisy Walsh source.')
    parser.add_argument('--out', type=Path, default=Path('results/dense_k6'))
    parser.add_argument('--p', type=int, default=12)
    parser.add_argument('--order', type=int, default=6)
    parser.add_argument('--candidate-degree', type=int, default=None)
    parser.add_argument('--delta', type=float, default=0.1)
    parser.add_argument('--train-samples', type=int, default=6000)
    parser.add_argument('--test-samples', type=int, default=6000)
    parser.add_argument('--data-seeds', type=int, nargs='+', default=[0, 1, 2])
    parser.add_argument('--feature-seeds', type=int, default=80)
    parser.add_argument('--num-budgets', type=int, default=41)
    parser.add_argument('--budgets', type=int, nargs='+', default=None)
    parser.add_argument('--plot', action='store_true')
    return parser

def validate_args(args: argparse.Namespace) -> None:
    if args.p <= 0:
        raise ValueError('p must be positive')
    if args.order < 0 or args.order > args.p:
        raise ValueError('order must satisfy 0 <= order <= p')
    if args.candidate_degree is None:
        args.candidate_degree = args.order
    if args.candidate_degree < args.order or args.candidate_degree > args.p:
        raise ValueError('candidate degree must satisfy order <= degree <= p')
    if not 0 <= args.delta < 0.5:
        raise ValueError('delta must satisfy 0 <= delta < 0.5')
    if args.train_samples <= 0 or args.test_samples <= 0:
        raise ValueError('sample counts must be positive')
    if args.num_budgets <= 1:
        raise ValueError('num-budgets must be greater than one')
    if args.feature_seeds <= 0:
        raise ValueError('feature-seeds must be positive')

def default_budgets(max_budget: int, num_budgets: int) -> list[int]:
    raw = np.linspace(1, max_budget, num_budgets)
    return sorted(set(np.rint(raw).astype(int).tolist()))

def summarize_dense(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[int(row['feature_budget_B'])].append(row)
    summary = []
    for budget, group in sorted(grouped.items()):
        first = group[0]
        h_vals = [float(row['accessible_min_entropy']) for row in group]
        p_vals = [float(row['p_ml']) for row in group]
        acc_vals = [float(row['raw_accuracy']) for row in group]
        contains_vals = [float(row['contains_rule']) for row in group]
        summary.append({'source_family': first['source_family'], 'source_order_k': first['source_order_k'], 'p': first['p'], 'delta': first['delta'], 'ideal_min_entropy': first['ideal_min_entropy'], 'model_family': first['model_family'], 'candidate_degree': first['candidate_degree'], 'candidate_terms_M': first['candidate_terms_M'], 'feature_budget_B': budget, 'budget_fraction': budget / int(first['candidate_terms_M']), 'runs': len(group), 'contains_rule_mean': mean(contains_vals), 'raw_accuracy_mean': mean(acc_vals), 'raw_accuracy_std': stdev(acc_vals) if len(acc_vals) > 1 else 0.0, 'p_ml_mean': mean(p_vals), 'p_ml_std': stdev(p_vals) if len(p_vals) > 1 else 0.0, 'accessible_min_entropy_mean': mean(h_vals), 'accessible_min_entropy_std': stdev(h_vals) if len(h_vals) > 1 else 0.0})
    return summary

def run(args: argparse.Namespace) -> list[dict[str, Any]]:
    validate_args(args)
    args.out.mkdir(parents=True, exist_ok=True)
    terms = combinations_up_to_degree(args.p, args.candidate_degree)
    candidate_terms = len(terms)
    target_term = tuple(range(args.order))
    if target_term not in terms:
        raise RuntimeError('target term is not in the candidate dictionary')
    target_index = terms.index(target_term)
    budgets = args.budgets or default_budgets(candidate_terms, args.num_budgets)
    budgets = sorted(set((max(1, min(candidate_terms, b)) for b in budgets)))
    config = {'p': args.p, 'order': args.order, 'candidate_degree': args.candidate_degree, 'candidate_terms': candidate_terms, 'target_index': target_index, 'delta': args.delta, 'ideal_min_entropy': ideal_min_entropy(args.delta), 'train_samples': args.train_samples, 'test_samples': args.test_samples, 'data_seeds': args.data_seeds, 'feature_seeds': args.feature_seeds, 'budgets': budgets}
    write_json(args.out / 'config.json', config)
    rows: list[dict[str, Any]] = []
    total = len(args.data_seeds) * args.feature_seeds * len(budgets)
    current = 0
    progress = ProgressTimer(total)
    print(f'Dense random-budget sweep: runs={total} p={args.p} k={args.order} D<={args.candidate_degree} candidate_terms={candidate_terms} data_seeds={len(args.data_seeds)} feature_seeds={args.feature_seeds}')
    for data_seed in args.data_seeds:
        train_rng = np.random.default_rng(data_seed)
        x_train, y_train, source = sample_noisy_parity(args.train_samples, args.p, args.order, args.delta, train_rng, subset=target_term)
        test_rng = np.random.default_rng(data_seed + 10000 * (args.order + 1))
        x_test, y_test, _ = sample_noisy_parity(args.test_samples, args.p, args.order, args.delta, test_rng, subset=source.subset)
        started = time.perf_counter()
        phi_train = walsh_features(x_train, terms)
        theta_full = phi_train.T @ y_train.astype(np.float32) / args.train_samples
        del phi_train
        phi_test = walsh_features(x_test, terms)
        basis_time_s = time.perf_counter() - started
        for feature_seed in range(args.feature_seeds):
            rng = np.random.default_rng(1000003 * data_seed + feature_seed)
            permutation = rng.permutation(candidate_terms)
            target_rank = int(np.where(permutation == target_index)[0][0]) + 1
            scores = np.zeros(args.test_samples, dtype=np.float32)
            previous_budget = 0
            for budget in budgets:
                current += 1
                started = time.perf_counter()
                block = permutation[previous_budget:budget]
                if len(block) > 0:
                    scores += phi_test[:, block] @ theta_full[block]
                previous_budget = budget
                y_pred = np.where(scores >= 0, 1, -1).astype(np.int8)
                eval_time_s = time.perf_counter() - started
                metrics = evaluate_predictions(y_test, y_pred, args.delta)
                row = {'source_family': 'noisy_walsh_parity', 'source_order_k': args.order, 'source_subset': ' '.join(map(str, source.subset)), 'p': args.p, 'delta': args.delta, 'ideal_min_entropy': metrics['ideal_min_entropy'], 'model_family': 'random_walsh_feature_projection', 'candidate_degree': args.candidate_degree, 'candidate_terms_M': candidate_terms, 'feature_budget_B': budget, 'budget_fraction': budget / candidate_terms, 'contains_rule': int(target_rank <= budget), 'target_rank': target_rank, 'train_samples': args.train_samples, 'test_samples': args.test_samples, 'data_seed': data_seed, 'feature_seed': feature_seed, 'raw_accuracy': metrics['raw_accuracy'], 'p_ml': metrics['p_ml'], 'accessible_min_entropy': metrics['accessible_min_entropy'], 'entropy_gap': metrics['entropy_gap'], 'basis_time_s': basis_time_s, 'eval_time_s': eval_time_s}
                rows.append(row)
                if current == 1 or current % 250 == 0 or current == total:
                    print(f"[{current:05d}/{total:05d}] data_seed={data_seed} feature_seed={feature_seed} B={budget}/{candidate_terms} hit={row['contains_rule']} H_A={row['accessible_min_entropy']:.4f} step={format_duration(eval_time_s)} {progress.status(current)}")
    write_csv(args.out / 'nice.csv', rows)
    summary = summarize_dense(rows)
    write_csv(args.out / 'summary.csv', summary)
    if args.plot:
        plot_dense_budget_curve(args.out / 'summary.csv', args.out / 'dense_budget_curve.png')
        plot_dense_budget_curve(args.out / 'summary.csv', args.out / 'dense_budget_curve.pdf')
    return rows

def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()
    run(args)
if __name__ == '__main__':
    main()
