from __future__ import annotations
import csv
import os
import tempfile
from collections import defaultdict
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', str(Path(tempfile.gettempdir()) / 'matplotlib'))
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib import font_manager
from .scaling import slope_label
from .walsh import model_budget
_available_fonts = {font.name for font in font_manager.fontManager.ttflist}
plt.rcParams['font.family'] = 'Ubuntu' if 'Ubuntu' in _available_fonts else 'DejaVu Sans'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
_CMAP = mcolors.LinearSegmentedColormap.from_list('', ['#9fcf69', '#33acdc'])
PALETTE = [_CMAP(x) for x in [0.0, 0.14, 0.28, 0.42, 0.56, 0.7, 0.84, 1.0]]
MARKERS = ['o', 's', 'D', '^', 'v', 'P', 'X', 'h']
COLORS = {'green': PALETTE[0], 'lime': PALETTE[1], 'orange': PALETTE[2], 'teal': PALETTE[3], 'cyan': PALETTE[4], 'red': PALETTE[5], 'purple': PALETTE[6], 'blue': PALETTE[7], 'grey': '#999999', 'dark': '#222222'}
RC_PARAMS = {'font.size': 9, 'axes.titlesize': 10, 'axes.titleweight': 'bold', 'axes.labelsize': 9, 'axes.labelweight': 'bold', 'xtick.labelsize': 8, 'ytick.labelsize': 8, 'legend.fontsize': 7, 'figure.figsize': (6.4, 4.1), 'figure.dpi': 150, 'savefig.dpi': 300, 'axes.prop_cycle': plt.cycler('color', PALETTE)}
plt.rcParams.update(RC_PARAMS)

def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def _style_axis(ax) -> None:
    ax.grid(True, axis='y', linestyle='--', which='major', color='grey', alpha=0.38)
    ax.grid(True, axis='x', linestyle='--', which='major', color='grey', alpha=0.34)
    ax.set_axisbelow(True)

