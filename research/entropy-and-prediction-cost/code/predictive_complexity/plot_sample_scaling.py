from __future__ import annotations
import argparse
import csv
from pathlib import Path
from typing import Any
from .io import write_csv, write_json
from .plotting import plot_sample_scaling_curve, plot_sample_thresholds
from .run_sample_scaling import collect_thresholds
from .scaling import fit_power_law

def read_rows(path: Path) -> list[dict[str, Any]]:
    with path.open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Regenerate sample-scaling thresholds, slope fit, and plots.')
    parser.add_argument('--summary', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=Path('results/sample_scaling'))
    parser.add_argument('--epsilon', type=float, default=0.03)
    return parser

def main() -> None:
    parser = build_argparser()
    args = parser.parse_args()
    if args.epsilon <= 0:
        raise ValueError('epsilon must be positive')
    args.out.mkdir(parents=True, exist_ok=True)
    summary_rows = read_rows(args.summary)
    thresholds = collect_thresholds(summary_rows, epsilon=args.epsilon)
    fit = fit_power_law(thresholds, x_key='table_size', y_key='required_samples', label='sample_size_vs_lookup_table_entries')
    write_csv(args.out / 'sample_thresholds.csv', thresholds)
    write_json(args.out / 'scaling_fit.json', fit)
    write_json(args.out / 'config.json', {'epsilon_bits': args.epsilon, 'summary': str(args.summary), 'sample_thresholds': 'sample_thresholds.csv', 'scaling_fit': 'scaling_fit.json'})
    plot_sample_scaling_curve(args.summary, args.out / 'sample_scaling.png')
    plot_sample_scaling_curve(args.summary, args.out / 'sample_scaling.pdf')
    plot_sample_thresholds(args.out / 'sample_thresholds.csv', args.out / 'sample_thresholds.png', fit)
    plot_sample_thresholds(args.out / 'sample_thresholds.csv', args.out / 'sample_thresholds.pdf', fit)
if __name__ == '__main__':
    main()
