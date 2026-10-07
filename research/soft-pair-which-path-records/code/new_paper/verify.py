from __future__ import annotations
import itertools
import json
from pathlib import Path
import numpy as np
import scipy.sparse as sp
import sympy as sy
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, solve_ivp
from scipy.special import wofz

def pair_kernel(k: float | np.ndarray, p: float | np.ndarray, T: float, gap: float) -> complex | np.ndarray:
    z = gap * T
    delta = (np.asarray(k) - np.asarray(p)) * T / 2
    return -np.pi * T ** 2 * np.exp(-((np.asarray(k) + np.asarray(p)) * T) ** 2 / 4) * (wofz(-z + delta) + wofz(-z - delta)) / 2

def odd_pair_kernel(k, p, T, gap):
    q = (np.asarray(k) + np.asarray(p)) * T
    delta = (np.asarray(k) - np.asarray(p)) * T / 2
    za, zb = (-gap * T + delta, -gap * T - delta)
    wa, wb = (wofz(za), wofz(zb))
    second = (4 * za ** 2 - 2) * wa + (4 * zb ** 2 - 2) * wb - 4j * (za + zb) / np.sqrt(np.pi)
    return -np.pi * T ** 2 / 2 * np.exp(-q ** 2 / 4) * ((0.5 - q ** 2 / 4) * (wa + wb) + second / 4)

def odd_time_integral_check():
    T, gap, k, p = (0.8, 1.7, 0.4, 0.9)
    q = (k + p) * T
    prefactor = -np.sqrt(np.pi) * T * np.exp(-q ** 2 / 4)

    def integrand(r):
        return np.exp(-r ** 2 / (4 * T ** 2) - 1j * gap * r) * np.cos((k - p) * r / 2) * (0.5 - q ** 2 / 4 - r ** 2 / (4 * T ** 2))
    direct = prefactor * (quad(lambda r: integrand(r).real, 0, np.inf, epsabs=1e-12)[0] + 1j * quad(lambda r: integrand(r).imag, 0, np.inf, epsabs=1e-12)[0])
    return float(abs(direct - odd_pair_kernel(k, p, T, gap)))

def one_minus_sinc(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x)
    y = x * x
    return np.where(np.abs(x) < 0.03, y / 6 - y ** 2 / 120 + y ** 3 / 5040 - y ** 4 / 362880, 1 - np.sinc(x / np.pi))

def pair_coefficient(T: float, gap: float=1.0, distance: float=1.0, width: float=0.2, order: int=160, kernel=pair_kernel) -> float:
    nodes, weights = leggauss(order)
    q = 6 * (nodes + 1)
    wq = 6 * weights
    x = (nodes + 1) / 2
    wx = weights / 2
    a = q[:, None] * x[None, :]
    b = q[:, None] * (1 - x[None, :])
    k, p = (a / T, b / T)
    da, db = (one_minus_sinc(k * distance), one_minus_sinc(p * distance))
    geometry = da + db - da * db
    form = np.exp(-width ** 2 * (k ** 2 + p ** 2))
    integrand = q[:, None] ** 3 * x[None, :] * (1 - x[None, :]) * form * np.abs(kernel(k, p, T, gap)) ** 2 * geometry
    return float(np.sum(wq[:, None] * wx[None, :] * integrand) / (8 * np.pi ** 4 * T ** 4))

def first_order_scaled_ratio(T: float, gap: float=1.0, distance: float=1.0, width: float=0.2) -> float:

    def integrand(z: float) -> float:
        k = z / (2 * gap * T ** 2)
        geom = float(one_minus_sinc(np.array(k * distance)))
        return k * np.exp(-z - T ** 2 * k ** 2 - width ** 2 * k ** 2) * geom / (2 * gap * T ** 2)
    scaled = T ** 2 / (2 * np.pi) * quad(integrand, 0, 70, epsabs=1e-28, epsrel=1e-10)[0]
    asymptotic_scaled = distance ** 2 / (32 * np.pi * gap ** 4 * T ** 6)
    return scaled / asymptotic_scaled

