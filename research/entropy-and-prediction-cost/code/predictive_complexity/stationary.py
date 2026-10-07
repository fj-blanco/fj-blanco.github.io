from __future__ import annotations
from dataclasses import dataclass
import math
import numpy as np

@dataclass(frozen=True)
class FeedbackSource:
    g: np.ndarray
    delta: float

    def __post_init__(self) -> None:
        table = np.asarray(self.g)
        if table.ndim != 1 or len(table) == 0 or len(table) & len(table) - 1:
            raise ValueError('g must have power-of-two length')
        if not np.all((table == 0) | (table == 1)):
            raise ValueError('g must contain bits')
        if not 0 < self.delta < 0.5:
            raise ValueError('stationary experiments require 0 < delta < 1/2')
        table = table.astype(np.int8, copy=True)
        table.flags.writeable = False
        object.__setattr__(self, 'g', table)

    @property
    def p(self) -> int:
        return len(self.g).bit_length()

    def bayes_bits(self, contexts: np.ndarray) -> np.ndarray:
        contexts = np.asarray(contexts, dtype=np.int64)
        return (contexts >> self.p - 1 ^ self.g[contexts & len(self.g) - 1]).astype(np.int8)

    def sample(self, n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
        if n < 1:
            raise ValueError('n must be positive')
        state = int(rng.integers(1 << self.p))
        errors = rng.random(n) < self.delta
        contexts = np.empty(n, dtype=np.int64)
        labels = np.empty(n, dtype=np.int8)
        state_mask = (1 << self.p) - 1
        suffix_mask = len(self.g) - 1
        for t in range(n):
            contexts[t] = state
            labels[t] = state >> self.p - 1 ^ int(self.g[state & suffix_mask]) ^ int(errors[t])
            state = state << 1 & state_mask | int(labels[t])
        return (contexts, labels)

    def block_probabilities(self, n: int) -> np.ndarray:
        if n < 1:
            raise ValueError('n must be positive')
        if n <= self.p:
            return np.full(1 << n, 2.0 ** (-n))
        words = np.arange(1 << n, dtype=np.int64)
        states = words >> n - self.p
        probabilities = np.full(len(words), 2.0 ** (-self.p))
        mask = (1 << self.p) - 1
        for shift in range(n - self.p - 1, -1, -1):
            bits = words >> shift & 1
            probabilities *= np.where(bits == self.bayes_bits(states), 1 - self.delta, self.delta)
            states = states << 1 & mask | bits
        return probabilities

def make_feedback(p: int, family: str, delta: float, rng: np.random.Generator) -> FeedbackSource:
    if p < 2:
        raise ValueError('the benchmark families require p >= 2')
    m = 1 << p - 1
    if family == 'copy':
        table = np.zeros(m, dtype=np.int8)
    elif family == 'parity':
        selected = rng.choice(p - 1, size=min(3, p - 1), replace=False)
        mask = sum((1 << int(j) for j in selected))
        table = np.array([(u & mask).bit_count() % 2 for u in range(m)], dtype=np.int8)
    elif family == 'lookup':
        table = rng.integers(0, 2, size=m, dtype=np.int8)
    else:
        raise ValueError(f'unknown feedback family: {family}')
    return FeedbackSource(table, delta)

def renyi_entropy(probabilities: np.ndarray, alpha: float) -> float:
    probabilities = np.asarray(probabilities, dtype=float)
    probabilities = probabilities[probabilities > 0]
    if alpha < 0:
        raise ValueError('alpha must be nonnegative')
    if alpha == 0:
        return math.log2(len(probabilities))
    if alpha == 1:
        return float(-np.sum(probabilities * np.log2(probabilities)))
    if math.isinf(alpha):
        return -math.log2(float(np.max(probabilities)))
    return float(np.log2(np.sum(probabilities ** alpha)) / (1 - alpha))

def fwht(values: np.ndarray) -> np.ndarray:
    out = np.array(values, copy=True)
    if out.ndim != 1 or len(out) == 0 or len(out) & len(out) - 1:
        raise ValueError('transform length must be a positive power of two')
    width = 1
    while width < len(out):
        blocks = out.reshape(-1, 2 * width)
        left = blocks[:, :width].copy()
        right = blocks[:, width:].copy()
        blocks[:, :width] = left + right
        blocks[:, width:] = left - right
        width *= 2
    return out

def fit_sparse_walsh(contexts: np.ndarray, labels: np.ndarray, p: int, terms: int) -> np.ndarray:
    m = 1 << p - 1
    if not 1 <= terms <= m or len(contexts) != len(labels) or len(labels) == 0:
        raise ValueError('invalid training arrays or term budget')
    residual = labels ^ contexts >> p - 1
    votes = np.bincount(contexts & m - 1, weights=1 - 2 * residual, minlength=m).astype(np.int64)
    spectrum = fwht(votes)
    selected = np.argsort(-np.abs(spectrum), kind='stable')[:terms]
    sparse = np.zeros(m, dtype=np.int64)
    sparse[selected] = spectrum[selected]
    return (fwht(sparse) < 0).astype(np.int8)

def population_guessing_power(source: FeedbackSource, predicted_g: np.ndarray) -> float:
    agreement = float(np.mean(predicted_g == source.g))
    return source.delta + (1 - 2 * source.delta) * agreement
