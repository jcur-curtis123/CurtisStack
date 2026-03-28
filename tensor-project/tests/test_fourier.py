import numpy as np

from tensor_project.fourier import fft_spectrum, dominant_frequency, reconstruct_from_fft


def test_dominant_frequency():
    sample_rate = 200
    t = np.linspace(0, 1, sample_rate, endpoint=False)
    signal = np.sin(2 * np.pi * 9 * t)
    freq = dominant_frequency(signal, sample_rate)
    assert abs(freq - 9.0) < 1e-9


def test_reconstruct_from_fft():
    sample_rate = 128
    t = np.linspace(0, 1, sample_rate, endpoint=False)
    signal = np.cos(2 * np.pi * 5 * t)
    freqs, amps, fft_vals = fft_spectrum(signal, sample_rate)
    reconstructed = reconstruct_from_fft(fft_vals, n=len(signal))
    assert np.allclose(signal, reconstructed)