def time_integral_check() -> float:
    T, gap, k, p = (0.8, 1.7, 0.4, 0.9)
    prefactor = -np.sqrt(np.pi) * T * np.exp(-((k + p) * T) ** 2 / 4)

    def integrand(r: float) -> complex:
        return np.exp(-r ** 2 / (4 * T ** 2) - 1j * gap * r) * np.cos((k - p) * r / 2)
    direct = prefactor * (quad(lambda r: integrand(r).real, 0, np.inf, epsabs=1e-12)[0] + 1j * quad(lambda r: integrand(r).imag, 0, np.inf, epsabs=1e-12)[0])
    return float(abs(direct - pair_kernel(k, p, T, gap)))

def fock_dyson_check() -> dict[str, float]:
    momenta = np.array([0.4, -0.4, 0.7, -0.7])
    energies = np.abs(momenta)
    couplings = np.array([0.2, 0.2, 0.16, 0.16])
    gap, T, distance = (2.3, 0.9, 1.2)
    basis = [n for n in itertools.product(range(5), repeat=4) if sum(n) <= 4]
    lookup = {n: i for i, n in enumerate(basis)}
    count = len(basis)
    annihilation = []
    for j in range(4):
        matrix = np.zeros((count, count))
        for n, column in lookup.items():
            if n[j]:
                lowered = list(n)
                lowered[j] -= 1
                matrix[lookup[tuple(lowered)], column] = np.sqrt(n[j])
        annihilation.append(sp.csr_matrix(matrix))
    plus = sp.csr_matrix([[0, 0], [1, 0]])
    minus = plus.T
    terms = []
    branch_b_phases = []
    for g, k, a, spatial_k in zip(couplings, energies, annihilation, momenta):
        creation_phase = np.exp(-1j * spatial_k * distance)
        branch_b_phases.extend([creation_phase.conjugate(), creation_phase, creation_phase.conjugate(), creation_phase])
        terms.extend([(gap - k, g * sp.kron(plus, a)), (gap + k, g * sp.kron(plus, a.T)), (-gap - k, g * sp.kron(minus, a)), (-gap + k, g * sp.kron(minus, a.T))])
    dim = 2 * count
    initial = np.zeros((5, dim), dtype=complex)
    initial[0, lookup[0, 0, 0, 0]] = 1

    def rhs(t: float, vector: np.ndarray) -> np.ndarray:
        state = vector.reshape(5, dim)
        previous = state[:-1].T
        evolved = np.zeros_like(previous)
        for frequency, matrix in terms:
            evolved += np.exp(1j * frequency * t) * (matrix @ previous)
        derivative = np.zeros_like(state)
        derivative[1:] = -1j * np.exp(-t ** 2 / (2 * T ** 2)) * evolved.T
        return derivative.ravel()
    solution = solve_ivp(rhs, (-8 * T, 8 * T), initial.ravel(), rtol=2e-11, atol=2e-13, method='DOP853')
    if not solution.success:
        raise RuntimeError(solution.message)
    state = solution.y[:, -1].reshape(5, dim)
    first_order_error = 0.0
    for j, (g, energy) in enumerate(zip(couplings, energies)):
        occupancy = [0, 0, 0, 0]
        occupancy[j] = 1
        expected = -1j * g * np.sqrt(2 * np.pi) * T * np.exp(-((gap + energy) * T) ** 2 / 2)
        actual = state[1, count + lookup[tuple(occupancy)]]
        first_order_error = max(first_order_error, abs(actual - expected))
    largest_pair_error = 0.0
    for j in range(4):
        for m in range(j, 4):
            n = [0, 0, 0, 0]
            n[j] += 1
            n[m] += 1
            factor = np.sqrt(2) if j == m else 2
            expected = factor * couplings[j] * couplings[m] * pair_kernel(energies[j], energies[m], T, gap)
            actual = state[2, lookup[tuple(n)]]
            largest_pair_error = max(largest_pair_error, abs(actual - expected))
    norm2 = 2 * np.vdot(state[0], state[2]).real + np.vdot(state[1], state[1]).real
    norm4 = 2 * np.vdot(state[0], state[4]).real + 2 * np.vdot(state[1], state[3]).real + np.vdot(state[2], state[2]).real
    momentum = np.array([np.dot(n, momenta) for n in basis])
    operator = np.tile(1 - np.cos(distance * momentum), 2)
    vacuum = lookup[0, 0, 0, 0]
    pair_v4 = float(np.vdot(state[2], operator * state[2]).real)
    one_three = float(2 * np.vdot(state[1], operator * state[3]).real)
    v2 = float(np.vdot(state[1], operator * state[1]).real)
    translation = np.tile(np.exp(-1j * distance * momentum), 2)
    direct_coefficient = -sum((np.vdot(state[m], translation * state[4 - m]) for m in range(5))).real
    result = {'maximum_first_order_amplitude_absolute_error': float(first_order_error), 'maximum_pair_amplitude_absolute_error': float(largest_pair_error), 'unitarity_order_2_error': float(abs(norm2)), 'unitarity_order_4_error': float(abs(norm4)), 'vacuum_path_weight': float(operator[vacuum]), 'pair_visibility_coefficient': pair_v4, 'one_three_interference_coefficient': one_three, 'fourth_order_branch_overlap_error': float(abs(direct_coefficient - pair_v4 - one_three)), 'full_evolution': []}
    for coupling in (0.08, 0.04):

        def full_rhs(t, vector):
            branches = vector.reshape(2, dim)
            evolved = np.zeros_like(branches)
            for (frequency, matrix), branch_phase in zip(terms, branch_b_phases):
                phase = np.exp(1j * frequency * t)
                evolved[0] += phase * (matrix @ branches[0])
                evolved[1] += phase * branch_phase * (matrix @ branches[1])
            return (-1j * coupling * np.exp(-t ** 2 / (2 * T ** 2)) * evolved).ravel()
        initial_branches = np.tile(initial[0], (2, 1))
        full = solve_ivp(full_rhs, (-8 * T, 8 * T), initial_branches.ravel(), rtol=3e-12, atol=3e-14, method='DOP853')
        if not full.success:
            raise RuntimeError(full.message)
        branch_a, branch_b = full.y[:, -1].reshape(2, dim)
        loss = 1 - abs(np.vdot(branch_a, branch_b))
        predicted = coupling ** 2 * v2 + coupling ** 4 * (pair_v4 + one_three)
        ground_prob = float(np.vdot(branch_a[:count], branch_a[:count]).real)
        conditional_loss = 1 - abs(np.vdot(branch_a[:count], branch_b[:count])) / ground_prob
        excited_prob = float(np.vdot(branch_a[count:], branch_a[count:]).real)
        result['full_evolution'].append({'lambda': coupling, 'visibility_loss': float(loss), 'fourth_order_prediction': predicted, 'remainder': float(loss - predicted), 'translation_identity_error': float(abs(loss - np.vdot(branch_a, operator * branch_a).real)), 'ground_conditioned_loss_over_pair_prediction': float(conditional_loss / (coupling ** 4 * pair_v4)), 'conditioning_bound_satisfied': bool(abs(conditional_loss - loss) <= 2 * excited_prob / (1 - excited_prob) + 1e-12)})
    result['remainder_halving_ratio'] = result['full_evolution'][0]['remainder'] / result['full_evolution'][1]['remainder']
    return result

