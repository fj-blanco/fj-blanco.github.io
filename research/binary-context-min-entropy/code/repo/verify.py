from __future__ import annotations
import argparse
from itertools import combinations, product
from math import log2
from pathlib import Path
import numpy as np
from gbar import floor_compatible, karp_from_action_costs, karp_min_entropy, local_cost, two_run_envelope
TOLERANCE = 2e-10

def close(actual: float, expected: float, label: str) -> None:
    if abs(actual - expected) > TOLERANCE:
        raise AssertionError(f'{label}: {actual:.12g} != {expected:.12g}')

def verify_floor_criterion(max_order: int, workdir: Path | None) -> int:
    checks = 0
    alpha = 0.7
    for p in range(1, max_order + 1):
        for size in range(1, p + 1):
            for lags in combinations(range(1, p + 1), size):
                for signs in product((0, 1), repeat=size):
                    coefficients = [0.0] * p
                    for lag, sign in zip(lags, signs):
                        coefficients[lag - 1] = (-1 if sign else 1) * alpha / size
                    value = karp_min_entropy(coefficients, workdir)
                    floor = -log2((1.0 + alpha) / 2.0)
                    observed = abs(value - floor) <= TOLERANCE
                    expected = floor_compatible(lags, signs)
                    if observed != expected:
                        raise AssertionError(f'floor criterion failed for p={p}, lags={lags}, signs={signs}')
                    checks += 1
    return checks

def verify_order_two(workdir: Path | None) -> int:
    checks = 0
    for a, b in ((0.4, 0.2), (0.1, 0.5), (0.5, 0.3), (0.2, 0.2)):
        beta = 1.0 - a - b
        w1 = -log2(a + beta / 2.0)
        w2 = -log2(b + beta / 2.0)
        w12 = -log2(a + b + beta / 2.0)
        expected = min(w1, (w12 + w2) / 2.0)
        close(karp_min_entropy([-a, -b], workdir), expected, 'negative p=2')
        close(karp_min_entropy([a, -b], workdir), expected, 'mixed p=2')
        checks += 2
    return checks

def verify_closed_families(workdir: Path | None) -> int:
    checks = 0
    for alpha in (0.2, 0.5, 0.8):
        close(karp_min_entropy([-alpha / 3.0] * 3, workdir), local_cost(3, 2, alpha), 'negative p=3')
        close(karp_min_entropy([-alpha / 4.0] * 4, workdir), (1.0 + 2.0 * local_cost(4, 3, alpha)) / 3.0, 'negative p=4')
        checks += 2
        beta = 1.0 - alpha
        high = -log2(1.0 - beta / 2.0)
        for p in (2, 4, 6, 8):
            coefficients = [0.0] * p
            coefficients[0] = coefficients[-1] = -alpha / 2.0
            expected = ((p - 1) * high + 1.0) / p
            close(karp_min_entropy(coefficients, workdir), expected, 'endpoint lags')
            checks += 1
        for p in (3, 5, 7):
            coefficients = [0.0] * p
            coefficients[0] = coefficients[-1] = -alpha / 2.0
            close(karp_min_entropy(coefficients, workdir), high, 'odd endpoint lags')
            checks += 1
    return checks

