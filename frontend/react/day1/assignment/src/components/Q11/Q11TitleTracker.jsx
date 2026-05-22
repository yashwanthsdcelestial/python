import React, { useState, useEffect } from "react";

function Q11TitleTracker() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
    return () => { document.title = "React App"; };
  }, [count]);

  return (
    <div>
      <h2>Q11 — Document Title Tracker</h2>
      <p style={{ color: "#64748b" }}>Watch the browser tab title change as you click the buttons!</p>
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <button onClick={() => setCount(c => c - 1)} style={{ fontSize: "1.4rem", padding: "4px 16px" }}>−</button>
        <span style={{ fontSize: "2rem", fontWeight: 700 }}>{count}</span>
        <button onClick={() => setCount(c => c + 1)} style={{ fontSize: "1.4rem", padding: "4px 16px" }}>+</button>
      </div>
      <p style={{ fontSize: "0.85rem", color: "#94a3b8", marginTop: "8px" }}>
        Current document.title: <code>Count: {count}</code>
      </p>
    </div>
  );
}

export default Q11TitleTracker;
