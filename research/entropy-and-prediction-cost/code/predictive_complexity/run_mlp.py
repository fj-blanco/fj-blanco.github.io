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
from .mlp_numpy import fit_mlp_classifier, mlp_parameter_count
from .mlp_torch import fit_mlp_classifier_torch, resolve_torch_device, torch_available, torch_import_error
from .plotting import plot_mlp_curve
from .progress import ProgressTimer, format_duration
from .sources import sample_noisy_lookup, sample_noisy_parity

def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Run a smooth-width MLP sweep on noisy Walsh/parity sources.')
    parser.add_argument('--out', type=Path, default=Path('results/mlp_smoke'))
    parser.add_argument('--p', type=int, default=8)
    parser.add_argument('--source', choices=['parity', 'lookup'], default='parity')
    parser.add_argument('--orders', type=int, nargs='+', default=[2, 3, 4])
    parser.add_argument('--hidden-widths', type=int, nargs='+', default=[2, 4, 6, 8, 12, 16, 24, 32, 48, 64])
    parser.add_argument('--hidden-layers', type=int, default=2)
    parser.add_argument('--activation', choices=['tanh', 'relu'], default='tanh')
    parser.add_argument('--delta', type=float, default=0.1)
    parser.add_argument('--train-samples', type=int, default=4000)
    parser.add_argument('--test-samples', type=int, default=4000)
    parser.add_argument('--seeds', type=int, nargs='+', default=[0, 1])
    parser.add_argument('--epochs', type=int, default=350)
    parser.add_argument('--batch-size', type=int, default=256)
    parser.add_argument('--learning-rate', type=float, default=0.005)
    parser.add_argument('--weight-decay', type=float, default=0.0)
    parser.add_argument('--grad-clip', type=float, default=5.0)
    parser.add_argument('--backend', choices=['numpy', 'torch', 'auto'], default='numpy', help="MLP training backend. 'auto' uses torch when it is installed.")
    parser.add_argument('--device', default='auto', help='Torch device, such as auto, cpu, cuda, or cuda:0.')
    parser.add_argument('--torch-deterministic', action='store_true', help='Ask PyTorch to prefer deterministic algorithms when using torch.')
    parser.add_argument('--fit-progress-epochs', type=int, default=0, help='Print within-fit progress every N epochs. Use 0 to print per fit only.')
    parser.add_argument('--subset-mode', choices=['prefix', 'random'], default='prefix', help='How to choose the parity subset for each source order.')
    parser.add_argument('--plot', action='store_true')
    return parser

def validate_args(args: argparse.Namespace) -> None:
    if args.p <= 0:
        raise ValueError('p must be positive')
    if args.hidden_layers <= 0:
        raise ValueError('hidden-layers must be positive')
    if any((width <= 0 for width in args.hidden_widths)):
        raise ValueError('hidden-widths must be positive')
    if any((order < 0 or order > args.p for order in args.orders)):
        raise ValueError('every order must satisfy 0 <= order <= p')
    if not 0 <= args.delta < 0.5:
        raise ValueError('delta must satisfy 0 <= delta < 0.5')
    if args.train_samples <= 0 or args.test_samples <= 0:
        raise ValueError('sample counts must be positive')
    if args.epochs <= 0:
        raise ValueError('epochs must be positive')
    if args.batch_size <= 0:
        raise ValueError('batch size must be positive')
    if args.learning_rate <= 0:
        raise ValueError('learning rate must be positive')
    if args.fit_progress_epochs < 0:
        raise ValueError('fit-progress-epochs must be non-negative')

def resolve_backend(args: argparse.Namespace) -> tuple[str, str]:
    if args.backend == 'numpy':
        return ('numpy', 'cpu')
    if args.backend == 'torch':
        return ('torch', resolve_torch_device(args.device))
    import_error = torch_import_error()
    if import_error is None:
        return ('torch', resolve_torch_device(args.device))
    print(f'warning: --backend auto could not import PyTorch; falling back to numpy/cpu ({import_error})')
    return ('numpy', 'cpu')

