from pathlib import Path
import json
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.special import eval_hermitenorm
from scipy.stats import norm
import bump
ROOT = Path(__file__).resolve().parents[2]
(ROOT / 'figures').mkdir(exist_ok=True)
a_vals = np.geomspace(2.1, 300, 80)
rho = np.array([bump.rho(a) for a in a_vals])
assert np.all((rho > 0) & (rho < 1))
z0 = norm.ppf(0.75)
orders = np.arange(2, 22, 2)
coefficients = np.array([4 * norm.pdf(z0) * eval_hermitenorm(int(n - 1), z0) / math.sqrt(math.factorial(int(n))) for n in orders])

def magnitude_overlap(r):
    return np.sum(coefficients ** 2 * r ** orders)

def magnitude_quadrature(r):
    sd = np.sqrt(1 - r * r)

    def conditional(y):
        return 2 * (norm.sf((z0 - r * y) / sd) + norm.cdf((-z0 - r * y) / sd)) - 1
    return 2 * (-quad(lambda y: conditional(y) * norm.pdf(y), 0, z0, epsabs=1e-13)[0] + quad(lambda y: conditional(y) * norm.pdf(y), z0, 12, epsabs=1e-13)[0])
for r in [0.01, 0.05, 0.3]:
    assert abs(magnitude_overlap(r) - magnitude_quadrature(r)) < 1e-12
C_sign = 2 * np.arcsin(rho) / np.pi
C_mag_lower = np.array([magnitude_overlap(r) for r in rho])
C_mag_upper = C_mag_lower + rho ** 22
assert np.all(C_mag_upper <= rho ** 2)
record = dict(a=a_vals.tolist(), rho=rho.tolist(), omega_mean=bump.omega_mean, asymptotic_coefficient=bump.g0 ** 2 / (4 * bump.norm1), sign_mirror=(C_sign / 2).tolist(), sign_upper=(np.sqrt(C_sign) / 2).tolist(), magnitude_mirror_lower=(C_mag_lower / 2).tolist(), magnitude_upper=(np.sqrt(C_mag_upper) / 2).tolist(), magnitude_overlap_tail_bound=(rho ** 22).tolist(), magnitude_Hermite_orders=orders.tolist(), magnitude_Hermite_coefficients=coefficients.tolist())
Path(__file__).with_name('leakage_data.json').write_text(json.dumps(record, indent=2) + '\n')
plt.rcParams.update({'font.family': 'serif', 'font.size': 8, 'axes.linewidth': 0.6, 'xtick.direction': 'in', 'ytick.direction': 'in', 'mathtext.fontset': 'dejavuserif', 'pdf.fonttype': 42})
fig, ax = plt.subplots(figsize=(3.35, 3.1))
for upper, lower, name, color in [(np.sqrt(C_sign) / 2, C_sign / 2, 'Sign', '#0072B2'), (np.sqrt(C_mag_upper) / 2, C_mag_lower / 2, 'Magnitude', '#D55E00')]:
    ax.fill_between(a_vals, lower, upper, color=color, alpha=0.09)
    ax.plot(a_vals, upper, color=color, lw=1.4, zorder=3, label=name + ': whole-wedge bound')
    ax.plot(a_vals, lower, color=color, lw=1.4, ls='--', zorder=4, label=name + ': reflected attack')
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_ylabel('Guessing advantage $d$')
ax.grid(True, which='major', lw=0.4, color='.88')
ax.spines[['top', 'right']].set_visible(False)
ax.set_xlim(2.1, 300)
ax.set_ylim(2e-14, 0.2)
ax.legend(loc='lower left', fontsize=6.8, frameon=False, handlelength=1.8)
ax.set_xlabel('Distance from the wedge edge, $a/\\sigma$')
fig.tight_layout(pad=0.3)
fig.savefig(ROOT / 'figures/fig_leakage.pdf')
r = bump.rho(10)
print(json.dumps(dict(rho_at_10=r, sign_upper_at_10=np.sqrt(2 * np.arcsin(r) / np.pi) / 2, magnitude_upper_at_10=np.sqrt(magnitude_overlap(r) + r ** 22) / 2, omega_mean=bump.omega_mean, asymptotic_coefficient=record['asymptotic_coefficient'], maximum_overlap_tail_bound=float(max(rho ** 22))), indent=2))
