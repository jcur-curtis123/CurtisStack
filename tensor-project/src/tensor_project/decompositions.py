from __future__ import annotations

import numpy as np

from .tensors import unfold, rank1_outer


def truncated_svd(X: np.ndarray, k: int | None = None):
    """
    Compute the SVD of a matrix and optionally truncate to rank k.
    """
    if X.ndim != 2:
        raise ValueError("X must be a matrix")
    U, s, Vt = np.linalg.svd(X, full_matrices=False)
    if k is None:
        return U, s, Vt
    if k < 1 or k > min(X.shape):
        raise ValueError("k must be between 1 and min(X.shape)")
    return U[:, :k], s[:k], Vt[:k, :]


def matrix_rank_from_svd(X: np.ndarray, tol: float = 1e-10) -> int:
    """
    Return the rank of X as the number of singular values greater than tol.
    """
    _, s, _ = truncated_svd(X)
    return int(np.sum(s > tol))


def best_rank_k_approximation(X: np.ndarray, k: int) -> np.ndarray:
    """
    Return the best rank-k approximation of a matrix from truncated SVD.
    """
    U, s, Vt = truncated_svd(X, k=k)
    return U @ np.diag(s) @ Vt


def cp_rank1_approximation(X: np.ndarray):
    """
    Simple CP-style rank-1 approximation of a tensor using the leading
    singular vector of each unfolding.

    This is an educational approximation, not a full ALS solver.
    """
    if X.ndim < 2:
        raise ValueError("X must have at least 2 dimensions")
    factors = []
    for mode in range(X.ndim):
        unfolded = unfold(X, mode)
        U, s, _ = np.linalg.svd(unfolded, full_matrices=False)
        factors.append(U[:, 0])

    approx = rank1_outer(factors)
    numerator = float(np.tensordot(X, approx, axes=X.ndim))
    denominator = float(np.sum(approx**2))
    scale = numerator / denominator if denominator != 0 else 0.0
    return scale, factors, scale * approx
