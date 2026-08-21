import React, { useState } from "react";
import "./App.css";

const DEFAULT_QUESTION = "Can I build a duplex here?";

// A verdict badge every eligibility state maps to. Kept as data (not
// scattered ternaries) so the stamp, card accent, and label always agree.
function verdictFor(data) {
  if (!data || !data.parcel) {
    return { stamp: "NO PARCEL FOUND", tone: "neutral" };
  }
  const eligible = data.eligibility?.eligible;
  if (eligible === true) return { stamp: "2-UNIT ELIGIBLE", tone: "yes" };
  if (eligible === false) return { stamp: "NOT ELIGIBLE", tone: "no" };
  return { stamp: "NEEDS REVIEW", tone: "neutral" };
}

export default function App() {
  const [address, setAddress] = useState("");
  const [question, setQuestion] = useState(DEFAULT_QUESTION);
  const [result, setResult] = useState(null);
  const [status, setStatus] = useState("idle"); // idle | loading | error
  const [errorMsg, setErrorMsg] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    if (!address.trim()) return;

    setStatus("loading");
    setErrorMsg("");
    try {
      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ address, question }),
      });
      if (!res.ok) {
        throw new Error(`Server responded ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
      setStatus("idle");
    } catch (err) {
      setStatus("error");
      setErrorMsg(
        "Couldn't reach the FieldMatch API. Check that the backend is running on port 8000, then try again."
      );
    }
  }

  const verdict = result ? verdictFor(result) : null;

  return (
    <div className="page">
      <header className="masthead">
        <div className="masthead-eyebrow">Parcel &amp; zoning lookup — Maine</div>
        <h1>FieldMatch</h1>
        <p className="masthead-sub">
          Enter an address to check whether the lot is eligible for a second
          housing unit under Maine's LD 2003 statewide density law.
        </p>
      </header>

      <main className="layout">
        <form className="query-panel" onSubmit={handleSubmit}>
          <label className="field">
            <span className="field-label">Property address</span>
            <input
              type="text"
              value={address}
              onChange={(e) => setAddress(e.target.value)}
              placeholder="385 Congress St, Portland, ME"
              autoComplete="off"
              required
            />
          </label>

          <label className="field">
            <span className="field-label">Question</span>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder={DEFAULT_QUESTION}
            />
          </label>

          <button type="submit" className="submit-btn" disabled={status === "loading"}>
            {status === "loading" ? "Checking parcel…" : "Check eligibility"}
          </button>

          {status === "error" && <p className="form-error">{errorMsg}</p>}

          {result?.demo_data && (
            <p className="demo-banner">
              Running on bundled demo parcels (downtown Portland, ME only).
              Drop a real parcels.shp into backend/data to use it anywhere
              else.
            </p>
          )}
        </form>

        <section className="result-panel" aria-live="polite">
          {!result && status !== "loading" && (
            <div className="empty-state">
              <p>No lookup yet.</p>
              <p className="empty-sub">Enter an address and check eligibility to see the parcel record here.</p>
            </div>
          )}

          {status === "loading" && (
            <div className="empty-state">
              <p>Geocoding address and checking the parcel…</p>
            </div>
          )}

          {result && status !== "loading" && (
            <article className={`record-card tone-${verdict.tone}`}>
              <div className={`stamp stamp-${verdict.tone}`}>{verdict.stamp}</div>

              <div className="ledger">
                <span>{result.geocoded?.display_name || result.address}</span>
                <span className="ledger-coords">
                  {result.geocoded ? `${result.geocoded.lat.toFixed(5)}, ${result.geocoded.lon.toFixed(5)}` : "—"}
                  {result.geocoded && !result.geocoded.matched && " (approx.)"}
                </span>
              </div>

              <p className="answer">{result.answer}</p>

              {result.parcel && (
                <dl className="facts">
                  <div>
                    <dt>Parcel ID</dt>
                    <dd>{result.parcel.parcel_id ?? "—"}</dd>
                  </div>
                  <div>
                    <dt>Zone</dt>
                    <dd>{result.parcel.zone || "—"}</dd>
                  </div>
                  <div>
                    <dt>Lot size</dt>
                    <dd>{result.parcel.lot_sqft ? `${Math.round(result.parcel.lot_sqft).toLocaleString()} sq ft` : "—"}</dd>
                  </div>
                  <div>
                    <dt>Max units</dt>
                    <dd>{result.eligibility?.max_units ?? "—"}</dd>
                  </div>
                  <div>
                    <dt>Growth area</dt>
                    <dd>{result.parcel.growth_area ? "Yes" : "No"}</dd>
                  </div>
                  <div>
                    <dt>Shoreland</dt>
                    <dd>{result.parcel.shoreland ? "Yes" : "No"}</dd>
                  </div>
                </dl>
              )}

              <div className="confidence">
                <div className="confidence-row">
                  <span>Confidence</span>
                  <span className="confidence-value">{Math.round(result.confidence * 100)}%</span>
                </div>
                <div className="confidence-track">
                  <div
                    className="confidence-fill"
                    style={{ width: `${Math.round(result.confidence * 100)}%` }}
                  />
                </div>
              </div>

              {result.eligibility?.caveats?.length > 0 && (
                <div className="caveats">
                  <span className="caveats-label">In order of what to check first</span>
                  <ol>
                    {result.eligibility.caveats.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ol>
                </div>
              )}
            </article>
          )}
        </section>
      </main>

      <footer className="foot-note">
        Reference only — not a substitute for your municipality's adopted
        ordinance or a call to the local code enforcement office.
      </footer>
    </div>
  );
}