def summarize_mlp(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[int(row['source_order_k']), int(row['hidden_width'])].append(row)
    summary = []
    for (order, hidden_width), group in sorted(grouped.items()):
        first = group[0]
        values = {key: [float(row[key]) for row in group] for key in ['raw_accuracy', 'p_ml', 'accessible_min_entropy', 'entropy_gap', 'train_accuracy', 'final_loss']}
        item = {'source_family': first['source_family'], 'source_order_k': order, 'model_family': first['model_family'], 'backend': first.get('backend', ''), 'device': first.get('device', ''), 'hidden_layers': first['hidden_layers'], 'hidden_width': hidden_width, 'activation': first['activation'], 'trainable_parameters': first['trainable_parameters'], 'parameter_count_formula': first['parameter_count_formula'], 'rule_complexity_proxy': first['rule_complexity_proxy'], 'parity_width_proxy': first['parity_width_proxy'], 'meets_width_proxy': first['meets_width_proxy'], 'p': first['p'], 'delta': first['delta'], 'train_samples': first['train_samples'], 'test_samples': first['test_samples'], 'epochs': first['epochs'], 'seeds': len(group), 'ideal_min_entropy': first['ideal_min_entropy']}
        for key, vals in values.items():
            item[f'{key}_mean'] = mean(vals)
            item[f'{key}_std'] = stdev(vals) if len(vals) > 1 else 0.0
        summary.append(item)
    return summary

def run(args: argparse.Namespace) -> list[dict[str, Any]]:
    validate_args(args)
    args.out.mkdir(parents=True, exist_ok=True)
    hidden_widths = sorted(set(args.hidden_widths))
    backend, device = resolve_backend(args)
    config = {'p': args.p, 'source': args.source, 'orders': args.orders, 'hidden_widths': hidden_widths, 'hidden_layers': args.hidden_layers, 'activation': args.activation, 'delta': args.delta, 'ideal_min_entropy': ideal_min_entropy(args.delta), 'train_samples': args.train_samples, 'test_samples': args.test_samples, 'seeds': args.seeds, 'epochs': args.epochs, 'batch_size': args.batch_size, 'learning_rate': args.learning_rate, 'weight_decay': args.weight_decay, 'grad_clip': args.grad_clip, 'requested_backend': args.backend, 'resolved_backend': backend, 'device': device, 'torch_available': torch_available(), 'torch_deterministic': args.torch_deterministic, 'fit_progress_epochs': args.fit_progress_epochs, 'subset_mode': args.subset_mode}
    write_json(args.out / 'config.json', config)
    rows: list[dict[str, Any]] = []
    total = len(args.seeds) * len(args.orders) * len(hidden_widths)
    current = 0
    progress = ProgressTimer(total)
    print(f'MLP sweep: backend={backend} device={device} runs={total} train={args.train_samples} test={args.test_samples} epochs={args.epochs} batch={args.batch_size}')
    for seed in args.seeds:
        seed_rng = np.random.default_rng(seed)
        subsets = {order: None for order in args.orders}
        for order in args.orders:
            if args.subset_mode == 'random':
                subset_rng = np.random.default_rng(int(seed_rng.integers(0, 2 ** 32 - 1)))
            else:
                subset_rng = seed_rng
            if args.source == 'parity':
                x_train, y_train, source = sample_noisy_parity(args.train_samples, args.p, order, args.delta, subset_rng, subset=subsets[order], subset_mode=args.subset_mode)
            else:
                x_train, y_train, source = sample_noisy_lookup(args.train_samples, args.p, order, args.delta, subset_rng, subset=subsets[order], subset_mode=args.subset_mode)
            subsets[order] = source.subset
            test_rng = np.random.default_rng(seed + 10000 * (order + 1))
            if args.source == 'parity':
                x_test, y_test, _ = sample_noisy_parity(args.test_samples, args.p, order, args.delta, test_rng, subset=source.subset, subset_mode=args.subset_mode)
            else:
                x_test, y_test, _ = sample_noisy_lookup(args.test_samples, args.p, order, args.delta, test_rng, subset=source.subset, table=source.table, subset_mode=args.subset_mode)
            for hidden_width in hidden_widths:
                current += 1
                model_seed = 1000003 * seed + 10007 * order + 101 * hidden_width + args.hidden_layers
                rng = np.random.default_rng(model_seed)
                print(f'[{current:03d}/{total:03d}] starting backend={backend} seed={seed} k={order} width={hidden_width} {progress.status(current - 1)}')
                fit_timer = ProgressTimer(args.epochs)

                def report_epoch(epoch: int, epochs: int, loss: float) -> None:
                    if args.fit_progress_epochs <= 0:
                        return
                    if epoch != 1 and epoch % args.fit_progress_epochs != 0 and (epoch != epochs):
                        return
                    print(f'    fit epoch={epoch:04d}/{epochs:04d} loss={loss:.4f} elapsed={format_duration(fit_timer.elapsed_s)} eta={format_duration(fit_timer.eta_s(epoch))}')
                started = time.perf_counter()
                if backend == 'torch':
                    result = fit_mlp_classifier_torch(x_train, y_train, hidden_width=hidden_width, hidden_layers=args.hidden_layers, seed=model_seed, activation=args.activation, epochs=args.epochs, batch_size=args.batch_size, learning_rate=args.learning_rate, weight_decay=args.weight_decay, grad_clip=args.grad_clip, device=device, deterministic=args.torch_deterministic, progress_callback=report_epoch if args.fit_progress_epochs > 0 else None)
                else:
                    result = fit_mlp_classifier(x_train, y_train, hidden_width=hidden_width, hidden_layers=args.hidden_layers, rng=rng, activation=args.activation, epochs=args.epochs, batch_size=args.batch_size, learning_rate=args.learning_rate, weight_decay=args.weight_decay, grad_clip=args.grad_clip, progress_callback=report_epoch if args.fit_progress_epochs > 0 else None)
                train_time_s = time.perf_counter() - started
                started = time.perf_counter()
                y_pred = result.model.predict(x_test, batch_size=args.batch_size)
                eval_time_s = time.perf_counter() - started
                metrics = evaluate_predictions(y_test, y_pred, args.delta)
                if args.source == 'parity':
                    rule_complexity_proxy = 1 if order == 0 else 2 ** max(order - 1, 0)
                else:
                    rule_complexity_proxy = 2 ** order
                expected_parameters = mlp_parameter_count(args.p, hidden_width, args.hidden_layers)
                if result.model.trainable_parameters != expected_parameters:
                    raise RuntimeError(f'MLP parameter count mismatch: model={result.model.trainable_parameters} formula={expected_parameters}')
                row = {'source_family': 'noisy_walsh_parity' if args.source == 'parity' else 'noisy_boolean_lookup', 'source_order_k': order, 'source_subset': ' '.join(map(str, source.subset)), 'p': args.p, 'delta': args.delta, 'theoretical_guessing_power': 1.0 - args.delta, 'ideal_min_entropy': metrics['ideal_min_entropy'], 'model_family': f'{backend}_mlp', 'backend': backend, 'device': device, 'hidden_layers': args.hidden_layers, 'hidden_width': hidden_width, 'activation': args.activation, 'trainable_parameters': result.model.trainable_parameters, 'parameter_count_formula': expected_parameters, 'rule_complexity_proxy': rule_complexity_proxy, 'parity_width_proxy': rule_complexity_proxy, 'meets_width_proxy': int(hidden_width >= rule_complexity_proxy), 'train_samples': args.train_samples, 'test_samples': args.test_samples, 'epochs': args.epochs, 'batch_size': args.batch_size, 'learning_rate': args.learning_rate, 'weight_decay': args.weight_decay, 'seed': seed, 'model_seed': model_seed, 'train_accuracy': result.train_accuracy, 'final_loss': result.final_loss, 'raw_accuracy': metrics['raw_accuracy'], 'p_ml': metrics['p_ml'], 'accessible_min_entropy': metrics['accessible_min_entropy'], 'entropy_gap': metrics['entropy_gap'], 'train_time_s': train_time_s, 'eval_time_s': eval_time_s}
                rows.append(row)
                print(f"[{current:03d}/{total:03d}] done backend={backend} seed={seed} k={order} width={hidden_width} params={row['trainable_parameters']} train_acc={row['train_accuracy']:.3f} H_A={row['accessible_min_entropy']:.4f} p_ml={row['p_ml']:.4f} fit={format_duration(train_time_s)} eval={format_duration(eval_time_s)} {progress.status(current)}")
    write_csv(args.out / 'nice.csv', rows)
    summary = summarize_mlp(rows)
    write_csv(args.out / 'summary.csv', summary)
    if args.plot:
        plot_mlp_curve(args.out / 'summary.csv', args.out / 'mlp_capacity_curve.png')
        plot_mlp_curve(args.out / 'summary.csv', args.out / 'mlp_capacity_curve.pdf')
    return rows

def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()
    run(args)
if __name__ == '__main__':
    main()