def plot_accessibility_curve(summary_csv: Path, out_png: Path) -> None:
    rows = _read_csv(summary_csv)
    if not rows:
        raise ValueError('summary CSV is empty')
    by_order: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_order[int(row['source_order_k'])].append(row)
    p = int(rows[0]['p'])
    ideal_h = float(rows[0]['ideal_min_entropy'])
    fig, ax = plt.subplots()
    _style_axis(ax)
    for order, group in sorted(by_order.items()):
        group = sorted(group, key=lambda r: int(r['model_budget_B']))
        x = [int(r['model_budget_B']) for r in group]
        y = [float(r['accessible_min_entropy_mean']) for r in group]
        yerr = [float(r['accessible_min_entropy_std']) for r in group]
        color = PALETTE[(order - 1) % len(PALETTE)]
        marker = MARKERS[(order - 1) % len(MARKERS)]
        ax.errorbar(x, y, yerr=yerr, marker=marker, markersize=4.8, linewidth=1.8, markeredgecolor='black', markeredgewidth=0.45, color=color, capsize=3, capthick=1.0, elinewidth=1.0, label=f'k={order}', zorder=3)
        critical_budget = model_budget(p, order)
        ax.axvline(critical_budget, color=color, alpha=0.17, linewidth=1.2, zorder=1)
    ax.axhline(1.0, color=COLORS['dark'], linestyle=':', linewidth=1.3, label='chance')
    ax.axhline(ideal_h, color=COLORS['grey'], linestyle='--', linewidth=1.4, label='ideal')
    ax.set_xscale('log')
    ax.set_xlabel('Model budget B(D)')
    ax.set_ylabel('Accessible min-entropy')
    ax.set_title('Same min-entropy, different predictive complexity')
    ax.set_ylim(0.08, 1.06)
    ax.legend(ncols=2, frameon=True, fancybox=True)
    fig.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_dense_budget_curve(summary_csv: Path, out_path: Path) -> None:
    rows = _read_csv(summary_csv)
    if not rows:
        raise ValueError('summary CSV is empty')
    x = [float(row['budget_fraction']) for row in rows]
    y = [float(row['accessible_min_entropy_mean']) for row in rows]
    yerr = [float(row['accessible_min_entropy_std']) / max(float(row['runs']), 1.0) ** 0.5 for row in rows]
    ideal_h = float(rows[0]['ideal_min_entropy'])
    order = int(rows[0]['source_order_k'])
    p = int(rows[0]['p'])
    candidate_degree = int(rows[0]['candidate_degree'])
    fig, ax = plt.subplots()
    _style_axis(ax)
    color = COLORS['cyan']
    ax.errorbar(x, y, yerr=yerr, marker='o', markersize=4.2, linewidth=1.8, markeredgecolor='black', markeredgewidth=0.45, color=color, capsize=2.5, capthick=1.0, elinewidth=1.0, label='measured mean', zorder=3)
    ax.axhline(1.0, color=COLORS['dark'], linestyle=':', linewidth=1.3, label='chance')
    ax.axhline(ideal_h, color=COLORS['grey'], linestyle='--', linewidth=1.4, label='ideal')
    ax.set_xlabel('Random feature budget fraction B / M')
    ax.set_ylabel('Accessible min-entropy')
    ax.set_title(f'Dense random-budget sweep, k={order}, p={p}, D<= {candidate_degree}')
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(0.08, 1.06)
    ax.legend(frameon=True, fancybox=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_mlp_curve(summary_csv: Path, out_path: Path) -> None:
    rows = _read_csv(summary_csv)
    if not rows:
        raise ValueError('summary CSV is empty')
    by_order: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_order[int(row['source_order_k'])].append(row)
    ideal_h = float(rows[0]['ideal_min_entropy'])
    hidden_layers = int(rows[0]['hidden_layers'])
    activation = rows[0]['activation']
    source_family = rows[0]['source_family']
    source_label = 'noisy lookup' if source_family == 'noisy_boolean_lookup' else source_family.replace('_', ' ')
    fig, ax = plt.subplots()
    _style_axis(ax)
    orders = sorted(by_order)
    for index, order in enumerate(orders):
        group = by_order[order]
        group = sorted(group, key=lambda r: int(r['trainable_parameters']))
        x = [int(r['trainable_parameters']) for r in group]
        y = [float(r['accessible_min_entropy_mean']) for r in group]
        yerr = [float(r['accessible_min_entropy_std']) for r in group]
        color_index = round(index * (len(PALETTE) - 1) / max(len(orders) - 1, 1))
        color = PALETTE[color_index]
        marker = MARKERS[index % len(MARKERS)]
        ax.errorbar(x, y, yerr=yerr, marker=marker, markersize=4.6, linewidth=1.8, markeredgecolor='black', markeredgewidth=0.45, color=color, capsize=3, capthick=1.0, elinewidth=1.0, label=f'k={order}', zorder=3)
    ax.axhline(1.0, color=COLORS['dark'], linestyle=':', linewidth=1.3, label='chance')
    ax.axhline(ideal_h, color=COLORS['grey'], linestyle='--', linewidth=1.4, label='ideal')
    ax.set_xscale('log')
    ax.set_xlabel('Trainable parameters')
    ax.set_ylabel('Accessible min-entropy')
    ax.set_title(f'MLP capacity sweep on {source_label} rules')
    ax.set_ylim(0.08, 1.06)
    ax.legend(ncols=2, frameon=True, fancybox=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_sample_scaling_curve(summary_csv: Path, out_path: Path) -> None:
    rows = _read_csv(summary_csv)
    if not rows:
        raise ValueError('summary CSV is empty')
    by_order: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_order[int(row['source_order_k'])].append(row)
    ideal_h = float(rows[0]['ideal_min_entropy'])
    fig, ax = plt.subplots()
    _style_axis(ax)
    orders = sorted(by_order)
    for index, order in enumerate(orders):
        group = sorted(by_order[order], key=lambda r: int(r['train_samples']))
        x = [int(r['train_samples']) for r in group]
        y = [float(r['accessible_min_entropy_mean']) for r in group]
        yerr = [float(r['accessible_min_entropy_std']) for r in group]
        oracle = [float(r['oracle_coverage_min_entropy_mean']) for r in group]
        color_index = round(index * (len(PALETTE) - 1) / max(len(orders) - 1, 1))
        color = PALETTE[color_index]
        marker = MARKERS[index % len(MARKERS)]
        ax.errorbar(x, y, yerr=yerr, marker=marker, markersize=4.4, linewidth=1.7, markeredgecolor='black', markeredgewidth=0.45, color=color, capsize=2.5, capthick=1.0, elinewidth=1.0, label=f'k={order}', zorder=3)
        ax.plot(x, oracle, linestyle='--', linewidth=1.1, color=color, alpha=0.72)
    ax.axhline(1.0, color=COLORS['dark'], linestyle=':', linewidth=1.3, label='chance')
    ax.axhline(ideal_h, color=COLORS['grey'], linestyle='--', linewidth=1.4, label='ideal')
    ax.set_xscale('log')
    ax.set_xlabel('Training samples N')
    ax.set_ylabel('Accessible min-entropy')
    ax.set_title('Sample scaling for noisy lookup rules')
    ax.set_ylim(0.08, 1.06)
    ax.legend(ncols=2, frameon=True, fancybox=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

def plot_sample_thresholds(threshold_csv: Path, out_path: Path, fit: dict[str, object] | None=None) -> None:
    rows = _read_csv(threshold_csv)
    if not rows:
        raise ValueError('threshold CSV is empty')
    learned = [row for row in rows if int(row['learned']) == 1]
    missing = [row for row in rows if int(row['learned']) == 0]
    fig, ax = plt.subplots(figsize=(4.6, 3.6))
    _style_axis(ax)
    if learned:
        x = [float(row['table_size']) for row in learned]
        y = [float(row['required_samples']) for row in learned]
        y_theory = [float(row['oracle_coverage_required_samples']) for row in learned]
        ax.plot(x, y, marker='o', markersize=5.2, linewidth=1.9, markeredgecolor='black', markeredgewidth=0.5, color=COLORS['cyan'], label=slope_label('majority learner', fit or {}), zorder=3)
        ax.plot(x, y_theory, marker='s', markersize=4.6, linewidth=1.4, linestyle='--', markeredgecolor='black', markeredgewidth=0.45, color=COLORS['green'], label='coverage bound', zorder=2)
    if missing:
        x_missing = [float(row['table_size']) for row in missing]
        y_floor = min((float(row['oracle_coverage_required_samples']) for row in rows))
        ax.scatter(x_missing, [y_floor] * len(x_missing), marker='x', color=PALETTE[-1], label='not reached', zorder=4)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Lookup table entries 2^k')
    ax.set_ylabel('Required training samples')
    ax.set_title('Samples required within epsilon of ideal')
    ax.legend(frameon=True, fancybox=True)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
