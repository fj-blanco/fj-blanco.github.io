from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class NoisyParitySource:
    p: int
    order: int
    delta: float
    subset: tuple[int, ...]

@dataclass(frozen=True)
class NoisyLookupSource:
    p: int
    order: int
    delta: float
    subset: tuple[int, ...]
    table: np.ndarray

def choose_subset(p: int, order: int, rng: np.random.Generator, mode: str='prefix') -> tuple[int, ...]:
    if order < 0 or order > p:
        raise ValueError('order must satisfy 0 <= order <= p')
    if mode == 'prefix':
        return tuple(range(order))
    if mode == 'random':
        return tuple(sorted(rng.choice(p, size=order, replace=False).tolist()))
    raise ValueError("subset mode must be either 'prefix' or 'random'")

def sample_noisy_parity(n: int, p: int, order: int, delta: float, rng: np.random.Generator, subset: tuple[int, ...] | None=None, subset_mode: str='prefix') -> tuple[np.ndarray, np.ndarray, NoisyParitySource]:
    if not 0 <= delta < 0.5:
        raise ValueError('delta must satisfy 0 <= delta < 0.5')
    if subset is None:
        subset = choose_subset(p, order, rng, subset_mode)
    x = rng.choice(np.array([-1, 1], dtype=np.int8), size=(n, p))
    if order == 0:
        clean = np.ones(n, dtype=np.int8)
    else:
        clean = np.prod(x[:, subset], axis=1, dtype=np.int8)
    flips = rng.random(n) < delta
    y = clean.copy()
    y[flips] *= -1
    return (x, y, NoisyParitySource(p=p, order=order, delta=delta, subset=subset))

def lookup_indices(x: np.ndarray, subset: tuple[int, ...]) -> np.ndarray:
    if not subset:
        return np.zeros(x.shape[0], dtype=np.int64)
    bits = (x[:, subset] > 0).astype(np.int64)
    powers = (1 << np.arange(len(subset), dtype=np.int64)).reshape(1, -1)
    return np.sum(bits * powers, axis=1)

def sample_noisy_lookup(n: int, p: int, order: int, delta: float, rng: np.random.Generator, subset: tuple[int, ...] | None=None, table: np.ndarray | None=None, subset_mode: str='prefix') -> tuple[np.ndarray, np.ndarray, NoisyLookupSource]:
    if not 0 <= delta < 0.5:
        raise ValueError('delta must satisfy 0 <= delta < 0.5')
    if subset is None:
        subset = choose_subset(p, order, rng, subset_mode)
    table_size = 2 ** order
    if table is None:
        table = rng.choice(np.array([-1, 1], dtype=np.int8), size=table_size)
    table = table.astype(np.int8, copy=False)
    if table.shape != (table_size,):
        raise ValueError('lookup table has incompatible size')
    x = rng.choice(np.array([-1, 1], dtype=np.int8), size=(n, p))
    clean = table[lookup_indices(x, subset)]
    flips = rng.random(n) < delta
    y = clean.copy()
    y[flips] *= -1
    source = NoisyLookupSource(p=p, order=order, delta=delta, subset=subset, table=table.copy())
    return (x, y, source)
