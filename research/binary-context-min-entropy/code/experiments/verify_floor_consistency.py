from itertools import combinations, product
from math import gcd, log2
from random import Random
from functools import reduce
TOL = 1e-10

def bits(p):
    return list(product((0, 1), repeat=p))

def shift(u, x):
    return u[1:] + (x,)

def sign_consistent(active_lags, sign_bits):
    d = reduce(gcd, active_lags)
    for q in (0, 1):
        if all((sign_bits[i] == q * (i // d) % 2 for i in active_lags)):
            return True
    return False

def transition_probability(u, x, beta, weights, sign_bits):
    prob = beta / 2
    p = len(u)
    for lag, weight in weights.items():
        lag_bit = u[p - lag]
        if x ^ lag_bit == sign_bits[lag]:
            prob += weight
    return prob

def karp_min_mean_cycle(p, beta, weights, sign_bits):
    contexts = bits(p)
    index = {u: n for n, u in enumerate(contexts)}
    n = len(contexts)
    edges_in = [[] for _ in range(n)]
    for u in contexts:
        src = index[u]
        for x in (0, 1):
            v = shift(u, x)
            dst = index[v]
            prob = transition_probability(u, x, beta, weights, sign_bits)
            edges_in[dst].append((src, -log2(prob)))
    dp = [[0.0] * n]
    for _ in range(n):
        prev = dp[-1]
        cur = [float('inf')] * n
        for v in range(n):
            cur[v] = min((prev[src] + cost for src, cost in edges_in[v]))
        dp.append(cur)
    best = float('inf')
    for v in range(n):
        candidate = max(((dp[n][v] - dp[k][v]) / (n - k) for k in range(n)))
        best = min(best, candidate)
    return best

def check_pattern(p, active_lags, sign_tuple, raw_weights):
    alpha = 0.7
    total_raw = sum(raw_weights)
    weights = {lag: alpha * raw / total_raw for lag, raw in zip(active_lags, raw_weights)}
    beta = 1 - alpha
    sign_bits = dict(zip(active_lags, sign_tuple))
    floor = -log2(1 - beta / 2)
    mmc = karp_min_mean_cycle(p, beta, weights, sign_bits)
    predicted_floor = sign_consistent(active_lags, sign_bits)
    observed_floor = abs(mmc - floor) <= TOL
    if predicted_floor != observed_floor:
        raise AssertionError(f'floor criterion mismatch: p={p}, active={active_lags}, signs={sign_bits}, predicted={predicted_floor}, mmc={mmc:.12f}, floor={floor:.12f}')
    if mmc + TOL < floor:
        raise AssertionError(f'Karp result violates universal floor: p={p}, active={active_lags}, signs={sign_bits}, mmc={mmc:.12f}, floor={floor:.12f}')

def exhaustive_equal_weight_checks(max_p=6):
    total = 0
    for p in range(1, max_p + 1):
        count = 0
        for size in range(1, p + 1):
            for active_lags in combinations(range(1, p + 1), size):
                for sign_tuple in product((0, 1), repeat=size):
                    check_pattern(p, active_lags, sign_tuple, [1.0] * size)
                    count += 1
        total += count
        print(f'p={p}: checked {count} equal-weight signed lag patterns')
    return total

def random_unequal_weight_checks(max_p=6, trials_per_p=80):
    rng = Random(1729)
    total = 0
    for p in range(1, max_p + 1):
        for _ in range(trials_per_p):
            active_lags = tuple((lag for lag in range(1, p + 1) if rng.random() < 0.55))
            if not active_lags:
                active_lags = (rng.randrange(1, p + 1),)
            sign_tuple = tuple((rng.randrange(2) for _ in active_lags))
            raw_weights = [0.1 + rng.random() for _ in active_lags]
            check_pattern(p, active_lags, sign_tuple, raw_weights)
            total += 1
        print(f'p={p}: checked {trials_per_p} random unequal-weight patterns')
    return total

def main():
    exhaustive = exhaustive_equal_weight_checks()
    random = random_unequal_weight_checks()
    print(f'noise-floor consistency criterion OK: {exhaustive} exhaustive + {random} random checks')
if __name__ == '__main__':
    main()
