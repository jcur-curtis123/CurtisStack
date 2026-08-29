import numpy as np

from tensor_project.decompositions import (
    truncated_svd,
    matrix_rank_from_svd,
    best_rank_k_approximation,
    cp_rank1_approximation,
)
from tensor_project.utils import relative_error


def test_truncated_svd_shapes():
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    U, s, Vt = truncated_svd(X, k=1)
    assert U.shape == (3, 1)
    assert s.shape == (1,)
    assert Vt.shape == (1, 2)


def test_matrix_rank_from_svd():
    X = np.array([[1.0, 0.0], [0.0, 0.0]])
    assert matrix_rank_from_svd(X) == 1


def test_best_rank_k_approximation_rank_1_error_reasonable():
    X = np.array([[3.0, 1.0], [1.0, 3.0], [2.0, 2.0]])
    X1 = best_rank_k_approximation(X, k=1)
    assert X1.shape == X.shape
    assert relative_error(X, X1) < 0.5


def test_cp_rank1_approximation_shape():
    T = np.arange(24, dtype=float).reshape(2, 3, 4)
    scale, factors, approx = cp_rank1_approximation(T)
    assert isinstance(scale, float)
    assert len(factors) == 3
    assert approx.shape == T.shape
