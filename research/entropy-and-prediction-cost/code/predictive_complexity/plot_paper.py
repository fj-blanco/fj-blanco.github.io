from __future__ import annotations
import argparse
import csv
import json
import math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.ticker import ScalarFormatter
import numpy as np
INK = '#1F2D3A'
TEAL = '#16877C'
ORANGE = '#C8692B'
PURPLE = '#6A55A0'
GRID = '#E6EBEE'
COLORS = {'copy': TEAL, 'parity': ORANGE, 'lookup': PURPLE}
LABELS = {'copy': 'Delayed copy', 'parity': 'Parity feedback', 'lookup': 'Random feedback'}
MARKERS = {'copy': 'o', 'parity': 's', 'lookup': '^'}
COLUMN = 3.375
PAGE = 7.0

def read_rows(path: Path) -> list[dict]:
    with path.open(newline='') as handle:
        return list(csv.DictReader(handle))

def column(rows: list[dict], name: str) -> np.ndarray:
    return np.array([float(row[name]) for row in rows])

def style() -> None:
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['cmr10', 'DejaVu Serif'], 'mathtext.fontset': 'cm', 'axes.formatter.use_mathtext': True, 'axes.unicode_minus': True, 'font.size': 8, 'axes.titlesize': 8, 'axes.labelsize': 8, 'xtick.labelsize': 7, 'ytick.labelsize': 7, 'legend.fontsize': 7, 'text.color': INK, 'axes.labelcolor': INK, 'xtick.color': INK, 'ytick.color': INK, 'axes.edgecolor': '#8C9AA4', 'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6, 'xtick.minor.width': 0.4, 'ytick.minor.width': 0.4, 'xtick.major.size': 2.5, 'ytick.major.size': 2.5, 'xtick.minor.size': 1.5, 'ytick.minor.size': 1.5, 'axes.spines.top': False, 'axes.spines.right': False, 'legend.frameon': False, 'legend.handlelength': 1.8, 'lines.linewidth': 1.2, 'lines.markersize': 3.5, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'savefig.facecolor': 'white', 'savefig.dpi': 300})

def finish(fig: plt.Figure, out: Path, name: str) -> None:
    fig.savefig(out / (name + '.pdf'), bbox_inches='tight', pad_inches=0.02)
    fig.savefig(out / (name + '.png'), dpi=300, bbox_inches='tight', pad_inches=0.02)
    plt.close(fig)

def panel(ax: plt.Axes, label: str, title: str='') -> None:
    text = f'({label})' + (f' {title}' if title else '')
    ax.set_title(text, loc='left', pad=4, fontsize=8)

