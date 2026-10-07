"""Smeared massless scalar field with a compactly supported source profile.

f(t, x) = b(t/tau) B(|x - a e1| / R),  b, B standard smooth bumps on (-1, 1).
supp f lies in the right wedge for a > tau + R.  We take tau = R = sigma.

On the mass shell (omega = |k|) the one-particle wave function is
    h(k) = g(|k|) exp(-i k1 a),  g(k) = bhat(k) * Bhat(k),
with the Lorentz-invariant measure d^3k / ((2 pi)^3 2|k|).  Then
    v      = <h, h>                 ~ int k g^2 dk
    c      = <h, Delta^{1/2} h>     ~ int k g^2 sinc(2 k a) dk
    <h,Kh> = 2 pi a <omega> v,      <omega> = int k^2 g^2 / int k g^2,
so rho = c / v and the one-particle modular energy per unit norm is
    S_f / v = 2 pi a <omega>.
Common prefactors cancel in all ratios.
"""
import numpy as np
from scipy.integrate import quad, simpson
from scipy.interpolate import CubicSpline
import os


def bump(s):
    s = np.asarray(s, float)
    out = np.zeros_like(s)
    m = np.abs(s) < 1
    out[m] = np.exp(-1.0 / (1.0 - s[m] ** 2))
    return out


sgrid = np.linspace(-1, 1, 4001)[1:-1]
bs = bump(sgrid)


def _chunked(fun, k, size=2000):
    return np.concatenate([fun(k[i:i + size]) for i in range(0, len(k), size)])


def bhat(k, tau=1.0):
    # Fourier transform of b(t/tau): tau * int b(s) cos(k tau s) ds, even and real
    return _chunked(lambda kk: tau * simpson(bs * np.cos(np.outer(kk, sgrid) * tau), x=sgrid), k)


rgrid = np.linspace(0, 1, 4001)[1:-1]
Br = bump(rgrid)


def Bhat(k, R=1.0):
    # 3D radial Fourier transform: 4 pi int B(r/R) r^2 sinc(k r) dr
    return _chunked(lambda kk: 4 * np.pi * R**3 * simpson(
        Br * rgrid**2 * np.sinc(np.outer(kk, rgrid) * R / np.pi), x=rgrid), k)


kmax, nk = 80.0, int(os.environ.get("BUMP_NK", "16001"))
k = np.linspace(0, kmax, nk)
g = bhat(k) * Bhat(k)
w1 = k * g**2
norm1 = simpson(w1, x=k)
omega_mean = simpson(k * w1, x=k) / norm1
g0 = g[0]
g2 = CubicSpline(k, g**2)


def rho(a):
    integral, error = quad(g2, 0, kmax, weight="sin", wvar=2*a, epsabs=1e-12)
    return integral / (2*a*norm1)


def rho_asym(a):
    # rho ~ g(0)^2 / (4 a^2 int k g^2 dk)
    return g0**2 / (4 * a**2 * norm1)


if __name__ == "__main__":
    print("tail check g(kmax)/g(0) =", g[-1] / g0, " <omega> sigma =", omega_mean)
    for a in [2, 3, 5, 10, 20, 50, 100, 300]:
        r = rho(a)
        print(f"a/sigma={a:4d} rho={r:.4e} asym={rho_asym(a):.4e} ratio={r/rho_asym(a):.4f} "
              f"Jensen floor exp(-pi a <w>)={np.exp(-np.pi*a*omega_mean):.3e}")
