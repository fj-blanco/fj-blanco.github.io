from __future__ import annotations
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import numpy as np
OUT = Path(__file__).with_suffix('.json')
RNG = np.random.default_rng(20261007)

def binom_upper_tail(n: int, k: int) -> Fraction:
    return Fraction(sum((math.comb(n, j) for j in range(max(0, k), n + 1))), 2 ** n)

def agreement_tail(m: int, active: int, rho: Fraction) -> Fraction:
    return binom_upper_tail(active, math.ceil((active + m * rho) / 2))

def exhaustive_pair_check() -> int:
    checked = 0
    for m in (2, 4):
        rules = list(product((0, 1), repeat=m))
        for f in product((0, 1), repeat=2 * m):
            active = sum((f[u] != f[m + u] for u in range(m)))
            for rho in (Fraction(1, 4), Fraction(1, 2), Fraction(1)):
                hits = 0
                for g in rules:
                    correct = sum(((f[u] == g[u]) + (f[m + u] == 1 - g[u]) for u in range(m)))
                    hits += Fraction(correct, 2 * m) >= (1 + rho) / 2
                assert Fraction(hits, len(rules)) == agreement_tail(m, active, rho)
                checked += 1
    assert agreement_tail(2, 1, Fraction(1, 4)) == Fraction(1, 2)
    assert agreement_tail(2, 2, Fraction(1, 4)) == Fraction(1, 4)
    return checked

def identity_check(trials: int=200) -> float:
    worst = 0.0
    for _ in range(trials):
        p = int(RNG.integers(2, 9))
        m = 1 << p - 1
        delta = float(RNG.uniform(0.01, 0.49))
        g = RNG.integers(0, 2, m)
        f = RNG.integers(0, 2, 2 * m)
        c = np.arange(2 * m)
        b = c >> p - 1 ^ g[c & m - 1]
        direct = np.mean(np.where(f == b, 1 - delta, delta))
        worst = max(worst, abs(direct - (delta + (1 - 2 * delta) * np.mean(f == b))))
    return float(worst)

def tail_table() -> list[dict]:
    rows = []
    for p in range(2, 9):
        m = 1 << p - 1
        for rho in (Fraction(1, 10), Fraction(1, 4), Fraction(1, 2), Fraction(1)):
            tails = [agreement_tail(m, active, rho) for active in range(m + 1)]
            bound = math.exp(-float(rho) ** 2 * m / 2)
            worst = max(tails)
            rows.append(dict(p=p, rho=str(rho), active_counts_checked=m + 1, maximum_exact_tail=str(worst), hoeffding_bound=bound, holds=float(worst) <= bound * (1 + 1e-12)))
    return rows

def constants_check() -> list[dict]:
    rows = []
    for a in (1.0, 3.0, 10.0):
        for rho in (0.1, 0.5, 1.0):
            d = rho ** 2 / (8 * a * math.log(2))
            for p in (20, 30, 40, 60):
                s = math.floor(d * 2 ** p / p)
                if s < p:
                    continue
                exponent = a * s * math.log(s) - rho ** 2 * 2 ** (p - 2)
                rows.append(dict(a=a, rho=rho, p=p, s=s, holds=exponent <= -rho ** 2 * 2 ** p / 8))
    return rows

def main() -> None:
    report = dict(exhaustive_pair_cases=exhaustive_pair_check(), agreement_identity_max_error=identity_check(), tails_all_active_counts=tail_table(), constants=constants_check())
    report['summary'] = dict(identity_ok=report['agreement_identity_max_error'] < 1e-12, hoeffding_ok=all((r['holds'] for r in report['tails_all_active_counts'])), constants_ok=all((r['holds'] for r in report['constants'])))
    OUT.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['summary'], indent=2))
    if not all(report['summary'].values()):
        raise SystemExit('Decision-cost validation failed')
if __name__ == '__main__':
    main()
