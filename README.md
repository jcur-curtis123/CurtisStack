
# CurtisStack
A collection of programming, data structures, and machine learning projects
built by **Jacob Curtis**.

This repository serves as a personal project stack showcasing:
- algorithmic thinking
- applied machine learning
- systems-level programming
- Python-based experimentation

---

## 📁 Projects

### 🔹 ML w: C
An end-to-end **unsupervised machine learning pipeline written entirely in C++**.

Features:
- SQLite-backed data storage
- Feature scaling
- K-Means clustering
- Principal Component Analysis (PCA)

📂 `ML w: C/`

---

### 🔹 Perceptron (2 Ways) — Python
Binary classification using perceptron learning implemented in Python.

---

### 🔹 Decision Tree — Python
Decision tree implementation and experiments in Python.

---

### 🔹 Linked List — Python
Linked list data structure implementations in Python.

---

## 🧠 Focus Areas

- Machine Learning (from scratch)
- Data Structures & Algorithms
- Systems Programming (C++)
- Applied Python for ML & experimentation

---

## 👤 Author

**Jacob Curtis**  
M.S. Data Science – Northeastern University

---

> Each project folder contains its own README
=======
# ODEWealthModel
**Continuous-Time Wealth Simulation (ODE) with PostgreSQL**

## Overview
ODEWealthModel is a Python simulation project that models long-term wealth growth using an **ordinary differential equation (ODE)**.  
It solves the wealth dynamics numerically (SciPy) and stores every simulation run and full wealth time series in **PostgreSQL** for reproducible analysis and strategy comparison.

---

## Differential Equation Model
Let **W(t)** be wealth at time **t** (in years). The model is:

dW/dt = ( r_f + pi * (mu - r_f) - lambda * pi^2 ) * W(t) + c(t) - u(t)

Where:
- **r_f**: risk-free rate
- **mu**: expected return of the risky asset
- **pi**: fraction of wealth allocated to the risky asset (strategy)
- **lambda**: penalty term for aggressive allocation (risk/fees proxy)
- **c(t)**: contribution rate (deposits per year)
- **u(t)**: withdrawal rate (spending per year)

Interpretation: the equation defines the **instantaneous rate of change** of wealth based on current wealth, returns, allocation, and cashflows.

---

## Why ODEs?
ODEs model systems that evolve continuously over time where the current state affects future outcomes.  
This makes them a natural fit for compounding capital growth and strategy-driven dynamics.

---

## Tech Stack
- **Python**: model + simulation runner
- **SciPy**: numerical ODE solver (`solve_ivp`)
- **PostgreSQL**: stores run metadata, parameters, and time-series results
- **SQL**: query and compare strategies across many runs

---

