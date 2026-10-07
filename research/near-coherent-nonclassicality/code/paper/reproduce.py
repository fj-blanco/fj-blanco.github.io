from __future__ import annotations
import json
import math
import os
from functools import lru_cache
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR', '/tmp/coherent-paper-matplotlib')
import numpy as np
from numpy.polynomial import polynomial as poly
from numpy.polynomial.hermite import hermgauss, hermval
from numpy.polynomial.legendre import leggauss
OUT = Path(__file__).resolve().parent

@lru_cache(None)
def gauss(n):
    return leggauss(n)

def state_coefficients(eps, direction):
    c = np.zeros(max(direction) + 1, dtype=complex)
    c[0] = 1
    for n, v in direction.items():
        c[n] = eps * v
    return c

def bargmann(c):
    return np.array([v / math.sqrt(math.factorial(n)) for n, v in enumerate(c)])

def kernel(f, z, tau=1.0):
    result = np.zeros(np.shape(z), dtype=float)
    for j in range(len(f)):
        result += (1 - 2 * tau) ** j / math.factorial(j) * abs(poly.polyval(z, poly.polyder(f, j))) ** 2
    return result

def loss_density(c, tau):
    rho = np.outer(c, c.conj()) / np.vdot(c, c).real
    result = np.zeros_like(rho)
    for ell in range(len(c)):
        K = np.zeros_like(rho)
        for n in range(ell, len(c)):
            K[n - ell, n] = math.sqrt(math.comb(n, ell) * (1 - tau) ** ell * tau ** (n - ell))
        result += K @ rho @ K.conj().T
    return result

def associated_laguerre(n, alpha, x):
    return sum((math.comb(n + alpha, n - j) * (-x) ** j / math.factorial(j) for j in range(n + 1)))

def fock_wigner(rho, beta):
    x = 4 * abs(beta) ** 2
    result = np.zeros(np.shape(beta), dtype=float)
    for n in range(len(rho)):
        result += rho[n, n].real * (-1) ** n * associated_laguerre(n, 0, x)
        for m in range(n + 1, len(rho)):
            term = rho[m, n] * (-1) ** n * math.sqrt(math.factorial(n) / math.factorial(m))
            term *= (2 * np.conj(beta)) ** (m - n) * associated_laguerre(n, m - n, x)
            result += 2 * term.real
    return 2 / math.pi * np.exp(-x / 2) * result

def logsumexp(x):
    x = np.asarray(x)
    m = x.max()
    return float(m + np.log(np.exp(x - m).sum()))

def log_negative_volume(c, tau=1.0, nr=64, nt=192):
    if tau <= 0.5:
        return -math.inf
    f = bargmann(c)
    roots = poly.polyroots(f)
    q = 2 * tau - 1
    radius = 2 * math.sqrt(q)
    distances = abs(roots[:, None] - roots[None, :]) + np.eye(len(roots)) * 1000000000.0
    if distances.min() < 2 * radius:
        raise ValueError('Stellar roots are too close for disjoint pocket quadrature')
    xth, wth = gauss(nt)
    th = math.pi * (xth + 1)
    wth = math.pi * wth
    xr, wr = gauss(nr)
    logs = []
    for root in roots:
        phase = root / abs(root)
        unit = phase * np.exp(1j * th)
        lo = np.zeros(nt)
        hi = np.full(nt, radius)
        assert float(kernel(f, root, tau)) < 0
        assert np.all(kernel(f, root + hi * unit, tau) > 0)
        grid = np.linspace(0, radius, 65)[:, None]
        signs = kernel(f, root + grid * unit, tau) < 0
        assert not np.any(np.diff(signs.astype(int), axis=0) > 0)
        for _ in range(48):
            mid = (lo + hi) / 2
            inside = kernel(f, root + mid * unit, tau) < 0
            lo = np.where(inside, mid, lo)
            hi = np.where(inside, hi, mid)
        boundary = (lo + hi) / 2
        r = (xr[:, None] + 1) * boundary / 2
        z = root + r * unit
        neg = -kernel(f, z, tau)
        assert np.all(neg > 0)
        weight = wr[:, None] * boundary / 2 * wth[None, :] * r
        logs.append(logsumexp(np.log(neg) + np.log(weight) - abs(z) ** 2 / (2 * tau)))
    return logsumexp(logs) - math.log(2 * math.pi * tau * np.vdot(c, c).real)

def full_plane_volume(c, tau, n=1001):
    f = bargmann(c)
    roots = poly.polyroots(f)
    lim = max(abs(roots)) + 4
    u = np.linspace(-lim, lim, n)
    total = 0.0
    for y in u:
        z = u + 1j * y
        total += np.maximum(-kernel(f, z, tau), 0).dot(np.exp(-abs(z) ** 2 / (2 * tau)))
    return total * (u[1] - u[0]) ** 2 / (2 * math.pi * tau * np.vdot(c, c).real)

