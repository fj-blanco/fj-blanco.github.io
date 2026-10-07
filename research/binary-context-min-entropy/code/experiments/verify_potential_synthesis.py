from __future__ import annotations
from itertools import product
from math import log2
from random import Random
Context = tuple[int, ...]
TOL = 1e-10

def contexts(p: int) -> list[Context]:
    return list(product((0, 1), repeat=p))

def shift(context: Context, x_value: int) -> Context:
    return context[1:] + (x_value,)

def transition_probability(context: Context, x_value: int, alphas: list[float]) -> float:
    p = len(alphas)
    beta = 1.0 - sum((abs(value) for value in alphas))
    probability = beta / 2.0
    for lag, coefficient in enumerate(alphas, start=1):
        past_value = context[p - lag]
        if coefficient > 0 and x_value == past_value:
            probability += coefficient
        if coefficient < 0 and x_value != past_value:
            probability += -coefficient
    return probability

def graph_edges(alphas: list[float]) -> tuple[list[Context], list[tuple[int, int, float]]]:
    nodes = contexts(len(alphas))
    index = {node: i for i, node in enumerate(nodes)}
    edges: list[tuple[int, int, float]] = []
    for context in nodes:
        source = index[context]
        for x_value in (0, 1):
            target = index[shift(context, x_value)]
            probability = transition_probability(context, x_value, alphas)
            edges.append((source, target, -log2(probability)))
    return (nodes, edges)

def karp_min_mean_cycle(n_nodes: int, edges: list[tuple[int, int, float]]) -> float:
    incoming: list[list[tuple[int, float]]] = [[] for _ in range(n_nodes)]
    for source, target, weight in edges:
        incoming[target].append((source, weight))
    distances = [[0.0] * n_nodes]
    for _ in range(n_nodes):
        previous = distances[-1]
        current = [float('inf')] * n_nodes
        for target in range(n_nodes):
            current[target] = min((previous[source] + weight for source, weight in incoming[target]))
        distances.append(current)
    best = float('inf')
    for node in range(n_nodes):
        local = max(((distances[n_nodes][node] - distances[k][node]) / (n_nodes - k) for k in range(n_nodes)))
        best = min(best, local)
    return best

def synthesize_potential(n_nodes: int, edges: list[tuple[int, int, float]], lambda_value: float) -> list[float]:
    potential = [0.0] * n_nodes
    for _ in range(n_nodes - 1):
        changed = False
        for source, target, weight in edges:
            shifted = weight - lambda_value
            candidate = potential[source] + shifted
            if candidate < potential[target] - TOL:
                potential[target] = candidate
                changed = True
        if not changed:
            break
    for source, target, weight in edges:
        if potential[source] + weight - lambda_value < potential[target] - 1e-08:
            raise AssertionError('shifted graph has a negative cycle')
    return potential

def verify_certificate(name: str, alphas: list[float]) -> None:
    nodes, edges = graph_edges(alphas)
    lambda_value = karp_min_mean_cycle(len(nodes), edges)
    potential = synthesize_potential(len(nodes), edges, lambda_value)
    min_slack = float('inf')
    tight_edges = 0
    for source, target, weight in edges:
        reduced = weight + potential[source] - potential[target]
        slack = reduced - lambda_value
        min_slack = min(min_slack, slack)
        if abs(slack) <= 1e-08:
            tight_edges += 1
        if slack < -1e-08:
            raise AssertionError(f'{name}: negative reduced slack {slack:.3e} on {nodes[source]} -> {nodes[target]}')
    span = max(potential) - min(potential)
    print(f'{name:32s} OK  p={len(alphas):2d}  lambda={lambda_value:.12f}  min_slack={min_slack:.3e}  tight_edges={tight_edges:4d}  potential_span={span:.6f}')

def alternating_sign(p: int, alpha: float) -> list[float]:
    return [(-1) ** (p - lag) * alpha / p for lag in range(1, p + 1)]

def block_negative_balanced(p: int, alpha: float) -> list[float]:
    return [-alpha / p if lag <= p // 2 else alpha / p for lag in range(1, p + 1)]

def random_gbar(p: int, rng: Random) -> list[float]:
    active = [lag for lag in range(1, p + 1) if rng.random() < 0.75]
    if not active:
        active = [rng.randrange(1, p + 1)]
    raw = [0.1 + rng.random() for _ in active]
    alpha = 0.75
    alphas = [0.0] * p
    for lag, weight in zip(active, raw):
        sign = -1 if rng.random() < 0.5 else 1
        alphas[lag - 1] = sign * alpha * weight / sum(raw)
    return alphas

def main() -> None:
    named_cases = [('positive p=5', [0.1] * 5), ('even alternating p=6', alternating_sign(6, 0.6)), ('odd alternating p=5', alternating_sign(5, 0.6)), ('odd alternating p=7', alternating_sign(7, 0.6)), ('pure negative p=4', [-0.15] * 4), ('dual endpoint p=8', [-0.2, 0, 0, 0, 0, 0, 0, -0.2]), ('block negative balanced p=6', block_negative_balanced(6, 0.6))]
    for name, alphas in named_cases:
        verify_certificate(name, alphas)
    rng = Random(20260605)
    for p in range(2, 8):
        for trial in range(10):
            verify_certificate(f'random p={p} #{trial}', random_gbar(p, rng))
    print('potential synthesis OK')
if __name__ == '__main__':
    main()