def verify_two_lag_master(workdir: Path | None) -> int:
    checks = 0
    lag_pairs = ((1, 2), (1, 3), (2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (5, 6), (5, 7), (3, 8))
    weights = ((0.3, 0.3), (0.1, 0.6), (0.6, 0.1), (0.05, 0.9), (0.9, 0.05), (0.25, 0.5), (0.33, 0.66))
    for a, b in lag_pairs:
        for signs in product((0, 1), repeat=2):
            frustrated = (a * signs[1] + b * signs[0]) % 2 == 1
            if frustrated == floor_compatible((a, b), signs):
                raise AssertionError(f'parity test disagrees with the gcd criterion: {(a, b, signs)}')
            if not frustrated:
                continue
            for ga, gb in weights:
                beta = 1.0 - ga - gb
                wa = -log2(ga + beta / 2.0)
                wb = -log2(gb + beta / 2.0)
                wab = -log2(1.0 - beta / 2.0)
                expected = min(((a - 1) * wab + wa) / a, ((b - 1) * wab + wb) / b)
                coefficients = [0.0] * b
                coefficients[a - 1] = (-1 if signs[0] else 1) * ga
                coefficients[b - 1] = (-1 if signs[1] else 1) * gb
                close(karp_min_entropy(coefficients, workdir), expected, f'two-lag master ({a},{b})')
                checks += 1
    return checks

def verify_frustration_inequality(max_length: int=14) -> int:
    checks = 0
    pairs = ((1, 2, 0, 1), (2, 3, 1, 1), (3, 4, 1, 1), (2, 5, 1, 0), (3, 5, 1, 0), (4, 5, 1, 1))
    for a, b, sign_a, sign_b in pairs:
        tight = False
        for length in range(1, max_length + 1):
            for bits in range(1 << length):
                word = [bits >> i & 1 for i in range(length)]
                defects_a = sum((word[t] ^ word[(t - a) % length] != sign_a for t in range(length)))
                defects_b = sum((word[t] ^ word[(t - b) % length] != sign_b for t in range(length)))
                slack = b * defects_a + a * defects_b - length
                if slack < 0:
                    raise AssertionError(f'frustration inequality failed: {(a, b, sign_a, sign_b, word)}')
                tight = tight or slack == 0
        if not tight:
            raise AssertionError(f'frustration inequality never tight for {(a, b, sign_a, sign_b)}')
        checks += 1
    return checks

def verify_parity_example() -> int:
    alpha = 0.6
    beta = 1.0 - alpha
    costs = np.empty((2, 4), dtype=np.float64)
    for state in range(4):
        newest = state & 1
        oldest = state >> 1 & 1
        for output in (0, 1):
            rule_1 = output ^ newest
            rule_2 = output ^ newest ^ oldest
            probability = beta / 2.0
            probability += alpha / 2.0 if rule_1 == 1 else 0.0
            probability += alpha / 2.0 if rule_2 == 0 else 0.0
            costs[output, state] = -log2(probability)
    c2 = -log2(beta / 2.0 + alpha)
    close(karp_from_action_costs(costs), (1.0 + 2.0 * c2) / 3.0, 'parity example')
    return 1

def verify_order_four_certificate() -> int:
    potential = (0, -4, -1, -5, 0, -2, -3, -3, -3, -3, -2, 0, -5, -1, -4, 2)
    mask = 15
    for state in range(16):
        for output in (0, 1):
            target = state << 1 & mask | output
            disagreements = (state ^ (mask if output else 0)).bit_count()
            if 3 * disagreements + potential[target] - potential[state] > 8:
                raise AssertionError('order-four integer certificate failed')
    return 32

def verify_majorization_example() -> int:
    candidate = sorted((1, 1, 1, 1, 2, 2, 3, 3))
    competitor = sorted((1, 1, 2, 2, 2, 2, 3))
    close(sum((max(x - 2, 0) for x in candidate)) / 8.0, 1.0 / 4.0, 'stop loss')
    close(sum((max(x - 2, 0) for x in competitor)) / 7.0, 1.0 / 7.0, 'stop loss')
    return 2

def verify_two_run(max_order: int, workdir: Path | None) -> int:
    checks = 0
    for p in range(2, max_order + 1):
        for alpha in (0.2, 0.5, 0.8):
            value = karp_min_entropy([-alpha / p] * p, workdir)
            expected, _ = two_run_envelope(p, alpha)
            close(value, expected, f'two-run p={p}, alpha={alpha}')
            checks += 1
    return checks

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--floor-max-order', type=int, default=5)
    parser.add_argument('--karp-max-order', type=int, default=10)
    parser.add_argument('--karp-workdir', type=Path)
    args = parser.parse_args()
    groups = {'floor criterion': verify_floor_criterion(args.floor_max_order, args.karp_workdir), 'order-two formulas': verify_order_two(args.karp_workdir), 'two-lag master formula': verify_two_lag_master(args.karp_workdir), 'frustration inequality': verify_frustration_inequality(), 'closed families': verify_closed_families(args.karp_workdir), 'parity example': verify_parity_example(), 'p=4 certificate': verify_order_four_certificate(), 'majorization example': verify_majorization_example(), 'two-run envelope': verify_two_run(args.karp_max_order, args.karp_workdir)}
    for name, count in groups.items():
        print(f'{name}: {count} checks')
    print(f'all checks passed: {sum(groups.values())}')
if __name__ == '__main__':
    main()
