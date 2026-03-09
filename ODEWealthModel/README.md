# ODEWealthModel
**Continuous-Time Wealth Simulation Using Ordinary Differential Equations**

## Overview
ODEWealthModel is a Python project that models long-term wealth growth as a
continuous-time dynamical system. Wealth evolution is defined by an ordinary
differential equation (ODE) and solved numerically, with all simulation results
stored in PostgreSQL for reproducible analysis.

---

## Model
Let **W(t)** denote wealth at time **t** (years).

dW/dt = ( r_f + pi · (mu − r_f) − lambda · pi² ) · W(t) + c(t) − u(t)

Where:
- **r_f** — risk-free rate  
- **mu** — expected return of risky asset  
- **pi** — fraction of wealth invested in risky asset  
- **lambda** — risk / fee penalty  
- **c(t)** — contribution rate  
- **u(t)** — withdrawal rate  

This equation defines the instantaneous rate of change of wealth given the
current portfolio strategy and cashflows.

---

## Why ODEs?
Ordinary differential equations are used to model systems that evolve
continuously over time. They are standard in physics and economics and provide
a natural framework for modeling compounding capital growth and strategy-driven
feedback effects.

---

## Tech Stack
- Python
- SciPy (`solve_ivp`)
- PostgreSQL
- SQLAlchemy

---

## Installation & Usage

### Prerequisites
- Python 3.10+
- PostgreSQL
- `psql` available on your PATH

---

### Setup

#### 1. Clone the repository

git clone git@github.com:jcur-curtis123/CurtisStack.git
cd CurtisStack/ODEWealthModel

#### 2. Create and activate a virtual env

python3 -m venv .venv
source .venv/bin/activate

#### 3. Create the database and tables

createdb odelab
psql -d odelab -f db/schema.sql

#### 4. Configure environment variables 

DATABASE_URL=postgresql+psycopg2://YOUR_USERNAME@localhost:5432/odelab

