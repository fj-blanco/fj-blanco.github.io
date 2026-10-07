from __future__ import annotations
from dataclasses import dataclass
from typing import Callable
import numpy as np

def mlp_parameter_count(p: int, hidden_width: int, hidden_layers: int) -> int:
    if hidden_width <= 0:
        raise ValueError('hidden_width must be positive')
    if hidden_layers <= 0:
        raise ValueError('hidden_layers must be positive')
    count = p * hidden_width + hidden_width
    count += (hidden_layers - 1) * (hidden_width * hidden_width + hidden_width)
    count += hidden_width + 1
    return count

@dataclass
class MLPTrainingResult:
    model: 'NumpyMLP'
    final_loss: float
    train_accuracy: float

class NumpyMLP:

    def __init__(self, input_dim: int, hidden_width: int, hidden_layers: int, rng: np.random.Generator, activation: str='tanh') -> None:
        if activation not in {'tanh', 'relu'}:
            raise ValueError("activation must be 'tanh' or 'relu'")
        self.input_dim = input_dim
        self.hidden_width = hidden_width
        self.hidden_layers = hidden_layers
        self.activation = activation
        dims = [input_dim] + [hidden_width] * hidden_layers + [1]
        self.weights: list[np.ndarray] = []
        self.biases: list[np.ndarray] = []
        for fan_in, fan_out in zip(dims[:-1], dims[1:]):
            scale = np.sqrt(2.0 / (fan_in + fan_out))
            self.weights.append(rng.normal(0.0, scale, size=(fan_in, fan_out)).astype(np.float32))
            self.biases.append(np.zeros(fan_out, dtype=np.float32))

    @property
    def trainable_parameters(self) -> int:
        return int(sum((weight.size for weight in self.weights)) + sum((bias.size for bias in self.biases)))

    def _activate(self, z: np.ndarray) -> np.ndarray:
        if self.activation == 'tanh':
            return np.tanh(z)
        return np.maximum(z, 0.0)

    def _activation_grad(self, z: np.ndarray, a: np.ndarray) -> np.ndarray:
        if self.activation == 'tanh':
            return 1.0 - a * a
        return (z > 0.0).astype(np.float32)

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, list[np.ndarray], list[np.ndarray]]:
        a = x.astype(np.float32, copy=False)
        activations = [a]
        preacts: list[np.ndarray] = []
        for weight, bias in zip(self.weights[:-1], self.biases[:-1]):
            z = a @ weight + bias
            a = self._activate(z)
            preacts.append(z)
            activations.append(a)
        logits = (a @ self.weights[-1] + self.biases[-1]).reshape(-1)
        return (logits, activations, preacts)

    def logits(self, x: np.ndarray, batch_size: int=4096) -> np.ndarray:
        out = np.empty(x.shape[0], dtype=np.float32)
        for start in range(0, x.shape[0], batch_size):
            end = min(start + batch_size, x.shape[0])
            out[start:end] = self.forward(x[start:end])[0]
        return out

    def predict(self, x: np.ndarray, batch_size: int=4096) -> np.ndarray:
        return np.where(self.logits(x, batch_size=batch_size) >= 0.0, 1, -1).astype(np.int8)

def _sigmoid(logits: np.ndarray) -> np.ndarray:
    out = np.empty_like(logits, dtype=np.float32)
    positive = logits >= 0
    out[positive] = 1.0 / (1.0 + np.exp(-logits[positive]))
    exp_logits = np.exp(logits[~positive])
    out[~positive] = exp_logits / (1.0 + exp_logits)
    return out

def _binary_cross_entropy(logits: np.ndarray, targets: np.ndarray) -> float:
    return float(np.mean(np.maximum(logits, 0.0) - logits * targets + np.log1p(np.exp(-np.abs(logits)))))

def _clip_gradients(grad_weights: list[np.ndarray], grad_biases: list[np.ndarray], max_norm: float) -> None:
    if max_norm <= 0:
        return
    total = 0.0
    for grad in grad_weights + grad_biases:
        total += float(np.sum(grad * grad))
    norm = total ** 0.5
    if norm <= max_norm:
        return
    scale = max_norm / (norm + 1e-12)
    for grad in grad_weights + grad_biases:
        grad *= scale

