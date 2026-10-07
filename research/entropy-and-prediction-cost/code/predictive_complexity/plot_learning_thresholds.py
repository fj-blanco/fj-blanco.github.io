from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Any
from .io import write_csv, write_json
from .plotting import COLORS, MARKERS, PALETTE, _style_axis, plt
from .scaling import first_within_epsilon, fit_power_law, slope_label
from .walsh import model_budget

def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def collect_walsh_thresholds(path: Path, epsilon: float) -> list[dict[str, Any]]:
    rows = read_rows(path)
    by_order: dict[int, list[dict[str, str]]] = {}
    for row in rows:
        by_order.setdefault(int(row['source_order_k']), []).append(row)
    out = []
    for order, group in sorted(by_order.items()):
        learned = first_within_epsilon(group, size_key='model_budget_B', ideal_key='ideal_min_entropy', observed_key='accessible_min_entropy_mean', epsilon=epsilon)
        first = group[0]
        p = int(first['p'])
        source_complexity = model_budget(p, order)
        item = {'model_family': 'walsh_energy_projection', 'source_family': first['source_family'], 'source_order_k': order, 'source_complexity_proxy': source_complexity, 'source_complexity_label': 'critical_walsh_budget', 'epsilon_bits': epsilon, 'ideal_min_entropy': first['ideal_min_entropy'], 'learned': int(learned is not None), 'required_model_size': '', 'required_width_or_degree': '', 'learned_accessible_min_entropy': '', 'learned_entropy_gap_abs': ''}
        if learned is not None:
            item.update({'required_model_size': int(learned['model_budget_B']), 'required_width_or_degree': int(learned['model_degree_D']), 'learned_accessible_min_entropy': float(learned['accessible_min_entropy_mean']), 'learned_entropy_gap_abs': abs(float(learned['accessible_min_entropy_mean']) - float(learned['ideal_min_entropy']))})
        out.append(item)
    return out

def collect_mlp_thresholds(path: Path, epsilon: float) -> list[dict[str, Any]]:
    rows = read_rows(path)
    by_order: dict[int, list[dict[str, str]]] = {}
    for row in rows:
        by_order.setdefault(int(row['source_order_k']), []).append(row)
    out = []
    for order, group in sorted(by_order.items()):
        learned = first_within_epsilon(group, size_key='trainable_parameters', ideal_key='ideal_min_entropy', observed_key='accessible_min_entropy_mean', epsilon=epsilon)
        first = group[0]
        source_complexity = int(float(first['rule_complexity_proxy']))
        item = {'model_family': first['model_family'], 'source_family': first['source_family'], 'source_order_k': order, 'source_complexity_proxy': source_complexity, 'source_complexity_label': 'lookup_table_entries', 'epsilon_bits': epsilon, 'ideal_min_entropy': first['ideal_min_entropy'], 'learned': int(learned is not None), 'required_model_size': '', 'required_width_or_degree': '', 'learned_accessible_min_entropy': '', 'learned_entropy_gap_abs': ''}
        if learned is not None:
            item.update({'required_model_size': int(learned['trainable_parameters']), 'required_width_or_degree': int(learned['hidden_width']), 'learned_accessible_min_entropy': float(learned['accessible_min_entropy_mean']), 'learned_entropy_gap_abs': abs(float(learned['accessible_min_entropy_mean']) - float(learned['ideal_min_entropy']))})
        out.append(item)
    return out

def fit_threshold_scaling(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    walsh = [row for row in rows if row['model_family'] == 'walsh_energy_projection']
    mlp = [row for row in rows if row['model_family'] != 'walsh_energy_projection']
    return {'walsh_energy_model': fit_power_law(walsh, x_key='source_complexity_proxy', y_key='required_model_size', label='walsh_model_size_vs_critical_budget'), 'mlp_lookup_model': fit_power_law(mlp, x_key='source_complexity_proxy', y_key='required_model_size', label='mlp_parameters_vs_lookup_table_entries')}

def plot_thresholds(rows: list[dict[str, Any]], out_path: Path, epsilon: float, fits: dict[str, dict[str, Any]]) -> None:
    walsh = [row for row in rows if row['model_family'] == 'walsh_energy_projection']
    mlp = [row for row in rows if row['model_family'] != 'walsh_energy_projection']
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
    for ax in axes:
        _style_axis(ax)
    panels = [(axes[0], walsh, 'Walsh energy model', 'Walsh source complexity B_c(k)', 'Required Walsh coefficients', COLORS['green'], MARKERS[0], fits['walsh_energy_model']), (axes[1], mlp, 'MLP lookup model', 'Lookup table entries 2^k', 'Required MLP parameters', COLORS['cyan'], MARKERS[1], fits['mlp_lookup_model'])]
    for ax, panel_rows, title, xlabel, ylabel, color, marker, fit in panels:
        learned = [row for row in panel_rows if int(row['learned']) == 1]
        missing = [row for row in panel_rows if int(row['learned']) == 0]
        x = [float(row['source_complexity_proxy']) for row in learned]
        y = [float(row['required_model_size']) for row in learned]
        ax.plot(x, y, marker=marker, markersize=6, linewidth=2.0, markeredgecolor='black', markeredgewidth=0.55, color=color, label=slope_label(f'epsilon = {epsilon:g} bits', fit), zorder=3)
        if missing:
            x_missing = [float(row['source_complexity_proxy']) for row in missing]
            y_floor = min(y) if y else 1.0
            ax.scatter(x_missing, [y_floor] * len(x_missing), marker='x', color=PALETTE[-1], label='not reached', zorder=4)
        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.legend(frameon=True, fancybox=True)
    fig.suptitle('Model size required to reach the ideal min-entropy', y=1.03)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Plot learned-size thresholds from Walsh and MLP summaries.')
    parser.add_argument('--walsh-summary', type=Path, required=True)
    parser.add_argument('--mlp-summary', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('results/learning_thresholds'))
    parser.add_argument('--epsilon', type=float, default=0.03)
    return parser

def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()
    if args.epsilon <= 0:
        raise ValueError('epsilon must be positive')
    args.out.mkdir(parents=True, exist_ok=True)
    rows = collect_walsh_thresholds(args.walsh_summary, args.epsilon)
    rows += collect_mlp_thresholds(args.mlp_summary, args.epsilon)
    fits = fit_threshold_scaling(rows)
    write_csv(args.out / 'learning_thresholds.csv', rows)
    write_json(args.out / 'scaling_fits.json', fits)
    write_json(args.out / 'config.json', {'epsilon_bits': args.epsilon, 'walsh_summary': str(args.walsh_summary), 'mlp_summary': str(args.mlp_summary), 'scaling_fits': 'scaling_fits.json'})
    plot_thresholds(rows, args.out / 'learning_thresholds.png', args.epsilon, fits)
    plot_thresholds(rows, args.out / 'learning_thresholds.pdf', args.epsilon, fits)
if __name__ == '__main__':
    main()
