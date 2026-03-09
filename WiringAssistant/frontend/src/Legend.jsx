import React from "react";

export default function Legend() {
  return (
    <div
      style={{
        position: "absolute",
        bottom: 10,
        right: 10,
        background: "white",
        border: "1px solid #e5e7eb",
        padding: "8px",
        fontSize: "12px",
        borderRadius: "4px",
      }}
    >
      <div><strong>Legend</strong></div>
      <div>━━━ Trunk</div>
      <div>━━ Branch</div>
      <div>■ Panel</div>
      <div>● Outlet</div>
    </div>
  );
}
