import React, { useState, useCallback } from "react";
import IncrementButton from "./IncrementButton";

function Q15CounterCallback() {
  const [count, setCount] = useState(0);
  const [theme, setTheme] = useState("light");

  console.log("Parent rendered — theme:", theme, "count:", count);

  // useCallback: onIncrement won't change when theme toggles
  const onIncrement = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  const bg = theme === "dark" ? "#1a1a2e" : "#f0f4ff";
  const color = theme === "dark" ? "#e2e8f0" : "#1a1a2e";

  return (
    <div>
      <h2>Q15 — Counter + Child Button (useCallback)</h2>
      <div style={{
        background: bg, color, padding: "24px", borderRadius: "12px",
        transition: "all 0.3s", display: "inline-block", minWidth: "300px"
      }}>
        <p style={{ fontSize: "1.8rem", fontWeight: 700, margin: "0 0 12px" }}>
          Count: {count}
        </p>
        <div style={{ display: "flex", gap: "12px", alignItems: "center", flexWrap: "wrap" }}>
          <IncrementButton onIncrement={onIncrement} />
          <button
            onClick={() => setTheme(t => t === "light" ? "dark" : "light")}
            style={{
              background: theme === "dark" ? "#f59e0b" : "#1a1a2e",
              color: "#fff", border: "none", borderRadius: "8px",
              padding: "10px 18px", cursor: "pointer", fontWeight: 600
            }}
          >
            {theme === "dark" ? "☀️ Light" : "🌙 Dark"}
          </button>
        </div>
        <p style={{ fontSize: "0.78rem", color: "#94a3b8", marginTop: "12px" }}>
          Toggle theme → Parent re-renders, but IncrementButton does NOT (check console).
        </p>
      </div>
    </div>
  );
}

export default Q15CounterCallback;
