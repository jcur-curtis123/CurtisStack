import numpy as np

from tensor_project.pca import center_matrix, covariance_matrix, pca_fit_transform


def test_center_matrix_zero_mean():
    X = np.array([[1.0, 2.0], [3.0, 4.0]])
    Xc, mean = center_matrix(X)
    assert np.allclose(Xc.mean(axis=0), 0.0)
    assert mean.shape == (1, 2)


def test_covariance_matrix_shape():
    X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    Xc, _ = center_matrix(X)
    C = covariance_matrix(Xc)
    assert C.shape == (2, 2)


def test_pca_fit_transform_shape():
    X = np.array([
        [2.0, 0.0],
        [0.0, 2.0],
        [3.0, 1.0],
        [1.0, 3.0],
    ])
    Z, model = pca_fit_transform(X, n_components=1)
    assert Z.shape == (4, 1)
    assert model["components"].shape == (1, 2)
