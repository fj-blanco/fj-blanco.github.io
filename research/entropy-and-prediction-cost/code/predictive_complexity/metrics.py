from __future__ import annotations
import math
import numpy as np

def ideal_min_entropy(delta: float) -> float:
    if not 0 <= delta <= 0.5:
        raise ValueError('delta must be in [0, 1/2]')
    return -math.log2(1.0 - delta)

def min_entropy_from_guessing_power(p_guess: float) -> float:
    p_guess = float(p_guess)
    if not 0 <= p_guess <= 1:
        raise ValueError('guessing probability must be in [0, 1]')
    return -math.log2(p_guess) if p_guess > 0 else math.inf

def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray, delta: float) -> dict[str, float]:
    y_true, y_pred = (np.asarray(y_true), np.asarray(y_pred))
    if y_true.ndim != 1 or y_true.size == 0 or y_pred.shape != y_true.shape:
        raise ValueError('expected nonempty, equally sized label vectors')
    accuracy = float(np.mean(y_true == y_pred))
    h_accessible = min_entropy_from_guessing_power(accuracy)
    h_ideal = ideal_min_entropy(delta)
    return {'raw_accuracy': accuracy, 'p_ml': accuracy, 'accessible_min_entropy': h_accessible, 'ideal_min_entropy': h_ideal, 'entropy_gap': h_accessible - h_ideal}
