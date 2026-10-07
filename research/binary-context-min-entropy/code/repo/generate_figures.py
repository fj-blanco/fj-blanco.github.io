from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from gbar import two_run_rate

def save(fig: plt.Figure, output: Path, stem: str) -> None:
    fig.savefig(output / f'{stem}.pdf', bbox_inches='tight')
    fig.savefig(output / f'{stem}.png', dpi=240, bbox_inches='tight')
    plt.close(fig)

def order_two_phase_diagram(output: Path) -> None:
    a = np.linspace(0.0, 1.0, 1200)
    upper = 1.0 - a
    boundary = a * (a + 1.0) / (a + 2.0)
    active = boundary < upper
    fig, ax = plt.subplots(figsize=(6.2, 5.0))
    ax.fill_between(a, 0.0, np.minimum(boundary, upper), alpha=0.22, label='Period-2 alternating cycle')
    ax.fill_between(a, boundary, upper, where=active, alpha=0.22, label='Period-4 cycle')
    ax.plot(a[active], boundary[active], linewidth=2.0, label='$\\gamma_2=\\gamma_1(\\gamma_1+1)/(\\gamma_1+2)$')
    ax.plot(a, upper, linewidth=1.2)
    ax.text(0.77, 0.245, '$\\gamma_1+\\gamma_2=1$', rotation=-45, ha='center', va='center')
    ax.set(xlim=(0.0, 1.0), ylim=(0.0, 1.0), xlabel='Lag-1 magnitude $\\gamma_1$', ylabel='Lag-2 magnitude $\\gamma_2$')
    ax.set_aspect('equal', adjustable='box')
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, loc='upper right')
    save(fig, output, 'order_two_phase_diagram')

def first_crossing(x: np.ndarray, y: np.ndarray) -> float | None:
    indices = np.flatnonzero(np.signbit(y[:-1]) != np.signbit(y[1:]))
    if len(indices) == 0:
        return None
    index = int(indices[0])
    return float(x[index] - y[index] * (x[index + 1] - x[index]) / (y[index + 1] - y[index]))

def two_run_plot(output: Path, p: int) -> None:
    alpha = np.linspace(0.0001, 0.99, 1500)
    run_lengths = list(range(p // 2 + 1, p + 1))
    branches = np.array([[two_run_rate(p, run_length, value) for value in alpha] for run_length in run_lengths])
    envelope = branches.min(axis=0)
    optimizer = branches.argmin(axis=0)
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    for index, run_length in enumerate(run_lengths):
        ax.plot(alpha, branches[index], linewidth=1.1, alpha=0.75, label=f'$R={run_length}$')
    ax.plot(alpha, envelope, linewidth=3.0, color='black', label='Lower envelope')
    for index in np.flatnonzero(optimizer[1:] != optimizer[:-1]):
        left = int(optimizer[index])
        right = int(optimizer[index + 1])
        crossing = first_crossing(alpha, branches[left] - branches[right])
        if crossing is not None:
            height = np.interp(crossing, alpha, envelope)
            ax.axvline(crossing, linestyle='--', linewidth=1.0, color='black', alpha=0.55)
            ax.text(crossing, height, f'  $\\alpha\\simeq{crossing:.3f}$', rotation=90, va='bottom', ha='left', fontsize=8)
    ax.set(xlim=(0.0, 0.99), xlabel='Structured weight $\\alpha$', ylabel='Candidate rate $H_{p,R}(\\alpha)$ [bits]')
    ax.grid(alpha=0.25)
    ax.legend(frameon=False, ncol=2)
    save(fig, output, f'two_run_envelope_p{p}')

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=Path('figures'))
    parser.add_argument('--order', type=int, default=12)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    order_two_phase_diagram(args.output_dir)
    two_run_plot(args.output_dir, args.order)
if __name__ == '__main__':
    main()