def validate():
    rng = np.random.default_rng(6142026)
    max_error = 0.0
    for degree in (3, 5, 8):
        c = rng.normal(size=degree + 1) + 1j * rng.normal(size=degree + 1)
        c[0] += 3
        beta = rng.normal(size=70) + 1j * rng.normal(size=70)
        for tau in (0.1, 0.5, 0.7, 1.0):
            expected = fock_wigner(loss_density(c, tau), beta)
            actual = 2 / math.pi * np.exp(-2 * abs(beta) ** 2) * kernel(bargmann(c), 2 * math.sqrt(tau) * beta.conj(), tau) / np.vdot(c, c).real
            error = float(abs(actual - expected).max())
            max_error = max(max_error, error)
            assert error < 2e-12
    refinement = []
    full_grid = []
    for direction in ({3: 1}, {3: 1, 5: 1}, {2: 0.6j, 4: 0.3, 5: 1}):
        d = max(direction)
        for R in (8.0, 20.0, 80.0):
            eps = math.sqrt(math.factorial(d)) / abs(direction[d]) / R ** d
            c = state_coefficients(eps, direction)
            for tau in (0.7, 1.0):
                a = log_negative_volume(c, tau)
                b = log_negative_volume(c, tau, nr=96, nt=384)
                error = abs(a - b)
                refinement.append(error)
                assert error < 2e-07, (direction, R, tau, error)
            if R == 8:
                reference = log_negative_volume(c)
                values = [full_plane_volume(c, 1.0, n=n) for n in (801, 1601)]
                rel = abs(values[-1] / math.exp(reference) - 1)
                full_grid.append(rel)
                assert rel < 0.0008, (direction, rel)
    q, w = hermgauss(40)
    theta = 2 * math.pi * np.arange(48) / 48
    d = 8
    hs = np.array([hermval(q, [0] * k + [1]) / math.sqrt(2 ** k * math.factorial(k)) for k in range(d + 1)])
    c = rng.normal(size=d + 1) + 1j * rng.normal(size=d + 1)
    rho = loss_density(c, 0.73)
    wave = hs[:, :, None] * np.exp(-1j * np.arange(d + 1)[:, None, None] * theta)
    density_ratio = np.einsum('mn,mqt,nqt->qt', rho, wave, wave.conj()).real
    homodyne_error = 0.0
    for k in range(1, d + 1):
        estimate = np.einsum('qt,q,q,t->', density_ratio, w, hs[k], np.exp(1j * k * theta)) / (math.sqrt(math.pi) * len(theta))
        expected = sum((math.sqrt(math.factorial(n + k) / math.factorial(n) / math.factorial(k)) * rho[n + k, n] for n in range(d + 1 - k)))
        homodyne_error = max(homodyne_error, abs(estimate - expected))
        assert abs(estimate - expected) < 2e-12
        assert abs(np.dot(w, hs[k] ** 2) / math.sqrt(math.pi) - 1) < 2e-12
    witness_error = 0.0
    for k in range(2, 9):
        eps = 0.08
        c = state_coefficients(eps, {k: 1})
        for tau in (0.01, 0.3, 0.5, 0.8, 1.0):
            rho = loss_density(c, tau)
            F1 = sum((n * rho[n, n].real for n in range(k + 1)))
            Fkm1 = sum((math.factorial(n) / math.factorial(n - k + 1) * rho[n, n].real for n in range(k - 1, k + 1)))
            actual = F1 * Fkm1 - math.factorial(k) * abs(rho[k, 0]) ** 2
            predicted = tau ** k * math.factorial(k) * eps ** 2 * (k * eps ** 2 - 1) / (1 + eps ** 2) ** 2
            witness_error = max(witness_error, abs(actual - predicted))
            assert np.isclose(actual, predicted, rtol=1e-12, atol=1e-13)
    return {'kernel_max_absolute_error': max_error, 'pocket_refinement_max_log_error': max(refinement), 'full_plane_max_relative_error': max(full_grid), 'homodyne_max_absolute_error': float(homodyne_error), 'witness_max_absolute_error': witness_error}

