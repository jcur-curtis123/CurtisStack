from __future__ import annotations

import numpy as np


def tensor_shape(X: np.ndarray) -> tuple[int, ...]:
    """Return the shape of a tensor as a tuple."""
    return tuple(X.shape)


def unfold(X: np.ndarray, mode: int) -> np.ndarray:
    """
    Unfold a tensor along a given mode.

    Parameters
    ----------
    X : np.ndarray
        Input tensor.
    mode : int
        Mode along which to unfold.

    Returns
    -------
    np.ndarray
        Matrix of shape (X.shape[mode], product of other dimensions).
    """
    if mode < 0 or mode >= X.ndim:
        raise ValueError(f"mode must be in [0, {X.ndim - 1}]")
    return np.reshape(np.moveaxis(X, mode, 0), (X.shape[mode], -1))


def fold(unfolded: np.ndarray, shape: tuple[int, ...], mode: int) -> np.ndarray:
    """
    Fold a mode-unfolded tensor back to its original shape.
    """
    if mode < 0 or mode >= len(shape):
        raise ValueError(f"mode must be in [0, {len(shape) - 1}]")
    front = shape[mode]
    rest = [shape[i] for i in range(len(shape)) if i != mode]
    reshaped = unfolded.reshape((front, *rest))
    return np.moveaxis(reshaped, 0, mode)


def mode_n_product(X: np.ndarray, M: np.ndarray, mode: int) -> np.ndarray:
    """
    Compute the mode-n product of tensor X with matrix M.

    If X has shape (I1, ..., In, ..., IN) and M has shape (J, In),
    then the result has shape (I1, ..., J, ..., IN).
    """
    if mode < 0 or mode >= X.ndim:
        raise ValueError(f"mode must be in [0, {X.ndim - 1}]")
    if M.ndim != 2:
        raise ValueError("M must be a matrix")
    if M.shape[1] != X.shape[mode]:
        raise ValueError(
            f"Incompatible shapes: M has second dimension {M.shape[1]}, "
            f"but X.shape[{mode}] = {X.shape[mode]}"
        )
    unfolded = unfold(X, mode)
    product = M @ unfolded
    new_shape = list(X.shape)
    new_shape[mode] = M.shape[0]
    return fold(product, tuple(new_shape), mode)


def frobenius_norm(X: np.ndarray) -> float:
    """Compute the Frobenius norm of a tensor."""
    return float(np.sqrt(np.sum(np.asarray(X, dtype=float) ** 2)))


def rank1_outer(vectors: list[np.ndarray]) -> np.ndarray:
    """
    Build a rank-1 tensor from a list of vectors using repeated outer products.
    """
    if not vectors:
        raise ValueError("vectors must be non-empty")
    result = np.asarray(vectors[0], dtype=float)
    for v in vectors[1:]:
        result = np.multiply.outer(result, np.asarray(v, dtype=float))
    return result
