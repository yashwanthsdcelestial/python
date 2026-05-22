import React, { useState, useEffect, useRef } from "react";

function Q9Clock() {
  const [time, setTime] = useState(new Date());
  const [running, setRunning] = useState(true);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (running) {
      intervalRef.current = setInterval(() => setTime(new Date()), 1000);
    }
    return () => clearInterval(intervalRef.current);
  }, [running]);

  const pad = (n) => String(n).padStart(2, "0");
  const formatted = `${pad(time.getHours())}:${pad(time.getMinutes())}:${pad(time.getSeconds())}`;

  return (
    <div>
      <h2>Q9 — Live Clock with useEffect</h2>
      <div style={{
        fontFamily: "monospace", fontSize: "2.5rem", fontWeight: 700,
        letterSpacing: "4px", color: "#1a1a2e", marginBottom: "12px"
      }}>
        {formatted}
      </div>
      <button
        onClick={() => setRunning(r => !r)}
        style={{
          background: running ? "#ef4444" : "#22c55e",
          color: "#fff", border: "none", borderRadius: "8px",
          padding: "8px 22px", cursor: "pointer", fontWeight: 600
        }}
      >
        {running ? "⏸ Pause" : "▶ Resume"}
      </button>
    </div>
  );
}

export default Q9Clock;
