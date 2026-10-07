from itertools import product
import math
TOL = 1e-12

def bits(p):
    return list(product((0, 1), repeat=p))

def shift(u, x):
    return u[1:] + (x,)

def log_cost(prob):
    return -math.log2(prob)

def assert_certificate(name, contexts, edge_cost, potential, lam):
    worst_margin = float('inf')
    worst_edge = None
    equality_edges = 0
    for u in contexts:
        for x in (0, 1):
            v = shift(u, x)
            reduced = edge_cost(u, x) + potential(u) - potential(v)
            margin = reduced - lam
            if margin < worst_margin:
                worst_margin = margin
                worst_edge = (u, x, v, reduced)
            if abs(margin) <= 1e-09:
                equality_edges += 1
    if worst_margin < -TOL:
        u, x, v, reduced = worst_edge
        raise AssertionError(f'{name}: reduced-cost inequality failed on {u} --{x}--> {v}: reduced={reduced:.12f}, lambda={lam:.12f}, margin={worst_margin:.3e}')
    print(f'{name:34s} OK  lambda={lam:.12f}  min_margin={worst_margin:.3e}  equality_edges={equality_edges}')

def verify_negative_p2(alpha):
    p = 2
    beta = 1 - alpha
    w_h = log_cost(1 - beta / 2)
    lam = (w_h + 1) / 2

    def edge_cost(u, x):
        disagreements = sum((1 for ui in u if x != ui))
        return log_cost(beta / 2 + alpha / p * disagreements)

    def potential(u):
        return 0.0 if u in ((0, 1), (1, 0)) else (1 - w_h) / 2
    assert_certificate(f'negative p=2 alpha={alpha}', bits(p), edge_cost, potential, lam)

def verify_negative_p3(alpha):
    p = 3
    beta = 1 - alpha

    def p_d(d):
        return beta / 2 + alpha * d / p
    c2 = log_cost(p_d(2))
    c3 = log_cost(p_d(3))
    lam = c2

    def edge_cost(u, x):
        disagreements = sum((1 for ui in u if x != ui))
        return log_cost(p_d(disagreements))

    def potential(u):
        return c2 - c3 if sum(u) in (0, 3) else 0.0
    assert_certificate(f'negative p=3 alpha={alpha}', bits(p), edge_cost, potential, lam)

def verify_mixed_sign_p2(a, b):
    beta = 1 - a - b
    if beta <= 0:
        raise ValueError('mixed-sign parameters require a+b<1')
    r = log_cost(a + beta / 2)
    s = log_cost(b + beta / 2)
    h = log_cost(1 - beta / 2)
    lam = min(r, (s + h) / 2)
    if (s + h) / 2 <= r:
        phi_diff = (s - h) / 2
    else:
        phi_diff = r - h

    def edge_cost(u, x):
        return log_cost(a * (x == u[1]) + b * (x != u[0]) + beta / 2)

    def potential(u):
        return phi_diff if u in ((0, 1), (1, 0)) else 0.0
    assert_certificate(f'mixed p=2 a={a}, b={b}', bits(2), edge_cost, potential, lam)

def longest_alternating_suffix(u):
    length = 1
    for i in range(len(u) - 1, 0, -1):
        if u[i] != u[i - 1]:
            length += 1
        else:
            break
    return length

def verify_dual_endpoint(p, gamma):
    beta = 1 - 2 * gamma
    w_h = log_cost(1 - beta / 2)
    delta = (1 - w_h) / p
    lam = w_h + delta

    def edge_cost(u, x):
        prob = gamma * (x != u[-1]) + gamma * (x != u[0]) + beta / 2
        return log_cost(prob)

    def potential(u):
        return (p - longest_alternating_suffix(u)) * delta
    assert_certificate(f'dual endpoint p={p}, gamma={gamma}', bits(p), edge_cost, potential, lam)

def main():
    for alpha in (0.1, 0.5, 0.9):
        verify_negative_p2(alpha)
        verify_negative_p3(alpha)
    for a, b in ((0.4, 0.2), (0.1, 0.5), (0.5, 0.3)):
        verify_mixed_sign_p2(a, b)
    for p in (2, 4, 6, 8, 10):
        for gamma in (0.05, 0.2, 0.49):
            verify_dual_endpoint(p, gamma)
if __name__ == '__main__':
    main()
