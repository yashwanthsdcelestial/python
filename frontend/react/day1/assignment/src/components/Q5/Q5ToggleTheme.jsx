import React, { useState } from "react";

function Q5ToggleTheme() {
  const [isDark, setIsDark] = useState(false);

  const style = {
    background: isDark ? "#1a1a2e" : "#f0f4ff",
    color: isDark ? "#e2e8f0" : "#1a1a2e",
    padding: "24px",
    borderRadius: "12px",
    transition: "all 0.3s ease",
  };

  return (
    <div>
      <h2>Q5 — Toggle Theme</h2>
      <div style={style}>
        <p style={{ marginTop: 0 }}>
          Currently in <strong>{isDark ? "Dark Mode " : "Light Mode "}</strong>
        </p>
        <button
          onClick={() => setIsDark(d => !d)}
          style={{
            background: isDark ? "#4f8ef7" : "#1a1a2e",
            color: "#fff",
            border: "none",
            borderRadius: "8px",
            padding: "10px 20px",
            cursor: "pointer",
            fontWeight: 600,
          }}
        >
          Switch to {isDark ? "Light" : "Dark"} Mode
        </button>
      </div>
    </div>
  );
}

export default Q5ToggleTheme;
