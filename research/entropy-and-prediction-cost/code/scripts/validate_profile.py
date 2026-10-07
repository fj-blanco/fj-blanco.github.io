from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product
import json
import math
from pathlib import Path
import random
import numpy as np
OUT = Path(__file__).with_suffix('.json')

def bayes(c: int, p: int, g: list[int]) -> int:
    return c >> p - 1 ^ g[c & (1 << p - 1) - 1]

def word_probabilities(p: int, g: list[int], n: int, delta):
    if n <= p:
        return [Fraction(1, 2 ** n) if isinstance(delta, Fraction) else 2.0 ** (-n)] * 2 ** n
    mask = (1 << p) - 1
    probs = []
    for word in range(1 << n):
        state = word >> n - p
        prob = Fraction(1, 2 ** p) if isinstance(delta, Fraction) else 2.0 ** (-p)
        for shift in range(n - p - 1, -1, -1):
            bit = word >> shift & 1
            prob *= 1 - delta if bit == bayes(state, p, g) else delta
            state = state << 1 & mask | bit
        probs.append(prob)
    return probs

def spectrum_formula(p: int, n: int, delta) -> Counter:
    if n <= p:
        return Counter({Fraction(1, 2 ** n): 2 ** n})
    return Counter({Fraction(1, 2 ** p) * delta ** j * (1 - delta) ** (n - p - j): 2 ** p * math.comb(n - p, j) for j in range(n - p + 1)})

def renyi(probs, alpha: float) -> float:
    q = np.asarray([float(x) for x in probs if x > 0])
    if alpha == 0:
        return math.log2(len(q))
    if alpha == 1:
        return float(-np.sum(q * np.log2(q)))
    if math.isinf(alpha):
        return -math.log2(q.max())
    return float(np.log2(np.sum(q ** alpha)) / (1 - alpha))

def h_alpha(delta: float, alpha: float) -> float:
    return renyi([delta, 1 - delta], alpha)

def karp_min_mean_cycle(weights: np.ndarray) -> float:
    n = len(weights)
    d = np.full((n + 1, n), np.inf)
    d[0, :] = 0.0
    for k in range(1, n + 1):
        d[k] = np.min(d[k - 1][:, None] + weights, axis=0)
    best = np.inf
    for v in range(n):
        if not np.isfinite(d[n, v]):
            continue
        worst = max(((d[n, v] - d[k, v]) / (n - k) for k in range(n) if np.isfinite(d[k, v])))
        best = min(best, worst)
    return float(best)

def moore_states(p: int, g: list[int]) -> int:
    m = 1 << p
    part = [bayes(c, p, g) for c in range(m)]
    while True:
        sig = [(part[c], part[2 * c % m], part[(2 * c + 1) % m]) for c in range(m)]
        names = {v: i for i, v in enumerate(sorted(set(sig)))}
        new = [names[v] for v in sig]
        if len(set(new)) == len(set(part)):
            return len(set(new))
        part = new

def all_rules(p: int):
    k = 1 << p - 1
    for code in range(1 << k):
        yield [code >> u & 1 for u in range(k)]

def main() -> None:
    rng = random.Random(20261006)
    delta_exact = Fraction(1, 10)
    alphas = (0.0, 0.5, 1.0, 2.0, 3.0, math.inf)
    report = {'rules_checked': 0, 'exact_spectrum_failures': 0, 'stationarity_failures': 0, 'causal_state_failures': 0, 'moore_failures': 0, 'short_window_failures': 0, 'decisional_entropy_failures': 0, 'max_renyi_error': 0.0, 'max_excess_entropy_error': 0.0, 'max_mean_cycle_error': 0.0, 'by_p': {}}
    rule_sets = {p: list(all_rules(p)) for p in (2, 3, 4)}
    for p in (5, 6, 7):
        rule_sets[p] = [[rng.randrange(2) for _ in range(1 << p - 1)] for _ in range(12)]
    for p, rules in rule_sets.items():
        n_max = p + (6 if p <= 4 else 4)
        for g in rules:
            m = 1 << p
            report['rules_checked'] += 1
            col = [Fraction(0)] * m
            for c in range(m):
                for y in (0, 1):
                    col[c << 1 & m - 1 | y] += 1 - delta_exact if y == bayes(c, p, g) else delta_exact
            report['stationarity_failures'] += int(any((x != 1 for x in col)))
            for n in range(1, n_max + 1):
                probs = word_probabilities(p, g, n, delta_exact)
                if Counter(probs) != spectrum_formula(p, n, delta_exact):
                    report['exact_spectrum_failures'] += 1
                for a in alphas:
                    err = abs(renyi(probs, a) - (min(n, p) + max(n - p, 0) * h_alpha(0.1, a)))
                    report['max_renyi_error'] = max(report['max_renyi_error'], err)
            laws = set()
            ok = True
            for c in range(m):
                law = []
                for fut in range(m):
                    state, prob = (c, Fraction(1))
                    for shift in range(p - 1, -1, -1):
                        bit = fut >> shift & 1
                        prob *= 1 - delta_exact if bit == bayes(state, p, g) else delta_exact
                        state = state << 1 & m - 1 | bit
                    law.append(prob)
                laws.add(tuple(law))
                state = c
                for _ in range(p):
                    state = state << 1 & m - 1 | bayes(state, p, g)
                ok &= int(np.argmax([float(x) for x in law])) == state and law.count(max(law)) == 1
            report['causal_state_failures'] += int(len(laws) != m or not ok)
            for delta in (0.05, 0.2, 0.45):
                n = p + 3
                hn = renyi(word_probabilities(p, g, n, delta), 1.0)
                hn1 = renyi(word_probabilities(p, g, n + 1, delta), 1.0)
                excess = hn - n * (hn1 - hn)
                report['max_excess_entropy_error'] = max(report['max_excess_entropy_error'], abs(excess - p * (1 - h_alpha(delta, 1.0))))
            for delta in (0.1, 0.3):
                w = np.full((m, m), np.inf)
                for c in range(m):
                    for y in (0, 1):
                        w[c, c << 1 & m - 1 | y] = -math.log2(1 - delta if y == bayes(c, p, g) else delta)
                report['max_mean_cycle_error'] = max(report['max_mean_cycle_error'], abs(karp_min_mean_cycle(w) + math.log2(1 - delta)))
            probs = word_probabilities(p, g, p + 1, delta_exact)
            for k in range(0, p + 1):
                joint = Counter()
                for word, pr in enumerate(probs):
                    window = word >> 1 & (1 << k) - 1
                    joint[window, word & 1] += pr
                success = sum((max(joint[w, 0], joint[w, 1]) for w in range(1 << k)))
                target = Fraction(1, 2) if k < p else 1 - delta_exact
                report['short_window_failures'] += int(success != target)
            report['moore_failures'] += int(moore_states(p, g) != m)
            report['decisional_entropy_failures'] += int(sum((bayes(c, p, g) for c in range(m))) != m // 2)
        report['by_p'][str(p)] = {'rules': len(rules), 'max_block_length': n_max, 'exhaustive': p <= 4}
    report['all_exact_checks_pass'] = all((report[k] == 0 for k in report if k.endswith('failures')))
    OUT.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    if not report['all_exact_checks_pass'] or any((report[key] > 1e-10 for key in ('max_renyi_error', 'max_excess_entropy_error', 'max_mean_cycle_error'))):
        raise SystemExit('Entropy-profile validation failed')
if __name__ == '__main__':
    main()
