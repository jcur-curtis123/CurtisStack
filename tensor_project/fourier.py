from __future__ import annotations

import numpy as np


def fft_spectrum(signal: np.ndarray, sample_rate: float):
    """
    Return positive frequencies and amplitude spectrum for a real-valued signal.
    """
    x = np.asarray(signal, dtype=float)
    n = x.size
    if n == 0:
        raise ValueError("signal must be non-empty")
    freqs = np.fft.rfftfreq(n, d=1.0 / sample_rate)
    fft_vals = np.fft.rfft(x)
    amplitudes = np.abs(fft_vals) / n
    return freqs, amplitudes, fft_vals


def dominant_frequency(signal: np.ndarray, sample_rate: float) -> float:
    """
    Return the dominant non-DC frequency of a real-valued signal.
    """
    freqs, amplitudes, _ = fft_spectrum(signal, sample_rate)
    if len(freqs) < 2:
        return 0.0
    idx = np.argmax(amplitudes[1:]) + 1
    return float(freqs[idx])


def reconstruct_from_fft(fft_vals: np.ndarray, n: int) -> np.ndarray:
    """
    Reconstruct a real-valued signal from its rFFT coefficients.
    """
    return np.fft.irfft(fft_vals, n=n)