def main() -> None:
    x, q = sy.symbols('x q', positive=True)
    angular_moment = sy.integrate(x * (1 - x) * (x ** 2 + (1 - x) ** 2), (x, 0, 1))
    gaussian_moment = sy.integrate(sy.pi * q ** 5 * sy.exp(-q ** 2 / 2), (q, 0, sy.oo))
    assert angular_moment == sy.Rational(1, 10)
    assert sy.simplify(gaussian_moment - 8 * sy.pi) == 0
    gaussian_coefficient = sy.simplify(angular_moment * gaussian_moment / (48 * sy.pi ** 4))
    assert gaussian_coefficient == 1 / (60 * sy.pi ** 3)
    result = {'angular_moment': str(angular_moment), 'gaussian_spectral_moment': str(gaussian_moment), 'gaussian_coefficient': str(gaussian_coefficient), 'time_integral_absolute_error': time_integral_check(), 'fock_dyson': fock_dyson_check(), 'continuum_convergence': []}
    for T in (2, 4, 8, 16, 32, 64, 128):
        numerical = pair_coefficient(T)
        predicted = 1 / (60 * np.pi ** 3 * T ** 4)
        result['continuum_convergence'].append({'T': T, 'pair_exact_over_asymptotic': numerical / predicted, 'one_quantum_exact_over_asymptotic': first_order_scaled_ratio(T)})
    assert result['time_integral_absolute_error'] < 1e-10
    assert result['fock_dyson']['maximum_pair_amplitude_absolute_error'] < 1e-09
    assert result['fock_dyson']['unitarity_order_4_error'] < 1e-09
    assert abs(result['continuum_convergence'][-1]['pair_exact_over_asymptotic'] - 1) < 0.0003
    odd_moment = sy.integrate(sy.pi * q ** 5 * (sy.Rational(1, 2) - q ** 2 / 4) ** 2 * sy.exp(-q ** 2 / 2), (q, 0, sy.oo))
    assert odd_moment == 14 * sy.pi
    result['odd_pulse'] = {'spectral_moment': str(odd_moment), 'time_integral_absolute_error': odd_time_integral_check(), 'convergence': []}
    for T in (8, 32, 128):
        ratio = pair_coefficient(T, kernel=odd_pair_kernel) / (7 / (240 * np.pi ** 3 * T ** 4))
        result['odd_pulse']['convergence'].append({'T': T, 'pair_exact_over_asymptotic': ratio})
    result['spatial_width_checks'] = [{'width': w, 'ratio_at_T128': pair_coefficient(128, width=w) / (1 / (60 * np.pi ** 3 * 128 ** 4))} for w in (0.2, 1.0, 3.0)]
    result['coincident_branches_loss'] = pair_coefficient(8, distance=0)
    result['quadrature_refinement_relative_change'] = abs(pair_coefficient(8, order=100) / pair_coefficient(8, order=160) - 1)
    assert result['fock_dyson']['maximum_first_order_amplitude_absolute_error'] < 1e-09
    assert abs(result['continuum_convergence'][-1]['one_quantum_exact_over_asymptotic'] - 1) < 0.0005
    assert result['fock_dyson']['unitarity_order_2_error'] < 1e-09
    assert result['fock_dyson']['fourth_order_branch_overlap_error'] < 1e-09
    assert all((r['translation_identity_error'] < 1e-10 and r['conditioning_bound_satisfied'] for r in result['fock_dyson']['full_evolution']))
    assert abs(result['fock_dyson']['remainder_halving_ratio'] - 64) < 2
    assert abs(result['fock_dyson']['full_evolution'][-1]['ground_conditioned_loss_over_pair_prediction'] - 1) < 0.005
    assert result['odd_pulse']['time_integral_absolute_error'] < 1e-10
    assert abs(result['odd_pulse']['convergence'][-1]['pair_exact_over_asymptotic'] - 1) < 0.001
    assert all((abs(r['ratio_at_T128'] - 1) < 0.005 for r in result['spatial_width_checks']))
    assert result['coincident_branches_loss'] == 0
    assert result['quadrature_refinement_relative_change'] < 1e-08
    output = Path(__file__).with_name('checks.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
if __name__ == '__main__':
    main()