def fit_mlp_classifier(x: np.ndarray, y_pm1: np.ndarray, *, hidden_width: int, hidden_layers: int, rng: np.random.Generator, activation: str='tanh', epochs: int=300, batch_size: int=256, learning_rate: float=0.005, weight_decay: float=0.0, beta1: float=0.9, beta2: float=0.999, eps: float=1e-08, grad_clip: float=5.0, progress_callback: Callable[[int, int, float], None] | None=None) -> MLPTrainingResult:
    if epochs <= 0:
        raise ValueError('epochs must be positive')
    if batch_size <= 0:
        raise ValueError('batch_size must be positive')
    if learning_rate <= 0:
        raise ValueError('learning_rate must be positive')
    x_train = x.astype(np.float32, copy=False)
    targets = ((y_pm1.astype(np.float32) + 1.0) * 0.5).astype(np.float32)
    model = NumpyMLP(input_dim=x_train.shape[1], hidden_width=hidden_width, hidden_layers=hidden_layers, rng=rng, activation=activation)
    mw = [np.zeros_like(weight) for weight in model.weights]
    vw = [np.zeros_like(weight) for weight in model.weights]
    mb = [np.zeros_like(bias) for bias in model.biases]
    vb = [np.zeros_like(bias) for bias in model.biases]
    step = 0
    n = x_train.shape[0]
    for epoch in range(epochs):
        order = rng.permutation(n)
        epoch_loss = 0.0
        epoch_seen = 0
        for start in range(0, n, batch_size):
            step += 1
            idx = order[start:start + batch_size]
            xb = x_train[idx]
            tb = targets[idx]
            m = xb.shape[0]
            logits, activations, preacts = model.forward(xb)
            if progress_callback is not None:
                epoch_loss += _binary_cross_entropy(logits, tb) * m
                epoch_seen += m
            dlogits = (_sigmoid(logits) - tb).reshape(m, 1) / m
            grad_weights = [np.zeros_like(weight) for weight in model.weights]
            grad_biases = [np.zeros_like(bias) for bias in model.biases]
            grad_weights[-1] = activations[-1].T @ dlogits
            grad_biases[-1] = np.sum(dlogits, axis=0)
            if weight_decay:
                grad_weights[-1] += weight_decay * model.weights[-1]
            da = dlogits @ model.weights[-1].T
            for layer in range(model.hidden_layers - 1, -1, -1):
                dz = da * model._activation_grad(preacts[layer], activations[layer + 1])
                grad_weights[layer] = activations[layer].T @ dz
                grad_biases[layer] = np.sum(dz, axis=0)
                if weight_decay:
                    grad_weights[layer] += weight_decay * model.weights[layer]
                if layer > 0:
                    da = dz @ model.weights[layer].T
            _clip_gradients(grad_weights, grad_biases, grad_clip)
            for i in range(len(model.weights)):
                mw[i] = beta1 * mw[i] + (1.0 - beta1) * grad_weights[i]
                vw[i] = beta2 * vw[i] + (1.0 - beta2) * grad_weights[i] ** 2
                mb[i] = beta1 * mb[i] + (1.0 - beta1) * grad_biases[i]
                vb[i] = beta2 * vb[i] + (1.0 - beta2) * grad_biases[i] ** 2
                mw_hat = mw[i] / (1.0 - beta1 ** step)
                vw_hat = vw[i] / (1.0 - beta2 ** step)
                mb_hat = mb[i] / (1.0 - beta1 ** step)
                vb_hat = vb[i] / (1.0 - beta2 ** step)
                model.weights[i] -= learning_rate * mw_hat / (np.sqrt(vw_hat) + eps)
                model.biases[i] -= learning_rate * mb_hat / (np.sqrt(vb_hat) + eps)
        if progress_callback is not None:
            progress_callback(epoch + 1, epochs, epoch_loss / max(epoch_seen, 1))
    train_logits = model.logits(x_train)
    train_predictions = np.where(train_logits >= 0.0, 1, -1).astype(np.int8)
    train_accuracy = float(np.mean(train_predictions == y_pm1))
    final_loss = _binary_cross_entropy(train_logits, targets)
    return MLPTrainingResult(model=model, final_loss=final_loss, train_accuracy=train_accuracy)
