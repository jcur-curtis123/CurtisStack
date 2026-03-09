import React from "react";

export default function PanelMarker({ panel }) {
  const { x, y } = panel.center;

  return (
    <>
      <rect
        x={x - 8}
        y={y - 8}
        width={16}
        height={16}
        fill="#111827"
        stroke="#ffffff"
        strokeWidth={2}
        rx={2}
      />
      <text
        x={x + 10}
        y={y - 10}
        fontSize={10}
        fill="#111827"
        fontWeight="bold"
      >
        PANEL
      </text>
    </>
  );
}
