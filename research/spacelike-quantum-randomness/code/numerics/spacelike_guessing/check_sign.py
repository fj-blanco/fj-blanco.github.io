import numpy as np
from scipy.integrate import quad
from scipy.special import erf
from scipy.stats import multivariate_normal
phi = lambda y, v: np.exp(-y * y / (2 * v)) / np.sqrt(2 * np.pi * v)
for rho in [0.05, 0.3, 0.8]:
    v = 1.3
    val = 2 * quad(lambda y: phi(y, v) * erf(rho * y / np.sqrt(2 * v * (1 - rho ** 2))), 0, np.inf)[0]
    assert abs(val - 2 / np.pi * np.arcsin(rho)) < 1e-10
    print(rho, val, 2 / np.pi * np.arcsin(rho))
    best = np.exp(-v * (1 - rho ** 2) / 2) * quad(lambda y: phi(y, v) * abs(np.sin(rho * y)), -np.inf, np.inf, limit=400)[0]
    thr = np.exp(-v * (1 - rho ** 2) / 2) * 2 * quad(lambda y: phi(y, v) * np.sin(rho * y), 0, np.inf)[0]
    print('   best', best, 'threshold', thr, 'mirror', np.exp(-v) * np.sinh(rho * v))
rng = np.random.default_rng(1)
for rho in [0.05, 0.3, 0.8]:
    X = rng.normal(size=4000000)
    Y = rho * X + np.sqrt(1 - rho ** 2) * rng.normal(size=X.size)
    assert abs(np.mean(np.sign(X) * np.sign(Y)) - 2 / np.pi * np.arcsin(rho)) < 6 / np.sqrt(X.size)
    print('MC', rho, np.mean(np.sign(X) * np.sign(Y)), 2 / np.pi * np.arcsin(rho), 'Ramsey thr MC', np.mean(np.sin(1.2 * X) * np.sign(Y)))
for l in [0.1, 0.01]:
    v = l ** 2
    rho = 0.2
    thr = np.exp(-v * (1 - rho ** 2) / 2) * 2 * quad(lambda y: phi(y, v) * np.sin(rho * y), 0, 40 * np.sqrt(v))[0]
    C = np.exp(-v) * np.sinh(rho * v)
    assert abs(thr / np.sqrt(C) - np.sqrt(2 * rho / np.pi)) < 3e-05
    print(l, thr / np.sqrt(C), np.sqrt(2 * rho / np.pi))
from scipy.stats import norm
z0 = norm.ppf(0.75)
a2 = 2 * np.sqrt(2) * z0 * norm.pdf(z0)
assert abs(2 * (2 * norm.sf(z0)) - 1) < 1e-14
for rho in [0.01, 0.05, 0.3]:
    sd = np.sqrt(1 - rho * rho)

    def conditional(y):
        tail = norm.sf((z0 - rho * y) / sd) + norm.cdf((-z0 - rho * y) / sd)
        return 2 * tail - 1
    C = 2 * (quad(lambda y: -conditional(y) * norm.pdf(y), 0, z0, epsabs=1e-13)[0] + quad(lambda y: conditional(y) * norm.pdf(y), z0, 10, epsabs=1e-13)[0])
    assert 0 < C <= rho * rho + 1e-12
    if rho == 0.01:
        assert abs(C / (a2 * a2 * rho * rho) - 1) < 0.001
    print('magnitude readout:', rho, 'C=', C, 'leading=', a2 * a2 * rho * rho)
