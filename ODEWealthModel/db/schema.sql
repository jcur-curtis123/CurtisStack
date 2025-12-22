DROP TABLE IF EXISTS wealth_timeseries CASCADE;
DROP TABLE IF EXISTS run_parameters CASCADE;
DROP TABLE IF EXISTS simulation_runs CASCADE;

CREATE TABLE simulation_runs (
  run_id BIGSERIAL PRIMARY KEY,
  model_name TEXT NOT NULL,
  start_ts TIMESTAMPTZ DEFAULT NOW(),
  notes TEXT
);

CREATE TABLE run_parameters (
  run_id BIGINT REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  value DOUBLE PRECISION NOT NULL,
  PRIMARY KEY (run_id, name)
);

CREATE TABLE wealth_timeseries (
  run_id BIGINT REFERENCES simulation_runs(run_id) ON DELETE CASCADE,
  t DOUBLE PRECISION NOT NULL,
  wealth DOUBLE PRECISION NOT NULL,
  contrib DOUBLE PRECISION,
  withdraw DOUBLE PRECISION,
  pi DOUBLE PRECISION,
  PRIMARY KEY (run_id, t)
);

CREATE INDEX idx_wealth_run ON wealth_timeseries(run_id);
