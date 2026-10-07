from itertools import product
from pathlib import Path
import json
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'checks').mkdir(exist_ok=True)
I = np.eye(2)
X = np.array([[0.0, 1.0], [1.0, 0.0]])
Y = np.array([[0.0, -1j], [1j, 0.0]])
Z = np.diag([1.0, -1.0])
P = (I - Z) / 2
PP, PM = ((I + X) / 2, (I - X) / 2)
rng = np.random.default_rng(20261007)

def tensor(ops):
    out = np.array([[1.0]])
    for op in ops:
        out = np.kron(out, op)
    return out

def unitary(h, t):
    vals, vecs = np.linalg.eigh(h)
    return vecs * np.exp(-1j * t * vals) @ vecs.conj().T

def oracle(n, table):
    out = np.zeros((2 ** (n + 1),) * 2)
    for x in range(2 ** n):
        for b in range(2):
            out[2 * x + (b ^ table[x]), 2 * x + b] = 1
    return out

def construction():
    records = []
    for n in (1, 2, 3):
        m, M = (n + 1, 4 ** (n + 1))
        h = tensor([I] * m + [X]).astype(complex)
        for i in range(m):
            ops = [I] * m + [Z]
            ops[i] = P if i < n else PM
            h += 2 ** i / M * tensor(ops)
        had = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2)
        change = tensor([I] * n + [had, I])
        block = np.zeros_like(h)
        for bits in product((0, 1), repeat=m):
            idx = sum((b * 2 ** (m - 1 - i) for i, b in enumerate(bits)))
            sector = sum((b * 2 ** i for i, b in enumerate(bits)))
            block[2 * idx:2 * idx + 2, 2 * idx:2 * idx + 2] = X + sector / M * Z
        err = np.linalg.norm(change.conj().T @ h @ change - block, 2)
        assert err < 1e-12
        for table in product((0, 1), repeat=2 ** n):
            uf = np.kron(oracle(n, table), I)
            assert np.linalg.norm(h @ uf - uf @ h, 2) < 1e-12
        records.append({'n': n, 'block_error': float(err), 'commuting_oracles': 2 ** 2 ** n})
    n = 2
    M = 4 ** (n + 1)
    a = ((2 ** (n + 1) - 1) / M) ** 2
    shift = a / (np.sqrt(1 + a) + 1)
    error = float(2 * np.sin(np.pi * shift))
    eta = 0.1
    mean_gap = float((np.pi / (2 * np.arcsin(eta / 2))) ** (2 ** (n + 1) - 1))
    assert error < eta and mean_gap > 30000000000.0
    return {'matrix_checks': records, 'identity_counterexample': {'n': n, 'eta': eta, 'q': 1, 'operator_error': error, 'asymptotic_mean_gap': mean_gap}}

def zero_auxiliary():
    records = []
    for n in (2, 3):
        labels = np.array(list(product((0, 1), repeat=n)))
        hvals = np.sqrt([2, 3, 5, 7, 11, 13, 17, 19][:2 ** n]) / 10
        walsh = (-1.0) ** (labels @ labels.T % 2)
        coeff = walsh.T @ hvals / 2 ** n
        c = coeff[-1]
        g = np.sqrt(1 - c * c)
        h = np.zeros((2 ** (n + 1),) * 2, complex)
        for label, value in zip(labels, coeff):
            h += value * tensor([Z if b else I for b in label] + [I if np.all(label) else PM])
        h += g * tensor([X] + [I] * (n - 1) + [PP])
        plus = np.kron(np.eye(2 ** n), np.array([[1.0], [1.0]]) / np.sqrt(2))
        minus = np.kron(np.eye(2 ** n), np.array([[1.0], [-1.0]]) / np.sqrt(2))
        hp = plus.conj().T @ h @ plus
        assert np.allclose(hp @ hp, np.eye(2 ** n), atol=1e-13)
        assert np.allclose(minus.conj().T @ h @ minus, np.diag(hvals), atol=1e-13)
        maxweight = 0
        for word in product(range(4), repeat=n + 1):
            pauli = tensor([[I, X, Y, Z][w] for w in word])
            val = np.trace(pauli @ h) / 2 ** (n + 1)
            if abs(val) > 1e-12:
                maxweight = max(maxweight, sum((w != 0 for w in word)))
        assert maxweight == n
        assert np.linalg.norm(unitary(hp, 2 * np.pi) - np.eye(2 ** n), 2) < 1e-12
        records.append({'n': n, 'max_Pauli_weight': maxweight, 'plus_sector_period_error': float(np.linalg.norm(unitary(hp, 2 * np.pi) - np.eye(2 ** n), 2))})
    return records

def stability():
    ratios = []
    for _ in range(200):
        z = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
        h = (z + z.conj().T) / 2
        z = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
        e = (z + z.conj().T) * 0.001
        t = rng.uniform(0, 5)
        dt = rng.uniform(-0.01, 0.01)
        ee = np.linalg.eigvalsh(e)
        c = (ee[-1] + ee[0]) / 2
        hh = np.linalg.eigvalsh(h + e)
        center = (hh[-1] + hh[0]) / 2
        actual = np.exp(1j * (t * c + dt * center)) * unitary(h + e, t + dt)
        distance = np.linalg.norm(actual - unitary(h, t), 2)
        bound = t * (ee[-1] - ee[0]) / 2 + abs(dt) * (hh[-1] - hh[0]) / 2
        assert distance <= bound + 1e-12
        ratios.append(float(distance / bound))
    return {'cases': len(ratios), 'largest_error_to_bound_ratio': max(ratios)}
if __name__ == '__main__':
    report = {'seed': 20261007, 'construction': construction(), 'zero_auxiliary': zero_auxiliary(), 'perturbation_bound': stability(), 'interpretation': 'Finite regression checks; universality and capacity are proved analytically.'}
    (ROOT / 'checks/capacity.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