def entropy_profiles(data: Path, out: Path) -> None:
    arrays = np.load(data / 'spectra.npz')
    rows = read_rows(data / 'spectra.csv')
    fig = plt.figure(figsize=(PAGE, 3.75), layout='constrained')
    fig.get_layout_engine().set(h_pad=0.03, w_pad=0.03, hspace=0.06, wspace=0.04)
    gs = fig.add_gridspec(2, 6, height_ratios=[1, 1.0])
    top = []
    cmap = 'viridis'
    for i, family in enumerate(COLORS):
        ax = fig.add_subplot(gs[0, 2 * i:2 * i + 2])
        probabilities = arrays[family + '_probabilities'].reshape(32, 32)
        im = ax.imshow(probabilities, cmap=cmap, norm=LogNorm(1e-07, 0.02), origin='lower', aspect='equal', interpolation='nearest')
        panel(ax, chr(97 + i), LABELS[family])
        ax.set_xticks([0, 31], ['00000', '11111'])
        ax.set_yticks([0, 31], ['00000', '11111'])
        ax.set_xlabel('Next five bits', labelpad=1)
        if i == 0:
            ax.set_ylabel('First five bits', labelpad=1)
        else:
            ax.set_yticklabels([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        top.append(ax)
    cb = fig.colorbar(im, ax=top, fraction=0.03, pad=0.015, shrink=0.9)
    cb.set_label('Word probability', fontsize=7)
    cb.set_ticks([1e-06, 0.0001, 0.01])
    cb.ax.tick_params(labelsize=6.5)
    cb.outline.set_linewidth(0.4)
    ax = fig.add_subplot(gs[1, :3])
    for family, linestyle in zip(COLORS, ('-', (0, (4, 2)), (0, (1, 1.5)))):
        probabilities = np.sort(arrays[family + '_probabilities'])[::-1]
        ax.plot(np.arange(1, 1025), probabilities, color=COLORS[family], ls=linestyle, label=LABELS[family], lw=1.5)
    ax.set_yscale('log')
    ax.set_xlabel('Word rank')
    ax.set_ylabel('Probability')
    ax.set_xlim(0, 1024)
    ax.set_ylim(1e-07, 0.05)
    panel(ax, 'd', 'Sorted probabilities, $n=10$')
    ax.legend(loc='upper right')
    ax.grid(axis='y', color=GRID, lw=0.5)
    ax = fig.add_subplot(gs[1, 3:])
    for alpha, color, label in (('1.0', INK, '$H_1$'), ('2.0', TEAL, '$H_2$'), ('inf', ORANGE, '$H_\\infty$')):
        selected = [r for r in rows if r['family'] == 'copy' and r['alpha'] == alpha]
        ax.plot(column(selected, 'n'), column(selected, 'formula'), color=color, label=label, lw=1.1)
        for offset, family in enumerate(COLORS):
            chosen = [r for r in rows if r['family'] == family and r['alpha'] == alpha][offset::3]
            ax.scatter(column(chosen, 'n'), column(chosen, 'entropy'), facecolor='white', edgecolor=color, marker=MARKERS[family], s=13, lw=0.8, zorder=3)
    ax.axvline(5, color='#AAB7BE', lw=0.7, ls='--')
    ax.text(5.3, 0.6, '$n=p$', color='#5B6B78', fontsize=7)
    ax.set_xlabel('Block length $n$')
    ax.set_ylabel('Block entropy (bits)')
    ax.set_xlim(0.5, 16.5)
    ax.set_xticks([1, 4, 8, 12, 16])
    ax.set_ylim(0, 11)
    panel(ax, 'e', 'Block entropies')
    handles, labels = ax.get_legend_handles_labels()
    from matplotlib.lines import Line2D
    handles += [Line2D([], [], ls='', marker=MARKERS[f], mfc='white', mec='#5B6B78', mew=0.8, ms=4) for f in COLORS]
    labels += ['copy', 'parity', 'random']
    ax.legend(handles, labels, loc='upper left', ncol=2, columnspacing=1.0)
    ax.grid(axis='y', color=GRID, lw=0.5)
    finish(fig, out, 'fig_entropy_profiles')

def prediction_cost(data: Path, out: Path, config: dict) -> None:
    rows = read_rows(data / 'capacity_summary.csv')
    fig, ax = plt.subplots(figsize=(COLUMN, 2.35), layout='constrained')
    ideal = -math.log2(1 - config['delta'])
    ax.axhline(1, color='#AAB7BE', lw=0.7, ls=':')
    ax.axhline(ideal, color=INK, lw=0.7, ls=':')
    for family in ('lookup', 'parity', 'copy'):
        selected = sorted([r for r in rows if r['family'] == family], key=lambda r: int(r['terms']))
        x = column(selected, 'terms')
        mean = column(selected, 'guessing_power_mean')
        half = 1.96 * column(selected, 'guessing_power_sem')
        filled = family != 'parity'
        ax.plot(x, -np.log2(mean), color=COLORS[family], marker=MARKERS[family], mfc=COLORS[family] if filled else 'white', mew=0.8, ms=3.2 if family != 'copy' else 2.6, lw=1.1, label=LABELS[family], zorder=4 if family == 'copy' else 3)
        ax.fill_between(x, -np.log2(np.minimum(1, mean + half)), -np.log2(np.maximum(1e-10, mean - half)), color=COLORS[family], alpha=0.18, linewidth=0)
        if family == 'lookup':
            known = column(selected, 'known_rule_power_mean')
            ax.plot(x, -np.log2(known), color=COLORS[family], ls=(0, (3, 1.6)), lw=0.9, label='Random, rule known', zorder=2)
    ax.set_xscale('log', base=2)
    ax.set_xticks([1, 4, 16, 64, 256])
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.set_xlabel('Retained Walsh terms $q$')
    ax.set_ylabel('Attack score $-\\log_2 \\overline{G}$ (bits)')
    ax.set_ylim(0.08, 1.05)
    ax.set_xlim(0.8, 640)
    ax.text(1.0, 0.985, 'chance', fontsize=6.5, color='#5B6B78', va='top')
    ax.text(1.0, ideal + 0.025, 'Bayes value $h_\\infty(\\delta)$', fontsize=6.5, color=INK)
    handles, labels = ax.get_legend_handles_labels()
    order = [labels.index(k) for k in ('Delayed copy', 'Parity feedback', 'Random feedback', 'Random, rule known')]
    ax.legend([handles[i] for i in order], [labels[i] for i in order], loc='upper right', bbox_to_anchor=(1.0, 0.93))
    ax.grid(axis='y', color=GRID, lw=0.5)
    finish(fig, out, 'fig_prediction_cost')

def estimation_gap(data: Path, out: Path, config: dict) -> None:
    rows = read_rows(data / 'estimation_summary.csv')
    theory = read_rows(data / 'estimation_theory.csv')
    sizes = sorted({int(r['m']) for r in rows})
    delta = config['delta']
    ideal = -math.log2(1 - delta)
    chosen_m = sizes[-1]
    selected = sorted([r for r in rows if int(r['m']) == chosen_m], key=lambda r: int(r['n']))
    reference = sorted([r for r in theory if int(r['m']) == chosen_m], key=lambda r: int(r['n']))
    fig = plt.figure(figsize=(PAGE, 2.45), layout='constrained')
    fig.get_layout_engine().set(w_pad=0.03, wspace=0.03)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.6, 1, 1])
    ax = fig.add_subplot(gs[0, 0])
    x = column(selected, 'n')
    mean = column(selected, 'estimate_mean')
    half = 1.96 * column(selected, 'estimate_sem')
    ax.plot(x, mean, color=TEAL, marker='o', ms=2.4, label='Estimate $\\widehat{h}_\\infty$')
    ax.fill_between(x, np.maximum(0, mean - half), np.minimum(1, mean + half), color=TEAL, alpha=0.2, linewidth=0)
    prediction = column(selected, 'prediction_power_mean')
    half_p = 1.96 * column(selected, 'prediction_power_sem')
    ax.plot(x, -np.log2(prediction), color=PURPLE, marker='s', ms=2.4, label='Majority score')
    ax.fill_between(x, -np.log2(prediction + half_p), -np.log2(prediction - half_p), color=PURPLE, alpha=0.2, linewidth=0)
    ax.plot(column(reference, 'n'), -np.log2(column(reference, 'coverage_power')), color=PURPLE, ls='--', lw=0.8, alpha=0.75, label='Coverage bound')
    ax.axhline(ideal, color=INK, lw=0.7, ls=':')
    ax.text(2 ** 4, ideal + 0.03, '$h_\\infty(\\delta)$', fontsize=7)
    ax.set_xscale('log', base=2)
    ax.set_xticks([2 ** k for k in range(4, int(math.log2(max(x))) + 1, 3)])
    ax.set_ylim(0, 1.06)
    ax.set_ylabel('Bits')
    ax.set_xlabel('Observations $N$')
    panel(ax, 'a', f'$M=2^{{{int(math.log2(chosen_m))}}}$')
    ax.legend(loc='lower left', bbox_to_anchor=(0.385, 0.21), handlelength=1.4, borderaxespad=0.2, fontsize=6.5)
    ax.grid(axis='y', color=GRID, lw=0.5)
    axes = [fig.add_subplot(gs[0, i]) for i in (1, 2)]
    palette = ['#B9C9D3', '#7FA7B8', '#4A8BA0', '#256A84', '#14395A']
    for m, color in zip(sizes, palette[-len(sizes):]):
        selected = sorted([r for r in rows if int(r['m']) == m], key=lambda r: int(r['n']))
        sparse = [r for r in selected if int(r['n']) <= m]
        axes[0].plot(column(sparse, 'n') / math.sqrt(m), np.sqrt(column(sparse, 'squared_error_mean')), color=color, marker='o', ms=1.8, lw=0.9, label=f'$2^{{{int(math.log2(m))}}}$')
        axes[1].plot(column(selected, 'n') / m, column(selected, 'recovered_advantage_mean'), color=color, marker='o', ms=1.8, lw=0.9)
    reference = sorted([r for r in theory if int(r['m']) == max(sizes)], key=lambda r: int(r['n']))
    axes[1].plot(column(reference, 'n') / max(sizes), (column(reference, 'majority_power') - 0.5) / (0.5 - delta), color=ORANGE, ls='--', lw=1.1, label='Exact majority reference')
    axes[0].set_xscale('log')
    axes[0].set_yscale('log')
    axes[0].set_xlim(0.25, 260)
    axes[0].set_ylim(0.002, 1.2)
    axes[0].set_xlabel('$N/\\sqrt{M}$')
    axes[0].set_ylabel('RMSE of estimate (bits)')
    axes[0].legend(title='$M$', title_fontsize=7, ncol=2, loc='lower left', columnspacing=0.8, handlelength=1.4)
    panel(axes[0], 'b', 'Estimation')
    axes[1].set_xscale('log')
    axes[1].set_xlim(0.002, 9)
    axes[1].set_ylim(-0.03, 1.04)
    axes[1].set_xlabel('$N/M$')
    axes[1].set_ylabel('Recovered advantage $(\\overline{G}-\\frac{1}{2})/\\gamma$')
    axes[1].legend(loc='upper left')
    panel(axes[1], 'c', 'Prediction')
    for a in axes:
        a.grid(axis='y', color=GRID, lw=0.5)
    finish(fig, out, 'fig_estimation_gap')

