from __future__ import annotations
import sys
from itertools import product
from math import log2
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'repo'))
from gbar import floor_compatible, karp_min_entropy
TOLERANCE = 1e-09

def frustrated(a: int, b: int, sa: int, sb: int) -> bool:
    return (a * sb + b * sa) % 2 == 1

def master(a: int, b: int, ga: float, gb: float) -> float:
    beta = 1.0 - ga - gb
    wa = -log2(ga + beta / 2.0)
    wb = -log2(gb + beta / 2.0)
    wab = -log2(ga + gb + beta / 2.0)
    return min(((a - 1) * wab + wa) / a, ((b - 1) * wab + wb) / b)

def check_formula() -> int:
    lag_pairs = [(1, 2), (1, 3), (1, 4), (1, 6), (2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 6), (2, 7), (4, 7), (5, 7), (6, 7), (3, 8), (7, 8)]
    weights = [(0.1, 0.1), (0.3, 0.3), (0.45, 0.45), (0.1, 0.6), (0.6, 0.1), (0.05, 0.9), (0.9, 0.05), (0.25, 0.5), (0.5, 0.25), (0.4, 0.55), (0.02, 0.02), (0.33, 0.66)]
    checks = 0
    for a, b in lag_pairs:
        for sa, sb in product((0, 1), repeat=2):
            if frustrated(a, b, sa, sb) == floor_compatible((a, b), (sa, sb)):
                raise AssertionError(f'parity test disagrees with gcd criterion: {(a, b, sa, sb)}')
            if not frustrated(a, b, sa, sb):
                continue
            for ga, gb in weights:
                if ga + gb >= 0.999:
                    continue
                coefficients = [0.0] * b
                coefficients[a - 1] = (-1 if sa else 1) * ga
                coefficients[b - 1] = (-1 if sb else 1) * gb
                value = karp_min_entropy(coefficients)
                expected = master(a, b, ga, gb)
                if abs(value - expected) > TOLERANCE:
                    raise AssertionError(f'master formula failed: lags=({a},{b}) s=({sa},{sb}) g=({ga},{gb}): {value:.12g} != {expected:.12g}')
                checks += 1
    return checks

def check_frustration_inequality(max_length: int=14) -> int:
    pairs = [(1, 2, 0, 1), (1, 2, 1, 1), (2, 3, 1, 0), (2, 3, 1, 1), (3, 4, 1, 1), (3, 4, 0, 1), (2, 5, 1, 0), (2, 5, 1, 1), (3, 5, 1, 0), (4, 5, 1, 1), (4, 5, 1, 0), (5, 6, 1, 1)]
    checks = 0
    for a, b, sa, sb in pairs:
        assert frustrated(a, b, sa, sb)
        tight = False
        for length in range(1, max_length + 1):
            for bits in range(1 << length):
                y = [bits >> i & 1 for i in range(length)]
                defects_a = sum((y[t] ^ y[(t - a) % length] != sa for t in range(length)))
                defects_b = sum((y[t] ^ y[(t - b) % length] != sb for t in range(length)))
                slack = b * defects_a + a * defects_b - length
                if slack < 0:
                    raise AssertionError(f'frustration inequality violated: lags=({a},{b}) s=({sa},{sb}) word={y}')
                tight = tight or slack == 0
                checks += 1
        if not tight:
            raise AssertionError(f'inequality never tight for lags=({a},{b}) s=({sa},{sb})')
    return checks

def main() -> None:
    print(f'master formula: {check_formula()} frustrated cases match Karp')
    print(f'frustration inequality: {check_frustration_inequality()} words checked, tight in every pair')
if __name__ == '__main__':
    main()
