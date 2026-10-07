from __future__ import annotations
import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Any

def write_json(path: Path, payload: dict[str, Any]) -> None:
    with path.open('w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2, sort_keys=True)
        f.write('\n')

def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def summarize(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[int(row['source_order_k']), int(row['model_degree_D'])].append(row)
    summary = []
    for (order, degree), group in sorted(grouped.items()):
        values = {key: [float(row[key]) for row in group] for key in ['raw_accuracy', 'p_ml', 'accessible_min_entropy', 'entropy_gap']}
        first = group[0]
        item = {'source_family': first['source_family'], 'source_order_k': order, 'model_family': first['model_family'], 'model_degree_D': degree, 'model_budget_B': first['model_budget_B'], 'contains_rule': first['contains_rule'], 'p': first['p'], 'delta': first['delta'], 'train_samples': first['train_samples'], 'test_samples': first['test_samples'], 'seeds': len(group), 'ideal_min_entropy': first['ideal_min_entropy']}
        for key, vals in values.items():
            item[f'{key}_mean'] = mean(vals)
            item[f'{key}_std'] = stdev(vals) if len(vals) > 1 else 0.0
        summary.append(item)
    return summary