def write_numbers(data: Path) -> None:
    config = json.loads((data / 'config.json').read_text())
    rows = read_rows(data / 'estimation_summary.csv')
    reference = read_rows(data / 'estimation_theory.csv')
    m = 1 << max(config['estimation']['orders'])
    n = int(32 * math.sqrt(m))
    row = min((r for r in rows if int(r['m']) == m), key=lambda r: abs(int(r['n']) - n))
    ref = next((r for r in reference if r['m'] == row['m'] and r['n'] == row['n']))
    capacity = read_rows(data / 'capacity_summary.csv')
    random_one = next((r for r in capacity if r['family'] == 'lookup' and int(r['terms']) == 1))
    random_64 = next((r for r in capacity if r['family'] == 'lookup' and int(r['terms']) == 64))
    numbers = {'ExampleContexts': str(m), 'ExampleSamples': row['n'], 'ExampleEstimate': f"{float(row['estimate_mean']):.4f}", 'ExampleRMSE': f"{math.sqrt(float(row['squared_error_mean'])):.4f}", 'ExamplePrediction': f"{float(row['prediction_power_mean']):.4f}", 'ExampleCoverage': f"{float(ref['coverage_power']):.4f}", 'RandomOnePower': f"{float(random_one['guessing_power_mean']):.4f}", 'RandomLearnedSixtyFour': f"{float(random_64['guessing_power_mean']):.3f}", 'RandomKnownSixtyFour': f"{float(random_64['known_rule_power_mean']):.3f}", 'ExactSpectrumError': f"{config['spectra']['maximum_absolute_entropy_error']:.1e}", 'TrajectoryRMS': f"{config['capacity']['trajectory_minus_exact_rms']:.4f}"}
    production_data = Path(__file__).resolve().parents[1] / 'paper' / 'data'
    if data.resolve() != production_data.resolve():
        return
    manuscript = production_data.parent / 'main.tex'
    if not manuscript.exists():
        (production_data / 'numbers.json').write_text(json.dumps(numbers, indent=2) + '\n')
        return
    lines = manuscript.read_text().splitlines()
    for name, value in numbers.items():
        prefix = '\\newcommand{\\' + name + '}{'
        matches = [i for i, line in enumerate(lines) if line.startswith(prefix)]
        if len(matches) != 1:
            raise ValueError(f'Expected one inline definition of {name} in {manuscript}')
        lines[matches[0]] = prefix + value + '}'
    manuscript.write_text('\n'.join(lines) + '\n')

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('paper/data'))
    parser.add_argument('--out', type=Path, default=Path('paper/figures'))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    style()
    config = json.loads((args.data / 'config.json').read_text())
    entropy_profiles(args.data, args.out)
    prediction_cost(args.data, args.out, config)
    estimation_gap(args.data, args.out, config)
    write_numbers(args.data)
    print(f'Three PDF/PNG figures written to {args.out}')
if __name__ == '__main__':
    main()
