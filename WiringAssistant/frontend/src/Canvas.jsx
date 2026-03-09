import { Stage, Layer, Circle, Line, Image as KonvaImage, Rect, Text } from "react-konva";
import useImage from "use-image";
import { useMemo, useState } from "react";

const API = "http://localhost:8000";

function dist(a,b){ const dx=a.x-b.x, dy=a.y-b.y; return Math.sqrt(dx*dx+dy*dy); }

export default function Canvas() {
  const [bgUrl, setBgUrl] = useState("/plan.png");
  const [img] = useImage(bgUrl);

  const [objects, setObjects] = useState([]); // {id,type,center:{x,y},bbox,confidence}
  const [wallMaskB64, setWallMaskB64] = useState(null);

  const [panelId, setPanelId] = useState(null);
  const [outletIds, setOutletIds] = useState([]);
  const [routes, setRoutes] = useState([]);

  const width = img?.width || 1024;
  const height = img?.height || 768;

  const outlets = useMemo(() => objects.filter(o => o.type === "outlet"), [objects]);
  const panel = useMemo(() => objects.find(o => o.id === panelId) || objects.find(o => o.type === "panel"), [objects, panelId]);

  const onFile = (e) => {
    const f = e.target.files?.[0];
    if (!f) return;
    const url = URL.createObjectURL(f);
    setBgUrl(url);
    // reset state
    setObjects([]);
    setWallMaskB64(null);
    setPanelId(null);
    setOutletIds([]);
    setRoutes([]);
  };

  const autodetect = async () => {
    // fetch the current image blob (bgUrl could be object URL or /plan.png)
    const blob = await fetch(bgUrl).then(r => r.blob());
    const form = new FormData();
    form.append("file", blob, "plan.png");
    const res = await fetch(`${API}/detect`, { method: "POST", body: form });
    if (!res.ok) {
      alert("Detect failed: " + (await res.text()));
      return;
    }
    const data = await res.json();
    setObjects(data.objects || []);
    setWallMaskB64(data.wall_mask_png_base64 || null);

    const panelObj = (data.objects || []).find(o => o.type === "panel") || null;
    if (panelObj) setPanelId(panelObj.id);

    const outIds = (data.objects || []).filter(o => o.type === "outlet").map(o => o.id);
    setOutletIds(outIds);
    setRoutes([]);
  };

  const optimize = async () => {
    if (!panelId || outletIds.length === 0 || !wallMaskB64) {
      alert("Need a panel, outlets, and wall mask. Run Auto-detect first.");
      return;
    }
    const req = {
      width,
      height,
      panel_id: panelId,
      outlet_ids: outletIds,
      objects,
      wall_mask_png_base64: wallMaskB64
    };
    const res = await fetch(`${API}/optimize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(req)
    });
    if (!res.ok) {
      alert("Optimize failed: " + (await res.text()));
      return;
    }
    const data = await res.json();
    setRoutes(data.routes || []);
  };

  const handleClick = (e) => {
    const stage = e.target.getStage();
    const pos = stage.getPointerPosition();
    if (!pos) return;

    // Click near an outlet to toggle include/exclude
    const near = outlets.find(o => dist(o.center, pos) < 15);
    if (near) {
      setOutletIds((prev) => prev.includes(near.id) ? prev.filter(id => id !== near.id) : [...prev, near.id]);
      return;
    }

    // If click near panel, set panel
    const maybePanel = objects.find(o => o.type === "panel" && dist(o.center, pos) < 20);
    if (maybePanel) {
      setPanelId(maybePanel.id);
      return;
    }
  };

  return (
    <div>
      <div style={{ display: "flex", gap: 10, alignItems: "center", marginBottom: 10 }}>
        <input type="file" accept="image/*" onChange={onFile} />
        <button onClick={autodetect}>Auto-detect</button>
        <button onClick={optimize}>Optimize wiring</button>
        <div style={{ fontSize: 12, opacity: 0.8 }}>
          Click an outlet to include/exclude. Panel auto-picks a candidate (you can refine later).
        </div>
      </div>

      <Stage width={width} height={height} onClick={handleClick} style={{ border: "1px solid #ddd" }}>
        <Layer>
          {img && <KonvaImage image={img} x={0} y={0} />}
        </Layer>

        <Layer>
          {/* panel */}
          {panel && (
            <>
              <Circle x={panel.center.x} y={panel.center.y} radius={10} stroke="blue" strokeWidth={3} />
              <Text x={panel.center.x + 12} y={panel.center.y - 8} text="PANEL" fontSize={12} fill="blue" />
            </>
          )}

          {/* outlets */}
          {outlets.map((o) => {
            const active = outletIds.includes(o.id);
            return (
              <Circle
                key={o.id}
                x={o.center.x}
                y={o.center.y}
                radius={8}
                stroke={active ? "green" : "#888"}
                strokeWidth={3}
                fill={active ? "rgba(0,255,0,0.15)" : "transparent"}
              />
            );
          })}

          {/* routes */}
          {routes.map((r, i) => (
            <Line
              key={i}
              points={r.points.flatMap((p) => [p.x, p.y])}
              stroke="red"
              strokeWidth={3}
              lineCap="round"
              lineJoin="round"
            />
          ))}
        </Layer>
      </Stage>
    </div>
  );
}
