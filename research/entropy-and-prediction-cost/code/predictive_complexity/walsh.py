from __future__ import annotations
from functools import lru_cache
from itertools import combinations
from math import comb
import numpy as np

def model_budget(p: int, degree: int) -> int:
    degree = min(degree, p)
    return sum((comb(p, j) for j in range(degree + 1)))

@lru_cache(maxsize=None)
def combinations_up_to_degree(p: int, degree: int) -> tuple[tuple[int, ...], ...]:
    if degree < 0:
        raise ValueError('degree must be non-negative')
    degree = min(degree, p)
    terms: list[tuple[int, ...]] = [()]
    for d in range(1, degree + 1):
        terms.extend(combinations(range(p), d))
    return tuple(terms)

def walsh_features(x: np.ndarray, terms: tuple[tuple[int, ...], ...], dtype: np.dtype=np.float32) -> np.ndarray:
    n = x.shape[0]
    phi = np.empty((n, len(terms)), dtype=dtype)
    phi[:, 0] = 1.0
    for j, term in enumerate(terms[1:], start=1):
        phi[:, j] = np.prod(x[:, term], axis=1, dtype=np.int8)
    return phi

def iter_batches(n: int, batch_size: int):
    for start in range(0, n, batch_size):
        yield (start, min(start + batch_size, n))
