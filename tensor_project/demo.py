import numpy as np

from tensor_project.tensors import unfold, mode_n_product, frobenius_norm
from tensor_project.decompositions import (
    matrix_rank_from_svd,
    best_rank_k_approximation,
    cp_rank1_approximation,
)
from tensor_project.pca import pca_fit_transform
from tensor_project.fourier import dominant_frequency


def main():
    print("Tensor Project Demo")

    T = np.arange(24, dtype=float).reshape(2, 3, 4)
    print("Tensor shape:", T.shape)
    print("Mode-1 unfolding shape:", unfold(T, mode=1).shape)
    print("Frobenius norm:", frobenius_norm(T))

    A = np.array([[1, 0], [0, 1], [1, 1]], dtype=float)
    transformed = mode_n_product(T, A, mode=0)
    print("Mode-0 product shape:", transformed.shape)

    X = np.array([[3.0, 1.0], [1.0, 3.0], [2.0, 2.0]])
    print("Matrix rank from SVD:", matrix_rank_from_svd(X))
    X1 = best_rank_k_approximation(X, k=1)
    print("Best rank-1 approximation:\n", X1)

    scale, factors, approx = cp_rank1_approximation(T)
    print("CP-style rank-1 scale:", scale)
    print("Factor lengths:", [len(f) for f in factors])
    print("Approximation shape:", approx.shape)

    data = np.array([
        [2.0, 0.0],
        [0.0, 2.0],
        [3.0, 1.0],
        [1.0, 3.0],
        [4.0, 2.0],
    ])
    Z, model = pca_fit_transform(data, n_components=1)
    print("PCA latent coordinates shape:", Z.shape)
    print("Explained variance ratio:", model["explained_variance_ratio"])

    sample_rate = 500
    t = np.linspace(0, 1, sample_rate, endpoint=False)
    signal = np.sin(2 * np.pi * 7 * t)
    print("Dominant frequency:", dominant_frequency(signal, sample_rate))

    print("Complete")


if __name__ == "__main__":
    main()
