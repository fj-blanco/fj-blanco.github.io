import math
from statistics import NormalDist
import numpy as np

def step(t):
    t = np.asarray(t, dtype=float)
    y = np.zeros_like(t)
    dy = np.zeros_like(t)
    y[t >= 1] = 1
    m = (t > 0) & (t < 1)
    x = t[m]
    left, right = (np.exp(-1 / x), np.exp(-1 / (1 - x)))
    y[m] = left / (left + right)
    dy[m] = y[m] * (1 - y[m]) * (1 / x ** 2 + 1 / (1 - x) ** 2)
    return (y, dy)

def profile(t):
    s, ds = step(np.asarray(t) + 1)
    return (np.exp(-t) * s, np.exp(-t) * (ds - s))

def pulse_checks():
    t = np.linspace(0, 1, 40001)
    s, ds = step(t)
    tail_deriv = np.exp(-t) * (-ds - (1 - s))
    cchi = 2 * math.pi * np.trapezoid(t * tail_deriv ** 2, t)
    jchi = np.trapezoid(tail_deriv ** 2, t)
    core = np.linspace(-1, 0, 40001)
    _, gp = profile(core)
    ce = np.trapezoid(gp ** 2, core) + 0.5 + jchi
    h = np.zeros_like(core)
    m = (core > -0.75) & (core < -0.25)
    h[m] = np.exp(-1 / (core[m] + 0.75) + 1 / (core[m] + 0.25)) * gp[m]
    pairing = np.trapezoid(gp * h, core)
    assert pairing > 0
    for ell in (0.7, 1.0, 2.3):
        for n in (2, 4, 8):
            amp, a = (math.sqrt(n), n * ell)
            u = np.linspace(0, ell, 40001)
            g, dg = profile((u + a) / ell)
            st, dst = step(u / ell)
            df = amp / ell * (dg * (1 - st) - g * dst)
            entropy = 2 * math.pi * np.trapezoid(u * df ** 2, u)
            expected = cchi * amp ** 2 * math.exp(-2 * a / ell)
            assert np.isclose(entropy, expected, rtol=1e-10, atol=1e-20)
            grid = np.linspace(-a - ell, ell, 200001)
            g, dg = profile((grid + a) / ell)
            st, dst = step(grid / ell)
            df = amp / ell * (dg * (1 - st) - g * dst)
            energy = np.trapezoid(df ** 2, grid)
            assert 0 < energy <= ce * amp ** 2 / ell * (1 + 1e-10)
            uc = ell * core - a
            g, dg = profile((uc + a) / ell)
            st, dst = step(uc / ell)
            df = amp / ell * (dg * (1 - st) - g * dst)
            measured = np.trapezoid(df * h, uc) / amp
            assert np.isclose(measured, pairing, rtol=1e-10)
    print(f'Pulse integrals verified: C_chi={cchi:.9g}, C_E={ce:.9g}, nonzero core pairing={pairing:.9g}')

def domination_checks():
    rng = np.random.default_rng(1907)
    for dim in (2, 3, 5):
        tau = np.arange(1, dim + 1, dtype=float)
        tau /= tau.sum()
        raw = rng.normal(size=(dim ** 2, dim ** 2)) + 1j * rng.normal(size=(dim ** 2, dim ** 2))
        rho = raw @ raw.conj().T
        rho /= np.trace(rho)
        lam, vec = np.linalg.eigh(rho)
        marginal = np.zeros((dim, dim), complex)
        for j in range(dim ** 2):
            c = vec[:, j].reshape(dim, dim)
            marginal += lam[j] * c.T @ c.conj()
        inv = np.diag(1 / np.sqrt(tau))
        pmax = 1 / np.linalg.eigvalsh(inv @ marginal @ inv)[-1]
        total_effect = np.zeros((dim, dim), complex)
        output = np.zeros_like(rho)
        for j in range(dim ** 2):
            c = vec[:, j].reshape(dim, dim)
            b = math.sqrt(pmax * lam[j]) * c @ inv
            total_effect += b.conj().T @ b
            out = (b @ np.diag(np.sqrt(tau))).reshape(-1)
            output += np.outer(out, out.conj())
        assert np.linalg.eigvalsh(total_effect)[-1] <= 1 + 1e-12
        assert np.allclose(output, pmax * rho, atol=1e-13)
        assert np.linalg.eigvalsh(np.diag(tau) - 1.01 * pmax * marginal)[0] < -1e-05
    print('Mixed-output domination criterion verified in dimensions 2, 3, 5, including violation above the optimum')

def optical_checks():
    dim = 100
    annih = np.diag(np.sqrt(np.arange(1, dim)), 1).astype(complex)
    number = np.arange(dim)
    for lam in (0.35, 0.65, 0.85):
        tau = (1 - lam ** 2) * lam ** (2 * number)
        root = np.diag(np.sqrt(tau))
        nbar = lam ** 2 / (1 - lam ** 2)
        for alpha in (0.2 + 0.15j, 0.9 - 0.3j):
            ket = np.empty(dim, complex)
            ket[0] = math.exp(-abs(alpha) ** 2 / 2)
            for k in range(1, dim):
                ket[k] = ket[k - 1] * alpha / math.sqrt(k)
            beta = alpha.conjugate() / lam
            gen = beta * annih.conj().T - beta.conjugate() * annih
            val, vectors = np.linalg.eigh(-1j * gen)
            disp = vectors * np.exp(1j * val) @ vectors.conj().T
            for efficiency in (0.25, 0.7, 1.0):
                effect = disp * (1 - efficiency) ** number @ disp.conj().T
                sigma = root @ effect.T @ root
                p = np.trace(sigma).real
                rho = sigma / p
                p_formula = math.exp(-efficiency * abs(beta) ** 2 / (1 + efficiency * nbar)) / (1 + efficiency * nbar)
                gamma = efficiency * math.sqrt(nbar * (1 + nbar)) * beta.conjugate() / (1 + efficiency * nbar)
                nth = (1 - efficiency) * nbar / (1 + efficiency * nbar)
                fidelity = np.vdot(ket, rho @ ket).real
                f_formula = math.exp(-abs(alpha - gamma) ** 2 / (1 + nth)) / (1 + nth)
                assert np.isclose(p, p_formula, rtol=2e-09, atol=1e-12)
                assert np.isclose(fidelity, f_formula, rtol=2e-09, atol=1e-12)
                assert np.isclose(np.trace(rho @ annih), gamma, rtol=2e-09, atol=1e-12)
                assert np.isclose(np.dot(number, np.diag(rho)).real, nth + abs(gamma) ** 2, rtol=2e-09, atol=1e-12)
                if efficiency == 1:
                    assert np.isclose(p, math.exp(-abs(alpha) ** 2 / nbar) / (1 + nbar), rtol=2e-09)
    print('Optical rate, mean, thermal noise, fidelity, and ideal optimum verified against 100-level Fock calculations (18 cases)')
if __name__ == '__main__':
    pulse_checks()
    domination_checks()
    optical_checks()
