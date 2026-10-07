from pathlib import Path
from itertools import product
import json
import math
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
(ROOT / 'checks').mkdir(exist_ok=True)
rng = np.random.default_rng(20261005)
I = np.eye(2)
X = np.array([[0.0, 1.0], [1.0, 0.0]])
Z = np.diag([1.0, -1.0])
P = (I - Z) / 2
PM = (I - X) / 2

def tensor(*a):
    out = np.array([[1.0]])
    for b in a:
        out = np.kron(out, b)
    return out

def squarefree_part(v):
    result = 1
    p = 2
    while p * p <= v:
        parity = 0
        while v % p == 0:
            parity ^= 1
            v //= p
        if parity:
            result *= p
        p = 3 if p == 2 else p + 2
    return result * v

def check_squarefree():
    records = []
    for n in range(1, 8):
        m = n + 1
        M = 4 ** m
        ds = [squarefree_part(M * M + s * s) for s in range(2 ** m)]
        assert len(set(ds)) == len(ds) and ds[0] == 1
        width = 2 * math.sqrt(1 + ((2 ** m - 1) / M) ** 2)
        assert width < 3
        records.append({'n': n, 'blocks': len(ds), 'distinct_squarefree_parts': len(set(ds)), 'width_over_J': width})
    return records

def check_programmed_returns():
    M = 16
    s = np.arange(4, dtype=float)
    r = np.sqrt(1 + (s / M) ** 2)
    dr = (s / M) ** 2 / (r + 1)
    eta = 0.15
    found = {}
    for start in range(1, 2000001, 50000):
        qs = np.arange(start, start + 50000)
        phases = qs[:, None] * dr[None, :]
        for f in range(4):
            if f in found:
                continue
            signs = np.array([0, 0, f & 1, f >> 1 & 1])
            errors = np.max(2 * np.abs(np.sin(np.pi * (phases - signs[None, :] / 2))), axis=1)
            hits = np.flatnonzero(errors < eta)
            if hits.size:
                j = hits[0]
                found[f] = (int(qs[j]), float(errors[j]))
        if len(found) == 4:
            break
    assert len(found) == 4, found
    H = tensor(I, I, X) + (tensor(P, I, Z) + 2 * tensor(I, PM, Z)) / M
    energies, basis = np.linalg.eigh(H)
    target_eigs = np.sort(np.concatenate([-r, r]))
    assert np.max(np.abs(energies - target_eigs)) < 1e-12
    records = []
    for f, (q, blockerror) in found.items():
        U = np.zeros((4, 4))
        for x, b in product(range(2), repeat=2):
            U[2 * x + (b ^ f >> x & 1), 2 * x + b] = 1
        evolved = basis * np.exp(-2j * np.pi * q * energies) @ basis.conj().T
        error = float(np.linalg.norm(evolved - np.kron(U, I), 2))
        assert abs(error - blockerror) < 2e-08 and error < eta
        records.append({'truth_table_integer': f, 'q': q, 'operator_norm_error': error})
    return records

def check_walsh_and_parity():
    n = 3
    m = n + 1
    labels = np.array(list(product([0, 1], repeat=m)))
    walsh = (-1.0) ** (labels @ labels.T % 2)
    maxerror = 0.0
    for f in range(2 ** 2 ** n):
        inputs = labels[:, :n] @ np.array([4, 2, 1])
        g = labels[:, n] * np.array([f >> int(x) & 1 for x in inputs])
        coeff = walsh.T @ g / 2 ** m
        phase = np.prod(np.exp(-1j * np.pi * walsh * coeff[None, :]), axis=1)
        maxerror = max(maxerror, float(np.max(np.abs(phase - (-1.0) ** g))))
    assert maxerror < 1e-12
    Y = np.array([[0, -1j], [1j, 0]])
    matrices = [I, X, Y, Z]
    minus = np.array([1.0, -1.0]) / np.sqrt(2)
    xs = list(product([0, 1], repeat=n))
    parity = np.array([(-1) ** sum(x) for x in xs])
    checked = 0
    for word in product(range(4), repeat=n + 1):
        if sum((v != 0 for v in word)) > 2:
            continue
        matrix = tensor(*(matrices[v] for v in word))
        diagonal = []
        for bits in xs:
            x = sum((b * 2 ** (n - 1 - j) for j, b in enumerate(bits)))
            state = np.kron(np.eye(2 ** n)[x], minus)
            diagonal.append(np.vdot(state, matrix @ state))
        assert abs(parity @ diagonal) < 1e-12
        checked += 1
    return {'truth_tables_checked': 256, 'walsh_max_error': maxerror, 'local_Pauli_strings_checked': checked}

def check_heralding_constants():
    smallest = 1.0
    for _ in range(10000):
        e = rng.uniform(0, 0.499)
        delta = 1 - 2 * e
        p, pp = 10 ** rng.uniform(-18, 0, 2)
        u = np.sqrt(p) * np.array([np.sqrt(1 - e), np.exp(1j * rng.uniform(0, 2 * np.pi)) * np.sqrt(e)])
        v = np.sqrt(pp) * np.array([np.sqrt(e), np.exp(1j * rng.uniform(0, 2 * np.pi)) * np.sqrt(1 - e)])
        distance = math.sqrt(max(0, float(p + pp - 2 * abs(np.vdot(u, v)))))
        lower = delta * math.sqrt((p + pp) / 2)
        assert distance >= lower * (1 - 1e-12)
        smallest = min(smallest, min(p, pp))

    def normstar(gs):
        return sum(((np.linalg.eigvalsh(g)[-1] - np.linalg.eigvalsh(g)[0]) / 2 for g in gs))
    for _ in range(1000):
        gs = []
        hs = []
        for _ in range(2):
            a = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
            b = rng.normal(size=(4, 4)) + 1j * rng.normal(size=(4, 4))
            gs.append((a + a.conj().T) * 10 ** rng.uniform(-8, 3))
            hs.append((b + b.conj().T) * 10 ** rng.uniform(-8, 3))
        aa, bb = (2 * normstar(gs), 2 * normstar(hs))
        lhs = normstar([g - h for g, h in zip(gs, hs)])
        rhs = (np.sqrt(aa) + np.sqrt(bb)) * normstar([g / np.sqrt(aa) - h / np.sqrt(bb) for g, h in zip(gs, hs)])
        assert lhs <= rhs * (1 + 1e-12)
    return {'accepted_state_pairs': 10000, 'smallest_probability': float(smallest), 'radial_norm_checks': 1000}
if __name__ == '__main__':
    report = {'seed': 20261005, 'squarefree_checks': check_squarefree(), 'one_input_qubit_returns': check_programmed_returns(), 'walsh_and_parity': check_walsh_and_parity(), 'heralding_and_radial_constants': check_heralding_constants(), 'interpretation': 'Finite numerical checks, not a substitute for the analytic proofs.'}
    (ROOT / 'checks/numerical_results.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
