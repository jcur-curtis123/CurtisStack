from __future__ import annotations

import numpy as np


def set_seed(seed: int = 42) -> None:
    np.random.seed(seed)


def relative_error(X: np.ndarray, Y: np.ndarray) -> float:
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    denom = np.linalg.norm(X)
    if denom == 0:
        raise ValueError("Reference tensor has zero norm")
    return float(np.linalg.norm(X - Y) / denom)
