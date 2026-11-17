"""
Module: em_algorithm.py
Implements:
Expectation-Maximization (EM) Algorithm for Gaussian Mixture Models (GMM).
Features E-step, M-step, Log-Likelihood Tracking, and Latent Variable Inference.
"""

import math
import random
import time
import numpy as np


def generate_sample_gmm_data(num_samples=120, num_clusters=2, seed=42):
    """Generates synthetic 1D multimodal Gaussian data with known true clusters."""
    np.random.seed(seed)
    data = []
    labels = []

    if num_clusters == 2:
        # Cluster 1: N(2.0, 0.8^2), Cluster 2: N(7.0, 1.2^2)
        n1 = num_samples // 2
        n2 = num_samples - n1
        c1 = np.random.normal(loc=2.0, scale=0.8, size=n1)
        c2 = np.random.normal(loc=7.0, scale=1.2, size=n2)
        data = np.concatenate([c1, c2])
        labels = [0] * n1 + [1] * n2
    elif num_clusters == 3:
        # 3 clusters: N(1.5, 0.6), N(5.0, 0.8), N(9.0, 1.0)
        n_each = num_samples // 3
        c1 = np.random.normal(loc=1.5, scale=0.6, size=n_each)
        c2 = np.random.normal(loc=5.0, scale=0.8, size=n_each)
        c3 = np.random.normal(loc=9.0, scale=1.0, size=num_samples - 2 * n_each)
        data = np.concatenate([c1, c2, c3])
        labels = [0] * n_each + [1] * n_each + [2] * (num_samples - 2 * n_each)
    else:
        # Generic multi-cluster
        n_each = num_samples // num_clusters
        all_clusters = []
        for k in range(num_clusters):
            pts = np.random.normal(loc=k * 3.5 + 2.0, scale=0.9, size=n_each)
            all_clusters.append(pts)
            labels.extend([k] * n_each)
        data = np.concatenate(all_clusters)

    return data, labels


def gaussian_1d_pdf(x, mean, var):
    """Univariate Gaussian probability density function."""
    var = max(var, 1e-6)
    denom = math.sqrt(2.0 * math.pi * var)
    exponent = -0.5 * ((x - mean) ** 2) / var
    return max(1e-12, (1.0 / denom) * math.exp(exponent))


def run_em_gmm(num_clusters=2, num_samples=120, max_iter=30, tolerance=1e-4, seed=42):
    """
    Executes the Expectation-Maximization Algorithm for Gaussian Mixture Models.
    E-step: Computes soft responsibilities gamma(i, k).
    M-step: Re-estimates means, variances, and mixture weights.
    """
    start_time = time.perf_counter()
    data, true_labels = generate_sample_gmm_data(num_samples, num_clusters, seed)
    N = len(data)
    K = num_clusters

    # Initial parameter guesses (e.g. quantiles / random points)
    sorted_data = np.sort(data)
    means = [float(sorted_data[int((k + 0.5) * N / K)]) for k in range(K)]
    variances = [float(np.var(data) / K)] * K
    weights = [1.0 / K] * K

    initial_params = {
        "means": [round(m, 3) for m in means],
        "variances": [round(v, 3) for v in variances],
        "weights": [round(w, 3) for w in weights]
    }

    log_likelihood_history = []
    responsibilities = np.zeros((N, K))

    converged = False
    prev_ll = -float('inf')

    for iteration in range(1, max_iter + 1):
        # -------------------------------------------------------------
        # E-STEP: Compute Responsibilities gamma(i, k)
        # -------------------------------------------------------------
        total_ll = 0.0
        for i in range(N):
            x = data[i]
            densities = [weights[k] * gaussian_1d_pdf(x, means[k], variances[k]) for k in range(K)]
            denom = sum(densities)

            if denom > 0:
                for k in range(K):
                    responsibilities[i, k] = densities[k] / denom
                total_ll += math.log(max(denom, 1e-12))
            else:
                responsibilities[i, :] = 1.0 / K

        log_likelihood_history.append({
            "iteration": iteration,
            "log_likelihood": round(total_ll, 3)
        })

        # Convergence test
        if abs(total_ll - prev_ll) < tolerance:
            converged = True
            break
        prev_ll = total_ll

        # -------------------------------------------------------------
        # M-STEP: Update Parameters (Weights, Means, Variances)
        # -------------------------------------------------------------
        for k in range(K):
            N_k = np.sum(responsibilities[:, k])
            if N_k < 1e-6:
                N_k = 1e-6

            # Update Mean
            means[k] = float(np.sum(responsibilities[:, k] * data) / N_k)

            # Update Variance
            diff_sq = (data - means[k]) ** 2
            variances[k] = float(max(1e-4, np.sum(responsibilities[:, k] * diff_sq) / N_k))

            # Update Mixture Weight
            weights[k] = float(N_k / N)

    # Normalize weights
    weight_sum = sum(weights)
    weights = [w / weight_sum for w in weights]

    # Cluster assignments (Hard clustering via argmax of soft responsibilities)
    assigned_clusters = [int(np.argmax(responsibilities[i, :])) for i in range(N)]

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 3)

    # Format points for frontend visualization
    formatted_points = []
    for i in range(N):
        formatted_points.append({
            "x": round(float(data[i]), 2),
            "cluster": assigned_clusters[i],
            "responsibilities": [round(float(responsibilities[i, k]), 3) for k in range(K)]
        })

    return {
        "success": True,
        "algorithm": "Expectation-Maximization (EM) for Gaussian Mixture Models",
        "num_clusters": K,
        "num_samples": N,
        "converged": converged,
        "total_iterations": len(log_likelihood_history),
        "initial_parameters": initial_params,
        "final_parameters": {
            "means": [round(m, 3) for m in means],
            "variances": [round(v, 3) for v in variances],
            "standard_deviations": [round(math.sqrt(v), 3) for v in variances],
            "weights": [round(w, 3) for w in weights]
        },
        "log_likelihood_history": log_likelihood_history,
        "sample_points": formatted_points[:60],
        "data_summary": {
            "min": round(float(np.min(data)), 2),
            "max": round(float(np.max(data)), 2),
            "mean": round(float(np.mean(data)), 2),
            "variance": round(float(np.var(data)), 2)
        },
        "execution_time_ms": elapsed_ms
    }
