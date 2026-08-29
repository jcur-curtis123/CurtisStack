from __future__ import annotations

import numpy as np


def center_matrix(X: np.ndarray):
    """
    Center a data matrix by subtracting the column means.
    """
    X = np.asarray(X, dtype=float)
    mean = X.mean(axis=0, keepdims=True)
    return X - mean, mean


def covariance_matrix(X_centered: np.ndarray) -> np.ndarray:
    """
    Compute the sample covariance matrix of centered data.
    """
    n = X_centered.shape[0]
    if n < 2:
        raise ValueError("Need at least 2 rows to compute sample covariance")
    return (X_centered.T @ X_centered) / (n - 1)


def explained_variance_ratio(eigenvalues: np.ndarray) -> np.ndarray:
    """
    Convert eigenvalues into explained variance ratios.
    """
    total = np.sum(eigenvalues)
    if total <= 0:
        raise ValueError("Total variance must be positive")
    return eigenvalues / total


def pca_fit_transform(X: np.ndarray, n_components: int):
    """
    PCA using SVD of the centered data matrix.
    """
    X_centered, mean = center_matrix(X)
    U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)

    if n_components < 1 or n_components > Vt.shape[0]:
        raise ValueError("Invalid number of components")

    components = Vt[:n_components]
    Z = X_centered @ components.T

    n = X.shape[0]
    explained_variances = (s**2) / (n - 1)
    variance_ratios = explained_variance_ratio(explained_variances)

    model = {
        "mean": mean,
        "components": components,
        "singular_values": s,
        "explained_variances": explained_variances,
        "explained_variance_ratio": variance_ratios,
    }
    return Z, model
