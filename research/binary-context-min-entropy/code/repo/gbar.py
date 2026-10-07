from __future__ import annotations
from contextlib import nullcontext
from math import gcd, log2
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np

def action_costs(coefficients: list[float]) -> np.ndarray:
    p = len(coefficients)
    beta = 1.0 - sum((abs(value) for value in coefficients))
    if beta <= 0.0:
        raise ValueError('the noise weight must be positive')
    states = np.arange(1 << p, dtype=np.uint64)
    probabilities = np.full((2, len(states)), beta / 2.0)
    for lag, coefficient in enumerate(coefficients, start=1):
        if coefficient == 0.0:
            continue
        past = states >> lag - 1 & 1
        for output in (0, 1):
            satisfied = past == output if coefficient > 0 else past != output
            probabilities[output, satisfied] += abs(coefficient)
    return -np.log2(probabilities)

def karp_from_action_costs(costs: np.ndarray, workdir: Path | None=None) -> float:
    if costs.ndim != 2 or costs.shape[0] != 2:
        raise ValueError('costs must have shape (2, 2**p)')
    n = costs.shape[1]
    if n == 0 or n & n - 1:
        raise ValueError('the state count must be a power of two')
    targets = np.arange(n, dtype=np.uint64)
    predecessor_0 = targets >> 1
    predecessor_1 = predecessor_0 | n >> 1
    outputs = targets & 1
    incoming_0 = costs[outputs, predecessor_0]
    incoming_1 = costs[outputs, predecessor_1]
    temporary = TemporaryDirectory(dir=workdir) if workdir else nullcontext(None)
    with temporary as directory:
        if directory is None:
            distances = np.empty((n + 1, n), dtype=np.float64)
        else:
            filename = Path(directory) / 'karp.dat'
            distances = np.memmap(filename, mode='w+', dtype=np.float64, shape=(n + 1, n))
        distances[0] = 0.0
        for length in range(1, n + 1):
            previous = distances[length - 1]
            distances[length] = np.minimum(previous[predecessor_0] + incoming_0, previous[predecessor_1] + incoming_1)
        final = distances[n]
        maxima = np.full(n, -np.inf)
        for length in range(n):
            ratio = (final - distances[length]) / (n - length)
            np.maximum(maxima, ratio, out=maxima)
        result = float(np.min(maxima))
        del distances
    return result

def karp_min_entropy(coefficients: list[float], workdir: Path | None=None) -> float:
    return karp_from_action_costs(action_costs(coefficients), workdir)

def floor_compatible(active_lags: tuple[int, ...], signs: tuple[int, ...]) -> bool:
    divisor = 0
    for lag in active_lags:
        divisor = gcd(divisor, lag)
    return any((all((sign == q * (lag // divisor) % 2 for lag, sign in zip(active_lags, signs))) for q in (0, 1)))

def local_cost(p: int, disagreements: int, alpha: float) -> float:
    probability = (1.0 - alpha) / 2.0 + disagreements * alpha / p
    return -log2(probability)

def two_run_rate(p: int, run_length: int, alpha: float) -> float:
    total = sum((local_cost(p, m, alpha) for m in range(p - run_length + 1, run_length)))
    total += (p - run_length + 1) * local_cost(p, run_length, alpha)
    return total / run_length

def two_run_envelope(p: int, alpha: float) -> tuple[float, int]:
    candidates = [(two_run_rate(p, run_length, alpha), run_length) for run_length in range(p // 2 + 1, p + 1)]
    return min(candidates)
