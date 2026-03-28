from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt


def plot_signal_and_spectrum(signal: np.ndarray, sample_rate: float):
    from .fourier import fft_spectrum

    x = np.asarray(signal, dtype=float)
    t = np.arange(len(x)) / sample_rate
    freqs, amps, _ = fft_spectrum(x, sample_rate)

    fig1 = plt.figure()
    plt.plot(t, x)
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.title("Signal")

    fig2 = plt.figure()
    plt.plot(freqs, amps)
    plt.xlabel("Frequency")
    plt.ylabel("Amplitude")
    plt.title("Amplitude Spectrum")
    return fig1, fig2


def plot_2d_pca_projection(Z: np.ndarray):
    if Z.shape[1] < 2:
        raise ValueError("Z must have at least 2 columns for a 2D plot")
    fig = plt.figure()
    plt.scatter(Z[:, 0], Z[:, 1])
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA Projection")
    return fig
