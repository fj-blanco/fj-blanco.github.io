#include <errno.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static double local_cost(int p, int disagreements, double alpha) {
    double probability = (1.0 - alpha) / 2.0 + alpha * disagreements / p;
    return -log2(probability);
}

static double two_run_rate(int p, int run_length, double alpha) {
    double total = 0.0;
    for (int m = p - run_length + 1; m < run_length; ++m) {
        total += local_cost(p, m, alpha);
    }
    total += (p - run_length + 1) * local_cost(p, run_length, alpha);
    return total / run_length;
}

static double envelope(int p, double alpha, int *best_run) {
    double best = INFINITY;
    for (int run = p / 2 + 1; run <= p; ++run) {
        double value = two_run_rate(p, run, alpha);
        if (value < best) {
            best = value;
            *best_run = run;
        }
    }
    return best;
}

static int certify(int p, double alpha, int max_iterations) {
    uint64_t n = UINT64_C(1) << p;
    uint64_t high_bit = UINT64_C(1) << (p - 1);
    uint64_t mask = n - 1;
    double *distance = calloc((size_t)n, sizeof(*distance));
    double *next = malloc((size_t)n * sizeof(*next));
    double costs[65];
    int best_run = 0;
    int iterations = 0;

    if (distance == NULL || next == NULL) {
        fprintf(stderr, "allocation failed for p=%d: %s\n", p, strerror(errno));
        free(distance);
        free(next);
        return 2;
    }
    for (int m = 0; m <= p; ++m) {
        costs[m] = local_cost(p, m, alpha);
    }
    double rate = envelope(p, alpha, &best_run);

    for (; iterations < max_iterations; ++iterations) {
        double max_drop = 0.0;
#pragma omp parallel for reduction(max : max_drop) schedule(static)
        for (uint64_t target = 0; target < n; ++target) {
            uint64_t predecessor_0 = target >> 1;
            uint64_t predecessor_1 = predecessor_0 | high_bit;
            int output = (int)(target & 1);
            int count_0 = __builtin_popcountll(predecessor_0);
            int count_1 = __builtin_popcountll(predecessor_1);
            int m_0 = output ? p - count_0 : count_0;
            int m_1 = output ? p - count_1 : count_1;
            double value = distance[target];
            double candidate = distance[predecessor_0] + costs[m_0] - rate;
            if (candidate < value) {
                value = candidate;
            }
            candidate = distance[predecessor_1] + costs[m_1] - rate;
            if (candidate < value) {
                value = candidate;
            }
            next[target] = value;
            double drop = distance[target] - value;
            if (drop > max_drop) {
                max_drop = drop;
            }
        }
        double *swap = distance;
        distance = next;
        next = swap;
        if (max_drop <= 1.0e-13) {
            ++iterations;
            break;
        }
    }

    double min_slack = INFINITY;
#pragma omp parallel for reduction(min : min_slack) schedule(static)
    for (uint64_t state = 0; state < n; ++state) {
        uint64_t successor_0 = (state << 1) & mask;
        uint64_t successor_1 = successor_0 | 1;
        int count = __builtin_popcountll(state);
        double slack_0 = costs[count] + distance[state] - distance[successor_0] - rate;
        double slack_1 = costs[p - count] + distance[state] - distance[successor_1] - rate;
        if (slack_0 < min_slack) {
            min_slack = slack_0;
        }
        if (slack_1 < min_slack) {
            min_slack = slack_1;
        }
    }

    const char *status = min_slack >= -1.0e-9 && iterations < max_iterations ? "ok" : "failed";
    printf("%d,%.12g,%d,%.12g,%d,%.6g,%s\n", p, alpha, best_run, rate,
           iterations, min_slack, status);
    free(distance);
    free(next);
    return strcmp(status, "ok") == 0 ? 0 : 1;
}

static int parse_int(const char *text, const char *name) {
    char *end = NULL;
    long value = strtol(text, &end, 10);
    if (*text == '\0' || *end != '\0' || value < 1 || value > 30) {
        fprintf(stderr, "invalid %s: %s\n", name, text);
        exit(2);
    }
    return (int)value;
}

int main(int argc, char **argv) {
    int min_order = 2;
    int max_order = 16;
    int max_iterations = 10000;
    const double alphas[] = {0.2, 0.5, 0.8};

    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--min-order") == 0 && i + 1 < argc) {
            min_order = parse_int(argv[++i], "minimum order");
        } else if (strcmp(argv[i], "--max-order") == 0 && i + 1 < argc) {
            max_order = parse_int(argv[++i], "maximum order");
        } else if (strcmp(argv[i], "--max-iterations") == 0 && i + 1 < argc) {
            max_iterations = parse_int(argv[++i], "iteration count");
        } else {
            fprintf(stderr, "usage: %s [--min-order N] [--max-order N] [--max-iterations N]\n", argv[0]);
            return 2;
        }
    }
    if (min_order > max_order) {
        fprintf(stderr, "minimum order exceeds maximum order\n");
        return 2;
    }

    int result = 0;
    puts("p,alpha,run_length,rate,iterations,min_slack,status");
    for (int p = min_order; p <= max_order; ++p) {
        for (size_t i = 0; i < sizeof(alphas) / sizeof(alphas[0]); ++i) {
            if (certify(p, alphas[i], max_iterations) != 0) {
                result = 1;
            }
        }
    }
    return result;
}