def make_figures():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import TwoSlopeNorm
    from matplotlib.patches import Circle
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'mathtext.fontset': 'stixsans', 'axes.labelsize': 10, 'axes.titlesize': 11, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#a6b2bc', 'text.color': '#172c3c', 'axes.labelcolor': '#172c3c', 'xtick.color': '#455a6b', 'ytick.color': '#455a6b', 'pdf.fonttype': 42, 'svg.fonttype': 'none', 'savefig.facecolor': 'white'})
    specs = [({3: 1}, 1.0, '#2364a8', 'o', '-', '$d=3,\\ \\tau=1$'), ({3: 1, 5: 1}, 1.0, '#ca503e', 's', '--', '$d=5,\\ \\tau=1$'), ({3: 1, 5: 1}, 0.7, '#008778', '^', '-.', '$d=5,\\ \\tau=0.7$')]
    records, refinement = ([], [])
    fig, axes = plt.subplots(1, 2, figsize=(8.2, 3.25), layout='constrained')
    for direction, tau, color, marker, ls, label in specs:
        d = max(direction)
        for panel in range(2):
            if panel == 0:
                epsilons = np.geomspace(1e-06, 0.0003, 13)
                radii = (math.sqrt(math.factorial(d)) / epsilons) ** (1 / d)
            else:
                radii = np.geomspace(8, 100, 15)
                epsilons = math.sqrt(math.factorial(d)) / radii ** d
            values = []
            for eps, R in zip(epsilons, radii):
                c = state_coefficients(eps, direction)
                ln = log_negative_volume(c, tau)
                refined = log_negative_volume(c, tau, nr=96, nt=384)
                refinement.append(abs(ln - refined))
                assert abs(ln - refined) < 1e-07
                values.append(ln)
                records.append({'panel': panel, 'nu': min(direction), 'd': d, 'tau': tau, 'epsilon': float(eps), 'R': float(R), 'log_negative_volume': ln, 'refinement_absolute_log_error': abs(ln - refined)})
            kw = dict(color=color, marker=marker, ls=ls, lw=1.6, ms=3.7, markeredgecolor='white', markeredgewidth=0.45, label=label)
            if panel == 0:
                axes[0].loglog(epsilons, -np.array(values), **kw)
            else:
                axes[1].plot(1 / radii, -2 * tau * np.array(values) / radii ** 2, **kw)
    axes[0].set(xlabel='Amplitude $\\epsilon$', ylabel='$-\\log\\mathcal{N}_W$', xlim=(8e-07, 0.0004))
    axes[0].set_title('(a)  Different exponential scales', loc='left')
    axes[0].legend(frameon=False, fontsize=9, loc='upper right')
    axes[1].axhline(1, color='#70818f', ls=(0, (3, 3)), lw=1, zorder=0)
    axes[1].scatter([0], [1], s=22, color='#172c3c', zorder=4)
    axes[1].text(0.003, 1.005, 'Limit', fontsize=9, color='#455a6b')
    axes[1].set(xlim=(-0.003, 0.13), ylim=(0.94, 1.025), xlabel='Inverse stellar scale $R^{-1}$', ylabel='$-2\\tau\\,\\log\\mathcal{N}_W\\,/\\,R^2$')
    axes[1].set_title('(b)  Convergence to the rate', loc='left')
    for ax in axes:
        ax.grid(alpha=0.12)
    fig.savefig(OUT / 'fig_rates.pdf', bbox_inches='tight')
    fig.savefig(OUT / 'fig_rates.png', dpi=220, bbox_inches='tight')
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.25), layout='constrained')
    R, d = (14.0, 5)
    c = state_coefficients(math.sqrt(math.factorial(d)) / R ** d, {3: 1, 5: 1})
    f = bargmann(c)
    roots = poly.polyroots(f)
    candidates = roots[abs(abs(roots) - min(abs(roots))) < 1e-08]
    root = candidates[np.argmax(candidates.imag)]
    phase = root / abs(root)
    v = np.linspace(-1.3, 1.3, 321)
    x, y = np.meshgrid(v, v)
    local_data = {}
    for ax, tau, panel in zip(axes, (1.0, 0.7), ('a', 'b')):
        B = kernel(f, root + phase * (x + 1j * y), tau) / abs(poly.polyval(root, poly.polyder(f))) ** 2
        im = ax.pcolormesh(x, y, B, cmap='RdBu_r', norm=TwoSlopeNorm(vmin=-1.1, vcenter=0, vmax=3), shading='auto', rasterized=True)
        ax.contour(x, y, B, levels=[0], colors='#172c3c', linewidths=1.3)
        ax.add_patch(Circle((0, 0), math.sqrt(2 * tau - 1), fill=False, edgecolor='white', lw=1.6, ls='--'))
        ax.scatter([0], [0], marker='x', color='white', s=35, lw=1.3)
        ax.set(aspect='equal', xlabel='Radial offset $\\mathrm{Re}\\,u$', ylabel='Tangential offset $\\mathrm{Im}\\,u$', xticks=[-1, 0, 1], yticks=[-1, 0, 1])
        ax.set_title(f'({panel})  Transmission $\\tau={tau:g}$', loc='left')
        local_data[str(tau)] = B
    cb = fig.colorbar(im, ax=axes, fraction=0.035, pad=0.035, extend='max')
    cb.set_label("$B\\,/\\,|f'(z_*)|^2$")
    fig.savefig(OUT / 'fig_pockets.pdf', bbox_inches='tight')
    fig.savefig(OUT / 'fig_pockets.png', dpi=220, bbox_inches='tight')
    plt.close(fig)
    np.savez_compressed(OUT / 'pocket_data.npz', x=x, y=y, B_tau_1=local_data['1.0'], B_tau_07=local_data['0.7'], root=root, R=R, f=f)
    return (records, max(refinement))
if __name__ == '__main__':
    checks = validate()
    print(json.dumps(checks, indent=2), flush=True)
    records, error = make_figures()
    checks['plotted_rates_max_refinement_log_error'] = error
    (OUT / 'numerical_data.json').write_text(json.dumps({'checks': checks, 'rate_data': records}, indent=2) + '\n')
    print(f'All checks passed. Maximum plotted log-volume refinement difference: {error:.3g}')
    print(f'Figures and numerical data written to {OUT}')
