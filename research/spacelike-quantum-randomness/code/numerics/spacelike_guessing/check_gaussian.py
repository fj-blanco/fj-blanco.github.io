import numpy as np
from numpy.polynomial.hermite_e import hermegauss
from scipy.special import erf
N = 70
r = 0.55
lam = np.tanh(r)
beta = -2 * np.log(lam)
a1 = np.diag(np.sqrt(np.arange(1, N)), 1)
x1 = (a1 + a1.T) / np.sqrt(2)
w, V = np.linalg.eigh(x1)
Omega = np.diag(np.sqrt(1 - lam ** 2) * lam ** np.arange(N))
Kdiag = beta * (np.arange(N)[:, None] - np.arange(N)[None, :])
sqrtDelta = np.exp(-Kdiag / 2)

def F_of_xa(F):
    return V * F(w) @ V.T
h = x1 @ Omega
v = np.sum(h * h)
rho = np.sum(h * h * sqrtDelta) / v
kh = np.sum(h * h * Kdiag)
print(f'v={v:.6f}, rho={rho:.6f}')
assert np.isclose(v, np.cosh(2 * r) / 2, atol=1e-12)
assert np.isclose(rho, np.tanh(2 * r), atol=1e-12)
z, wz = hermegauss(120)
wz = wz / wz.sum()

def E1(g):
    return np.sum(wz * g(np.sqrt(v) * z))

def E2(F, G):
    X = np.sqrt(v) * z[:, None]
    Y = rho * X + np.sqrt(v * (1 - rho ** 2)) * z[None, :]
    return np.sum(wz[:, None] * wz[None, :] * F(X) * G(Y))
for name, F, dF, s in [('Ramsey sin(0.8x)', lambda x: np.sin(0.8 * x), lambda x: 0.8 * np.cos(0.8 * x), 0.8), ('tanh(1.5x)', lambda x: np.tanh(1.5 * x), lambda x: 1.5 / np.cosh(1.5 * x) ** 2, None)]:
    psi = F_of_xa(F) @ Omega
    q = np.sum(psi * psi)
    C = np.sum(psi * psi * sqrtDelta)
    kap_q = np.sum(psi * psi * Kdiag)
    assert np.isclose(q, E1(lambda x: F(x) ** 2), atol=2e-05)
    assert np.isclose(C, E2(F, F), atol=2e-05)
    assert np.isclose(kap_q, kh * E1(lambda x: dF(x) ** 2), atol=0.0002)
    print(f"{name}: q={q:.6f} vs {E1(lambda x: F(x) ** 2):.6f}; C={C:.6f} vs Mehler {E2(F, F):.6f}; kappa*q={kap_q:.6f} vs <h,Kh>E[F'^2]={kh * E1(lambda x: dF(x) ** 2):.6f}")
s = 0.8
vs, cs = (s ** 2 * v, s ** 2 * rho * v)
print('Ramsey closed form e^{-v}sinh c:', np.exp(-vs) * np.sinh(cs), ' q:', (1 - np.exp(-2 * vs)) / 2)
m = np.exp(-v / 2)
F = lambda x: (np.cos(x) - m) / (1 + m)
dF = lambda x: -np.sin(x) / (1 + m)
psi = F_of_xa(F) @ Omega
C = np.sum(psi * psi * sqrtDelta)
expected = m * m * (np.cosh(rho * v) - 1) / (1 + m) ** 2
assert np.isclose(E1(F), 0, atol=1e-12)
assert np.isclose(C, expected, atol=1e-12)
assert np.isclose(np.sum(psi * psi * Kdiag), kh * E1(lambda x: dF(x) ** 2), atol=1e-12)
print('smooth even readout: overlap and finite-energy identity passed', C)
