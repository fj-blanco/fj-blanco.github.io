import math
import unittest
import numpy as np
from predictive_complexity.metrics import evaluate_predictions

class EvaluationTests(unittest.TestCase):

    def test_test_labels_cannot_flip_the_predictor(self):
        result = evaluate_predictions(np.array([0, 0, 0, 1]), np.ones(4), 0.1)
        self.assertEqual(result['p_ml'], 0.25)
        self.assertEqual(result['accessible_min_entropy'], 2.0)

    def test_always_wrong_predictor_has_zero_success(self):
        result = evaluate_predictions(np.array([0, 1]), np.array([1, 0]), 0.1)
        self.assertEqual(result['p_ml'], 0.0)
        self.assertTrue(math.isinf(result['accessible_min_entropy']))
if __name__ == '__main__':
    unittest.main()
