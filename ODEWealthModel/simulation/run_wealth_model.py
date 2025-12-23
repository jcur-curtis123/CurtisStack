import numpy as np
import pandas as pd
import os
from scipy.integrate import solve_ivp
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Create a .env file with DATABASE_URL defined."
    )


engine = create_engine(
DATABASE_URL)

def wealth_ode(t, y, rf, mu, lam, pi, contrib, withdraw):
    W = y[0]
    growth = (rf + pi * (mu - rf) - lam * pi**2) * W
    return [growth + contrib - withdraw]

def run_simulation():
    params = {
        "rf": 0.03,
        "mu": 0.08,
        "lam": 0.01,
        "pi": 0.6,
        "contrib": 12_000,
        "withdraw": 0.0,
        "W0": 100_000,
        "T": 40
    }

    t_eval = np.linspace(0, params["T"], 1500)

    sol = solve_ivp(
        wealth_ode,
        (0, params["T"]),
        [params["W0"]],
        t_eval=t_eval,
        args=(
            params["rf"],
            params["mu"],
            params["lam"],
            params["pi"],
            params["contrib"],
            params["withdraw"],
        ),
    )

    df = pd.DataFrame({
        "t": sol.t,
        "wealth": sol.y[0],
        "contrib": params["contrib"],
        "withdraw": params["withdraw"],
        "pi": params["pi"]
    })

    with engine.begin() as conn:
        run_id = conn.execute(
            text("""
                INSERT INTO simulation_runs (model_name, notes)
                VALUES ('WealthODE', 'Baseline 60/40 strategy')
                RETURNING run_id
            """)
        ).scalar_one()

        conn.execute(
            text("""
                INSERT INTO run_parameters (run_id, name, value)
                VALUES (:run_id, :name, :value)
            """),
            [{"run_id": run_id, "name": k, "value": float(v)}
             for k, v in params.items()]
        )

        df.insert(0, "run_id", run_id)
        df.to_sql("wealth_timeseries", conn, if_exists="append", index=False)

    print(f"Simulation stored with run_id={run_id}")

if __name__ == "__main__":
    run_simulation()
