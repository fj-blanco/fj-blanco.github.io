import numpy as np
from scipy.linalg import sqrtm, logm
rng = np.random.default_rng(7)

def rand_rho(d):
    G = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    r = G @ G.conj().T
    return r / np.trace(r).real

def setup(rho):
    p, U = np.linalg.eigh(rho)
    d = len(p)
    Omega = np.zeros(d * d, complex)
    for i in range(d):
        Omega[i * d + i] = np.sqrt(p[i])
    Delta = np.kron(np.diag(p), np.diag(1 / p))
    K = -np.kron(np.diag(np.log(p)), np.eye(d)) + np.kron(np.eye(d), np.diag(np.log(p)))
    return (p, U, Omega, Delta, K)

def J_apply(v, d):
    m = v.reshape(d, d)
    return np.conj(m.T).reshape(-1)

def checks(d, sharp):
    rho = rand_rho(d)
    p, U, Omega, Delta, K = setup(rho)
    H = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    H = H + H.conj().T
    if sharp:
        w, V = np.linalg.eigh(H)
        Z0 = V @ np.diag(np.sign(w)) @ V.conj().T
        Z = Z0
    else:
        Z = H - np.trace(np.diag(p) @ H).real * np.eye(d)
        Z = Z / np.linalg.norm(Z, 2)
    Zf = np.kron(Z, np.eye(d))
    psi = Zf @ Omega
    q = np.vdot(psi, psi).real
    sqrtD = np.diag(np.sqrt(np.diag(Delta)))
    C = np.vdot(psi, sqrtD @ psi).real
    C_alt = np.vdot(psi, J_apply(psi, d)).real
    Om = Omega.reshape(d, d)
    Zm = Z @ Om
    sigma = Om.T @ Zm.conj()
    X = Om.T @ np.conj(Zm)
    X = (X + X.conj().T) / 2 if np.allclose(X, X.conj().T, atol=1e-10) else X
    dd = 0.5 * np.sum(np.abs(np.linalg.eigvalsh((X + X.conj().T) / 2)))
    kappa = np.vdot(psi, K @ psi).real / q
    out = dict(q=q, C=C, C_alt=C_alt, two_d=2 * dd, sqrtC=np.sqrt(C), kappa=kappa, jensen=q * np.exp(-kappa / 2))
    if sharp:
        rho_d = np.diag(p)
        rZ = Z @ rho_d @ Z
        S = np.trace(rZ @ (logm(rZ) - logm(rho_d))).real
        out['relent'] = S
    return out
worst = 0
for trial in range(300):
    d = rng.integers(2, 6)
    o = checks(d, sharp=False)
    assert abs(o['C'] - o['C_alt']) < 1e-10, o
    assert o['C'] <= o['two_d'] + 1e-10, o
    assert o['two_d'] <= o['sqrtC'] + 1e-10, o
    assert o['kappa'] >= -1e-12 and o['C'] >= o['jensen'] - 1e-12, o
    o = checks(d, sharp=True)
    assert abs(o['kappa'] - o['relent']) < 1e-08, o
    worst = max(worst, o['two_d'] / o['sqrtC'])
print('finite-dim checks passed; max 2d/sqrt(C) =', worst)
for b in [0.3, 1.0, 3.0, 8.0]:
    pp = 1 / (1 + np.exp(-b))
    rho = np.diag([pp, 1 - pp])
    P, U, Omega, Delta, K = setup(rho)
    Z = np.array([[0, 1], [1, 0]], complex)
    psi = np.kron(Z, np.eye(2)) @ Omega
    C = np.vdot(psi, np.sqrt(np.diag(Delta)) * psi).real
    kap = np.vdot(psi, K @ psi).real
    Om = Omega.reshape(2, 2)
    X = Om.T @ np.conj(Z @ Om)
    two_d = np.sum(np.abs(np.linalg.eigvalsh((X + X.conj().T) / 2)))
    print(f'b={b}: C={C:.6f} sech={1 / np.cosh(b / 2):.6f} kappa={kap:.6f} btanh={b * np.tanh(b / 2):.6f} 2d={two_d:.6f}')
for t in [0.01, 0.2, 0.7, 1.0]:
    rho = np.eye(2) / 2
    Z = np.diag([t, -t])
    D = np.eye(2) / np.sqrt(2)
    C = np.trace(D @ Z @ D @ Z)
    two_d = np.sum(np.abs(np.linalg.eigvalsh(D @ Z @ D)))
    assert np.isclose(C, t * t) and np.isclose(two_d, np.sqrt(C))
print('exact upper endpoint checks passed')
