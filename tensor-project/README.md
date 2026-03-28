# Tensor Project

A GitHub-ready Python project for learning and experimenting with:

- tensor operations
- tensor decompositions
- PCA
- Fourier analysis
- visualization
- testing

## Features

- Clean `src/` layout
- NumPy-based tensor utilities
- Matrix SVD helpers and CP-style tensor rank-1 approximation
- PCA from scratch and with SVD intuition
- Fourier transform helpers for 1D signals
- Plotting utilities
- Example script
- Unit tests
- GitHub Actions CI
- MIT License

## Project Structure

```text
tensor-project/
├── .github/workflows/python-tests.yml
├── data/
├── docs/
├── examples/
├── notebooks/
├── src/tensor_project/
├── tests/
├── .gitignore
├── LICENSE
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

## Run the example

```bash
python examples/demo.py
```

## Run tests

```bash
pytest
```

## Quick example

```python
import numpy as np
from tensor_project.pca import pca_fit_transform
from tensor_project.fourier import dominant_frequency
from tensor_project.tensors import unfold

X = np.array([
    [2.0, 0.0],
    [0.0, 2.0],
    [3.0, 1.0],
    [1.0, 3.0],
])

Z, model = pca_fit_transform(X, n_components=1)
print(Z.shape)

signal = np.sin(2 * np.pi * 5 * np.linspace(0, 1, 500, endpoint=False))
freq = dominant_frequency(signal, sample_rate=500)
print(freq)

T = np.arange(24).reshape(2, 3, 4)
print(unfold(T, mode=1).shape)
```

## Roadmap

- Tucker decomposition
- CP-ALS decomposition
- tensor completion experiments
- convolution and spectral filtering demos
- autoencoder latent-dimension experiments
- notebook-based mini textbook

## License

MIT
