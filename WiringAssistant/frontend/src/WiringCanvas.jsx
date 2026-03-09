import React from "react";
import PanelMarker from "./PanelMarker";
import OutletMarker from "./OutletMarker";
import Legend from "./Legend";

const CIRCUIT_COLORS = [
  "#2563eb", // blue
  "#16a34a", // green
  "#dc2626", // red
  "#9333ea", // purple
  "#ea580c", // orange
  "#0891b2", // cyan
];

export default function WiringCanvas({
  width,
  height,
  panel,
  outlets,
  circuits,
}) {
  return (
    <div style={{ position: "relative" }}>
      <svg width={width} height={height} style={{ background: "#f9fafb" }}>
        {/* ROUTES */}
        {circuits.map((circuit, ci) => {
          const color = CIRCUIT_COLORS[ci % CIRCUIT_COLORS.length];

          return circuit.routes.map((route, ri) => {
            const strokeWidth = route.kind === "trunk" ? 6 : 2;
            const opacity = route.kind === "trunk" ? 1.0 : 0.8;

            const d = route.points
              .map((p, i) =>
                i === 0 ? `M ${p.x} ${p.y}` : `L ${p.x} ${p.y}`
              )
              .join(" ");

            return (
              <path
                key={`${ci}-${ri}`}
                d={d}
                fill="none"
                stroke={color}
                strokeWidth={strokeWidth}
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity={opacity}
              />
            );
          });
        })}

        {/* PANEL */}
        {panel && <PanelMarker panel={panel} />}

        {/* OUTLETS */}
        {outlets.map((outlet) => {
          const circuitIndex = circuits.findIndex((c) =>
            c.outlet_ids.includes(outlet.id)
          );
          const color =
            circuitIndex >= 0
              ? CIRCUIT_COLORS[circuitIndex % CIRCUIT_COLORS.length]
              : "#6b7280";

          return (
            <OutletMarker
              key={outlet.id}
              outlet={outlet}
              color={color}
            />
          );
        })}
      </svg>

      <Legend />
    </div>
  );
}
