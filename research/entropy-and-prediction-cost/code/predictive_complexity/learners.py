from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .walsh import combinations_up_to_degree, iter_batches, model_budget, walsh_features

@dataclass
class WalshEnergyModel:
    p: int
    degree: int
    theta: np.ndarray

    @property
    def budget(self) -> int:
        return model_budget(self.p, self.degree)

    def scores(self, x: np.ndarray, batch_size: int=4096) -> np.ndarray:
        terms = combinations_up_to_degree(self.p, self.degree)
        out = np.empty(x.shape[0], dtype=np.float32)
        for start, end in iter_batches(x.shape[0], batch_size):
            phi = walsh_features(x[start:end], terms)
            out[start:end] = phi @ self.theta
        return out

    def predict(self, x: np.ndarray, batch_size: int=4096) -> np.ndarray:
        scores = self.scores(x, batch_size=batch_size)
        return np.where(scores >= 0, 1, -1).astype(np.int8)

def fit_walsh_projection(x: np.ndarray, y: np.ndarray, degree: int, batch_size: int=4096) -> WalshEnergyModel:
    p = x.shape[1]
    terms = combinations_up_to_degree(p, degree)
    theta = np.zeros(len(terms), dtype=np.float64)
    for start, end in iter_batches(x.shape[0], batch_size):
        phi = walsh_features(x[start:end], terms, dtype=np.float32)
        theta += phi.T @ y[start:end].astype(np.float32)
    theta = (theta / x.shape[0]).astype(np.float32)
    return WalshEnergyModel(p=p, degree=degree, theta=theta)
