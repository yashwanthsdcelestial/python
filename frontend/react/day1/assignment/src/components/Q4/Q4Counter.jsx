import React, { useState } from "react";

function Q4Counter() {
  const [count, setCount] = useState(0);
  const MIN = 0, MAX = 10;

  return (
    <div>
      <h2>Q4 — Counter App with Limits</h2>
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <button
          onClick={() => setCount(c => c - 1)}
          disabled={count <= MIN}
          style={{ fontSize: "1.5rem", padding: "6px 18px", cursor: count <= MIN ? "not-allowed" : "pointer" }}
        >−</button>

        <span style={{ fontSize: "2rem", fontWeight: 700, minWidth: "40px", textAlign: "center" }}>{count}</span>

        <button
          onClick={() => setCount(c => c + 1)}
          disabled={count >= MAX}
          style={{ fontSize: "1.5rem", padding: "6px 18px", cursor: count >= MAX ? "not-allowed" : "pointer" }}
        >+</button>

        <button onClick={() => setCount(0)} style={{ padding: "8px 16px", background: "#94a3b8", color: "#fff", border: "none", borderRadius: "6px", cursor: "pointer" }}>
          Reset
        </button>
      </div>

      {count === MIN && <p style={{ color: "#ef4444" }}>⚠ Minimum limit reached!</p>}
      {count === MAX && <p style={{ color: "#ef4444" }}>⚠ Maximum limit reached!</p>}
    </div>
  );
}

export default Q4Counter;
