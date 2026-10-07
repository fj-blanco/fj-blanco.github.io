from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np

def entropy_from_power(power: float) -> float:
    if not 0 <= power <= 1:
        raise ValueError('guessing probability must be in [0, 1]')
    return -math.log2(power) if power > 0 else math.inf

def entropy_from_moment(moment: float) -> float:
    theta = min(1.0, max(0.0, moment))
    return entropy_from_power((1 + math.sqrt(theta)) / 2)

@dataclass(frozen=True)
class CollisionEstimate:
    raw_moment: float
    entropy: float
    lower: float
    upper: float
    context_pairs: int

def table_statistics(contexts: np.ndarray, labels: np.ndarray, m: int) -> tuple[np.ndarray, np.ndarray]:
    contexts = np.asarray(contexts)
    labels = np.asarray(labels)
    if m < 1 or contexts.ndim != 1 or labels.shape != contexts.shape:
        raise ValueError('invalid observations')
    if not np.issubdtype(contexts.dtype, np.integer) or np.any(contexts < 0) or np.any(contexts >= m):
        raise ValueError('contexts must be integer indices in [0, m)')
    if not np.all((labels == 0) | (labels == 1)):
        raise ValueError('labels must be bits')
    counts = np.bincount(contexts, minlength=m).astype(np.int64)
    votes = np.bincount(contexts, weights=1 - 2 * labels.astype(np.int64), minlength=m).astype(np.int64)
    return (counts, votes)

def collision_estimate(contexts: np.ndarray, labels: np.ndarray, m: int, eta: float=0.05) -> CollisionEstimate:
    n = len(contexts)
    if n < 2 or not 0 < eta < 1:
        raise ValueError('at least two observations and eta in (0, 1) are required')
    counts, votes = table_statistics(contexts, labels, m)
    raw = float(m) * float(np.sum(votes * votes - counts)) / (n * (n - 1))
    variance_bound = (2 * m + n - 2) / (n * (n - 1))
    radius = math.sqrt(variance_bound / eta)
    lower = entropy_from_moment(raw + radius)
    upper = entropy_from_moment(raw - radius)
    pairs = int(np.sum(counts * (counts - 1)) // 2)
    return CollisionEstimate(raw, entropy_from_moment(raw), lower, upper, pairs)

def moment_variance(n: int, m: int, delta: float) -> float:
    if n < 2 or m < 1 or (not 0 <= delta <= 0.5):
        raise ValueError('invalid moment-variance parameters')
    theta = (1 - 2 * delta) ** 2
    return (2 * (m - theta * theta) + 4 * (n - 2) * (theta - theta * theta)) / (n * (n - 1))

def majority_error(visits: int, delta: float) -> float:
    return sum((math.comb(visits, errors) * delta ** errors * (1 - delta) ** (visits - errors) * (1.0 if 2 * errors > visits else 0.5 if 2 * errors == visits else 0.0) for errors in range(visits + 1)))

def expected_majority_power(n: int, m: int, delta: float) -> float:
    if n < 0 or m < 2 or (not 0 <= delta < 0.5) or (n / m > 32):
        raise ValueError('requires n >= 0, m >= 2, n/m <= 32, and delta in [0, 1/2)')
    mass = math.exp(n * math.log1p(-1 / m))
    total = 0.0
    error = 0.0
    for visits in range(n + 1):
        total += mass
        error += mass * majority_error(visits, delta)
        ratio = (n - visits) / ((visits + 1) * (m - 1))
        if ratio < 1 and mass * ratio / (1 - ratio) < 1e-13:
            break
        mass *= ratio
    return 1 - delta - (1 - 2 * delta) * error

def coverage_power(n: int, m: int, delta: float) -> float:
    return 0.5 + (0.5 - delta) * -math.expm1(n * math.log1p(-1 / m))
