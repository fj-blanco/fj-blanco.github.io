from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import numpy as np
OUT = Path(__file__).with_suffix('.json')
RNG = np.random.default_rng(20261008)

def u_stat_batch(contexts: np.ndarray, labels: np.ndarray, m: int) -> np.ndarray:
    rows, n = contexts.shape
    z = 1 - 2 * labels.astype(np.int64)
    offset = (np.arange(rows)[:, None] * m + contexts).ravel()
    counts = np.bincount(offset, minlength=rows * m).reshape(rows, m)
    votes = np.bincount(offset, weights=z.ravel(), minlength=rows * m).reshape(rows, m)
    return m * np.sum(votes ** 2 - counts, axis=1) / (n * (n - 1))

def variance_formula(n: int, m: int, delta: float) -> float:
    th = (1 - 2 * delta) ** 2
    return (2 * (m - th ** 2) + 4 * (n - 2) * (th - th ** 2)) / (n * (n - 1))

def moments_check(reps: int=20000) -> list[dict]:
    rows = []
    for m in (16, 256, 4096):
        for n in (8, 64, 512):
            for delta in (0.05, 0.2, 0.4):
                vals = []
                for start in range(0, reps, 2000):
                    k = min(2000, reps - start)
                    table = RNG.integers(0, 2, (k, m), dtype=np.int8)
                    c = RNG.integers(0, m, (k, n))
                    y = np.take_along_axis(table, c, 1) ^ (RNG.random((k, n)) < delta)
                    vals.append(u_stat_batch(c, y, m))
                v = np.concatenate(vals)
                th = (1 - 2 * delta) ** 2
                var = variance_formula(n, m, delta)
                mean_z = (v.mean() - th) / math.sqrt(var / reps)
                var_rel = v.var(ddof=1) / var - 1
                rows.append(dict(M=m, N=n, delta=delta, mean=float(v.mean()), theta=th, mean_z=float(mean_z), var_mc=float(v.var(ddof=1)), var_formula=var, var_relative_error=float(var_rel)))
    return rows

def exact_tv(m: int, n: int, d0: Fraction, d1: Fraction) -> tuple[Fraction, Fraction]:

    def law(delta: float) -> dict:
        out = {}
        for ctx in product(range(m), repeat=n):
            for lab in product((0, 1), repeat=n):
                total = Fraction(0)
                for table in product((0, 1), repeat=m):
                    pr = Fraction(1)
                    for c, y in zip(ctx, lab):
                        pr *= 1 - delta if y == table[c] else delta
                    total += pr
                out[ctx, lab] = total / 2 ** m / m ** n
        return out
    a, b = (law(d0), law(d1))
    tv = Fraction(1, 2) * sum((abs(a[k] - b[k]) for k in a))
    collision = 1 - math.prod((1 - Fraction(i, m) for i in range(n)))
    return (tv, collision)

def majority_error(r: int, delta: float) -> float:
    return sum((math.comb(r, e) * delta ** e * (1 - delta) ** (r - e) * (1.0 if 2 * e > r else 0.5 if 2 * e == r else 0.0) for e in range(r + 1)))

def hoeffding_majority_check(delta: float=0.1) -> float:
    gamma = 0.5 - delta
    worst = -1.0
    for r in range(0, 200):
        exact = majority_error(r, delta)
        worst = max(worst, exact - math.exp(-2 * r * gamma ** 2))
    return worst

def exact_moments_check() -> int:
    checked = 0
    for m, n in ((2, 2), (2, 3), (2, 4), (3, 3)):
        for delta in (Fraction(1, 10), Fraction(1, 4)):
            theta = (1 - 2 * delta) ** 2
            for table in product((0, 1), repeat=m):
                mass = mean = second = Fraction(0)
                for contexts in product(range(m), repeat=n):
                    for labels in product((0, 1), repeat=n):
                        probability = Fraction(1, m ** n)
                        for c, y in zip(contexts, labels):
                            probability *= delta if y != table[c] else 1 - delta
                        pair_sum = sum(((-1) ** (labels[i] + labels[j]) for i in range(n) for j in range(i + 1, n) if contexts[i] == contexts[j]))
                        u = Fraction(m * pair_sum, math.comb(n, 2))
                        mass += probability
                        mean += probability * u
                        second += probability * u ** 2
                assert mass == 1 and mean == theta
                assert second - mean ** 2 == variance_formula(n, m, delta)
                checked += 1
    return checked

def main() -> None:
    report = {'exact_fixed_table_moment_cases': exact_moments_check()}
    tvs = []
    for m, n in ((3, 2), (3, 3), (4, 3), (4, 4)):
        tv, coll = exact_tv(m, n, Fraction(1, 20), Fraction(3, 10))
        union_bound = Fraction(math.comb(n, 2), m)
        tvs.append(dict(M=m, N=n, exact_tv=str(tv), collision_probability=str(coll), union_bound=str(union_bound), holds=tv <= coll <= union_bound))
    report['total_variation'] = tvs
    report['majority_hoeffding_max_excess'] = hoeffding_majority_check()
    report['moments_monte_carlo'] = moments_check()
    report['summary'] = {'tv_bound_holds': all((r['holds'] for r in tvs)), 'majority_hoeffding_ok': report['majority_hoeffding_max_excess'] <= 1e-15, 'max_abs_mean_z_diagnostic': max((abs(r['mean_z']) for r in report['moments_monte_carlo'])), 'max_abs_var_relative_error_diagnostic': max((abs(r['var_relative_error']) for r in report['moments_monte_carlo']))}
    OUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['summary'], indent=2))
    if not report['summary']['tv_bound_holds'] or not report['summary']['majority_hoeffding_ok']:
        raise SystemExit('Estimation validation failed')
if __name__ == '__main__':
    main()
