from collections import Counter
from itertools import product
import math
import unittest
import numpy as np
from predictive_complexity.estimation import collision_estimate, expected_majority_power, moment_variance, table_statistics
from predictive_complexity.stationary import FeedbackSource, fit_sparse_walsh, fwht

class StationaryTests(unittest.TestCase):

    def test_all_small_rules(self):
        for p in range(1, 5):
            m = 1 << p
            for code in range(1 << m // 2):
                g = np.array([code >> u & 1 for u in range(m // 2)])
                source = FeedbackSource(g, 0.1)
                columns = [0] * m
                b = [c >> p - 1 ^ int(g[c % (m // 2)]) for c in range(m)]
                for c in range(m):
                    for y in (0, 1):
                        columns[(c << 1) % m | y] += 9 if y == b[c] else 1
                self.assertEqual(columns, [10] * m)
                for q in range(4):
                    errors = Counter()
                    direct = []
                    for word in product((0, 1), repeat=p + q):
                        count = 0
                        for t in range(p, len(word)):
                            suffix = sum((word[j] << t - 1 - j for j in range(t - p + 1, t)))
                            count += word[t] != word[t - p] ^ int(g[suffix])
                        errors[count] += 1
                        direct.append(2 ** (-p) * 0.1 ** count * 0.9 ** (q - count))
                    self.assertEqual(errors, Counter({r: m * math.comb(q, r) for r in range(q + 1)}))
                    np.testing.assert_allclose(source.block_probabilities(p + q), direct, atol=1e-15)
                partition = b
                while True:
                    signatures = [(partition[c], partition[2 * c % m], partition[(2 * c + 1) % m]) for c in range(m)]
                    names = {v: j for j, v in enumerate(sorted(set(signatures)))}
                    refined = [names[v] for v in signatures]
                    if len(set(refined)) == len(set(partition)):
                        break
                    partition = refined
                self.assertEqual(len(set(refined)), m)

    def test_future_laws_and_excess_entropy(self):
        rng = np.random.default_rng(3291)
        for p in range(1, 5):
            m = 1 << p
            for delta in (0.05, 0.2, 0.45):
                for _ in range(3):
                    g = rng.integers(2, size=m // 2)
                    source = FeedbackSource(g, delta)
                    joint = source.block_probabilities(2 * p).reshape(m, m)
                    past = joint.sum(axis=1)
                    future = joint.sum(axis=0)
                    np.testing.assert_allclose(past, 1 / m, atol=1e-14)
                    np.testing.assert_allclose(future, 1 / m, atol=1e-14)
                    conditional = joint / past[:, None]
                    modes = np.argmax(conditional, axis=1)
                    self.assertEqual(len(set(modes)), m)
                    for c in range(m):
                        bits = [c >> j & 1 for j in reversed(range(p))]
                        for _ in range(p):
                            suffix = sum((bit << j for j, bit in enumerate(reversed(bits[1:]))))
                            bit = bits[0] ^ int(g[suffix])
                            bits = bits[1:] + [bit]
                        expected = sum((bit << j for j, bit in enumerate(reversed(bits))))
                        self.assertEqual(modes[c], expected)
                    np.testing.assert_allclose(conditional.max(axis=1), (1 - delta) ** p)
                    information = np.sum(joint * np.log2(joint / np.outer(past, future)))
                    binary_entropy = -delta * math.log2(delta) - (1 - delta) * math.log2(1 - delta)
                    self.assertAlmostEqual(information, p * (1 - binary_entropy), places=12)

    def test_sampler_alignment_and_noise(self):
        source = FeedbackSource(np.array([0, 1, 1, 1]), 0.2)
        c, y = source.sample(100000, np.random.default_rng(791))
        np.testing.assert_array_equal(c[1:], c[:-1] << 1 & 7 | y[:-1])
        errors = y ^ source.bayes_bits(c)
        self.assertLess(abs(float(errors.mean()) - 0.2), 0.005)
        self.assertLess(float(np.max(np.abs(np.bincount(c, minlength=8) / len(c) - 1 / 8))), 0.006)

    def test_transform_against_definition(self):
        values = np.array([3, -2, 0, 7, 1, -5, 2, 2])
        expected = [sum((int(values[u]) * (-1) ** (u & v).bit_count() for u in range(8))) for v in range(8)]
        np.testing.assert_array_equal(fwht(values), expected)
        np.testing.assert_array_equal(fwht(fwht(values)), 8 * values)

    def test_sparse_fit_and_full_fit(self):
        p = 4
        contexts = np.tile(np.arange(16), 3)
        labels = np.array([c >> 3 ^ (c & 5).bit_count() % 2 for c in contexts])
        truth = np.array([(u & 5).bit_count() % 2 for u in range(8)])
        np.testing.assert_array_equal(fit_sparse_walsh(contexts, labels, p, 1), truth)
        rng = np.random.default_rng(902)
        contexts = rng.integers(16, size=137)
        labels = rng.integers(0, 2, size=137)
        residual = labels ^ contexts >> 3
        _, votes = table_statistics(contexts & 7, residual, 8)
        np.testing.assert_array_equal(fit_sparse_walsh(contexts, labels, p, 8), votes < 0)

class EstimationTests(unittest.TestCase):

    def test_moment_mean_variance_and_majority_by_enumeration(self):
        m, n, delta = (2, 3, 0.2)
        moment_mean = moment_second = expected_power = 0.0
        for rule_tuple in product((0, 1), repeat=m):
            rule = np.array(rule_tuple)
            conditional_mean = conditional_second = 0.0
            for contexts_tuple in product(range(m), repeat=n):
                contexts = np.array(contexts_tuple)
                for error_tuple in product((0, 1), repeat=n):
                    errors = np.array(error_tuple)
                    probability = 1 / 2 ** m * (1 / m ** n) * delta ** sum(errors) * (1 - delta) ** (n - sum(errors))
                    labels = rule[contexts] ^ errors
                    estimate = collision_estimate(contexts, labels, m)
                    direct = m / math.comb(n, 2) * sum((int(contexts[i] == contexts[j]) * (-1) ** int(labels[i] + labels[j]) for i in range(n) for j in range(i + 1, n)))
                    self.assertAlmostEqual(estimate.raw_moment, direct)
                    conditional_mean += 2 ** m * probability * direct
                    conditional_second += 2 ** m * probability * direct * direct
                    moment_mean += probability * direct
                    moment_second += probability * direct * direct
                    _, votes = table_statistics(contexts, labels, m)
                    learned = (votes < 0).astype(int)
                    expected_power += probability * (delta + (1 - 2 * delta) * np.mean(learned == rule))
            self.assertAlmostEqual(conditional_mean, (1 - 2 * delta) ** 2)
            self.assertAlmostEqual(conditional_second - conditional_mean ** 2, moment_variance(n, m, delta))
        self.assertAlmostEqual(moment_mean, (1 - 2 * delta) ** 2)
        self.assertAlmostEqual(moment_second - moment_mean ** 2, moment_variance(n, m, delta))
        self.assertAlmostEqual(expected_power, expected_majority_power(n, m, delta), places=11)

    def test_estimator_does_not_need_rule_or_noise(self):
        contexts = np.array([0, 0, 1, 1, 1, 2])
        labels = np.array([0, 1, 0, 0, 1, 1])
        a = collision_estimate(contexts, labels, 4)
        modified = labels ^ (contexts == 1)
        self.assertEqual(a, collision_estimate(contexts, modified, 4))

    def test_clipping_and_interval_endpoints(self):
        for labels in (np.array([0, 0]), np.array([0, 1])):
            estimate = collision_estimate(np.array([0, 0]), labels, 4)
            self.assertTrue(0 <= estimate.lower <= estimate.entropy <= estimate.upper <= 1)
        self.assertEqual(expected_majority_power(0, 8, 0.1), 0.5)

    def test_occupancy_curve_denoses(self):
        values = [expected_majority_power(n, 32, 0.1) for n in (0, 1, 32, 128, 512)]
        self.assertTrue(all((a <= b for a, b in zip(values, values[1:]))))
        self.assertLess(abs(values[-1] - 0.9), 0.001)
if __name__ == '__main__':
    unittest.main()
