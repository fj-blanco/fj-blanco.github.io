from __future__ import annotations
import importlib.util
from dataclasses import dataclass
from typing import Any, Callable
import numpy as np

def torch_import_error() -> str | None:
    if importlib.util.find_spec('torch') is None:
        return 'PyTorch is not installed'
    try:
        import torch
    except Exception as exc:
        return f'{type(exc).__name__}: {exc}'
    return None

def torch_available() -> bool:
    return torch_import_error() is None

def _import_torch() -> Any:
    try:
        import torch
    except Exception as exc:
        raise RuntimeError(f'PyTorch could not be imported. Install/fix torch in the lab environment or run with --backend numpy. Import error was: {type(exc).__name__}: {exc}') from exc
    return torch

def resolve_torch_device(requested: str) -> str:
    torch = _import_torch()
    if requested == 'auto':
        return 'cuda' if torch.cuda.is_available() else 'cpu'
    if requested.startswith('cuda') and (not torch.cuda.is_available()):
        raise RuntimeError('requested a CUDA device, but torch.cuda.is_available() is false')
    return requested

@dataclass
class TorchMLPTrainingResult:
    model: 'TorchMLP'
    final_loss: float
    train_accuracy: float

class TorchMLP:

    def __init__(self, module: Any, *, device: str, input_dim: int, hidden_width: int, hidden_layers: int, activation: str) -> None:
        self.module = module
        self.device = device
        self.input_dim = input_dim
        self.hidden_width = hidden_width
        self.hidden_layers = hidden_layers
        self.activation = activation

    @property
    def trainable_parameters(self) -> int:
        return int(sum((parameter.numel() for parameter in self.module.parameters() if parameter.requires_grad)))

    def logits(self, x: np.ndarray, batch_size: int=4096) -> np.ndarray:
        torch = _import_torch()
        self.module.eval()
        out = np.empty(x.shape[0], dtype=np.float32)
        with torch.no_grad():
            for start in range(0, x.shape[0], batch_size):
                end = min(start + batch_size, x.shape[0])
                xb = torch.as_tensor(x[start:end].astype(np.float32, copy=False), device=self.device)
                logits = self.module(xb).reshape(-1)
                out[start:end] = logits.detach().cpu().numpy()
        return out

    def predict(self, x: np.ndarray, batch_size: int=4096) -> np.ndarray:
        return np.where(self.logits(x, batch_size=batch_size) >= 0.0, 1, -1).astype(np.int8)

def _build_module(*, input_dim: int, hidden_width: int, hidden_layers: int, activation: str, seed: int, device: str) -> Any:
    torch = _import_torch()
    torch.manual_seed(seed)
    if device.startswith('cuda'):
        torch.cuda.manual_seed_all(seed)
    layers: list[Any] = []
    dims = [input_dim] + [hidden_width] * hidden_layers + [1]
    activation_cls = torch.nn.ReLU if activation == 'relu' else torch.nn.Tanh
    for layer_index, (fan_in, fan_out) in enumerate(zip(dims[:-1], dims[1:])):
        linear = torch.nn.Linear(fan_in, fan_out)
        scale = (2.0 / (fan_in + fan_out)) ** 0.5
        with torch.no_grad():
            linear.weight.normal_(0.0, scale)
            linear.bias.zero_()
        layers.append(linear)
        if layer_index < len(dims) - 2:
            layers.append(activation_cls())
    return torch.nn.Sequential(*layers).to(device)

def fit_mlp_classifier_torch(x: np.ndarray, y_pm1: np.ndarray, *, hidden_width: int, hidden_layers: int, seed: int, activation: str='tanh', epochs: int=300, batch_size: int=256, learning_rate: float=0.005, weight_decay: float=0.0, grad_clip: float=5.0, device: str='auto', deterministic: bool=False, progress_callback: Callable[[int, int, float], None] | None=None) -> TorchMLPTrainingResult:
    if activation not in {'tanh', 'relu'}:
        raise ValueError("activation must be 'tanh' or 'relu'")
    if epochs <= 0:
        raise ValueError('epochs must be positive')
    if batch_size <= 0:
        raise ValueError('batch_size must be positive')
    if learning_rate <= 0:
        raise ValueError('learning_rate must be positive')
    torch = _import_torch()
    device = resolve_torch_device(device)
    if deterministic:
        torch.use_deterministic_algorithms(True, warn_only=True)
    x_train_np = x.astype(np.float32, copy=False)
    targets_np = ((y_pm1.astype(np.float32) + 1.0) * 0.5).astype(np.float32)
    x_train = torch.as_tensor(x_train_np, device=device)
    targets = torch.as_tensor(targets_np, device=device)
    module = _build_module(input_dim=x_train.shape[1], hidden_width=hidden_width, hidden_layers=hidden_layers, activation=activation, seed=seed, device=device)
    optimizer = torch.optim.Adam(module.parameters(), lr=learning_rate, weight_decay=weight_decay)
    criterion = torch.nn.BCEWithLogitsLoss(reduction='mean')
    n = x_train.shape[0]
    for epoch in range(epochs):
        module.train()
        order = torch.randperm(n, device=device)
        loss_total = 0.0
        seen = 0
        for start in range(0, n, batch_size):
            idx = order[start:start + batch_size]
            xb = x_train[idx]
            tb = targets[idx]
            optimizer.zero_grad(set_to_none=True)
            logits = module(xb).reshape(-1)
            loss = criterion(logits, tb)
            loss.backward()
            if grad_clip > 0:
                torch.nn.utils.clip_grad_norm_(module.parameters(), grad_clip)
            optimizer.step()
            if progress_callback is not None:
                batch_n = int(xb.shape[0])
                loss_total += float(loss.detach().cpu()) * batch_n
                seen += batch_n
        if progress_callback is not None:
            mean_loss = loss_total / max(seen, 1)
            progress_callback(epoch + 1, epochs, mean_loss)
    module.eval()
    with torch.no_grad():
        train_logits = module(x_train).reshape(-1)
        final_loss = float(criterion(train_logits, targets).detach().cpu())
        train_predictions = torch.where(train_logits >= 0.0, 1, -1)
        y_train = torch.as_tensor(y_pm1.astype(np.int64, copy=False), device=device)
        train_accuracy = float((train_predictions == y_train).float().mean().detach().cpu())
    return TorchMLPTrainingResult(model=TorchMLP(module, device=device, input_dim=x_train.shape[1], hidden_width=hidden_width, hidden_layers=hidden_layers, activation=activation), final_loss=final_loss, train_accuracy=train_accuracy)
