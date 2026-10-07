from __future__ import annotations
import math
from typing import Any
import numpy as np

def first_within_epsilon(rows: list[dict[str, Any]], *, size_key: str, ideal_key: str, observed_key: str, epsilon: float) -> dict[str, Any] | None:
    for row in sorted(rows, key=lambda item: float(item[size_key])):
        gap = abs(float(row[observed_key]) - float(row[ideal_key]))
        if gap <= epsilon:
            return row
    return None

def fit_power_law(rows: list[dict[str, Any]], *, x_key: str, y_key: str, learned_key: str='learned', label: str='') -> dict[str, Any]:
    learned = [row for row in rows if int(row.get(learned_key, 1)) == 1 and str(row.get(x_key, '')) != '' and (str(row.get(y_key, '')) != '') and (float(row[x_key]) > 0.0) and (float(row[y_key]) > 0.0)]
    if len(learned) < 2:
        return {'fit_available': False, 'label': label, 'x_key': x_key, 'y_key': y_key, 'n_points': len(learned)}
    x = np.log([float(row[x_key]) for row in learned])
    y = np.log([float(row[y_key]) for row in learned])
    design = np.column_stack([np.ones_like(x), x])
    intercept, slope = np.linalg.lstsq(design, y, rcond=None)[0]
    y_hat = intercept + slope * x
    residuals = y - y_hat
    sst = float(np.sum((y - np.mean(y)) ** 2))
    sse = float(np.sum(residuals ** 2))
    r_squared = 1.0 - sse / sst if sst > 0.0 else 1.0
    fit: dict[str, Any] = {'fit_available': True, 'label': label, 'x_key': x_key, 'y_key': y_key, 'n_points': len(learned), 'loglog_slope': float(slope), 'loglog_intercept': float(intercept), 'r_squared': r_squared}
    if len(learned) > 2:
        sxx = float(np.sum((x - np.mean(x)) ** 2))
        sigma2 = sse / (len(learned) - 2)
        fit['slope_standard_error'] = float(math.sqrt(sigma2 / sxx)) if sxx > 0 else 0.0
    return fit

def slope_label(base: str, fit: dict[str, Any]) -> str:
    if not fit.get('fit_available'):
        return base
    slope = float(fit['loglog_slope'])
    if 'slope_standard_error' in fit:
        return f"{base}, slope={slope:.2f}+/-{float(fit['slope_standard_error']):.2f}"
    return f'{base}, slope={slope:.2f}'
