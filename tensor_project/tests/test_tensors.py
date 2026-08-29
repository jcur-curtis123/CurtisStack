import numpy as np

from tensor_project.tensors import unfold, fold, mode_n_product, frobenius_norm, rank1_outer


def test_unfold_and_fold_roundtrip():
    X = np.arange(24).reshape(2, 3, 4)
    unfolded = unfold(X, mode=1)
    rebuilt = fold(unfolded, X.shape, mode=1)
    assert np.array_equal(X, rebuilt)


def test_mode_n_product_shape():
    X = np.arange(24).reshape(2, 3, 4)
    M = np.array([[1, 0], [0, 1], [1, 1]])
    Y = mode_n_product(X, M, mode=0)
    assert Y.shape == (3, 3, 4)


def test_frobenius_norm():
    X = np.array([[3.0, 4.0]])
    assert frobenius_norm(X) == 5.0


def test_rank1_outer_shape():
    v1 = np.array([1, 2])
    v2 = np.array([3, 4, 5])
    v3 = np.array([6, 7])
    T = rank1_outer([v1, v2, v3])
    assert T.shape == (2, 3, 2)
