import math
from statistics import NormalDist
import numpy as np

def detector_checks():
    phi = NormalDist()
    for n in (1, 3, 20):
        for delta in (0.01, 0.1, 0.4):
            mu, var = (1.3, 0.7)
            cutoff = mu - math.sqrt(var / n) * phi.inv_cdf(1 - delta)
            completeness = 1 - phi.cdf((cutoff - mu) / math.sqrt(var / n))
            q = 1 - phi.cdf(cutoff / math.sqrt(var / n))
            q_formula = 0.5 * math.erfc((math.sqrt(n) * mu / math.sqrt(var) - phi.inv_cdf(1 - delta)) / math.sqrt(2))
            assert abs(completeness - (1 - delta)) < 1e-14
            assert abs(q - q_formula) < 1e-14
    for x in np.linspace(0, 12, 1000):
        assert math.erfc(x / math.sqrt(2)) / 2 <= math.exp(-x * x / 2) / 2 + 1e-15
    print('Gaussian threshold completeness, false acceptance, and tail bound verified')
if __name__ == '__main__':
    detector_checks()
