import React, { useState } from "react";

function Q6LoginLogout() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <div>
      <h2>Q6 — Login / Logout UI</h2>
      <div style={{
        padding: "24px", background: "#fff", borderRadius: "12px",
        boxShadow: "0 2px 12px rgba(0,0,0,0.08)", display: "inline-block", minWidth: "260px", textAlign: "center"
      }}>
        {isLoggedIn ? (
          <p style={{ fontSize: "1.1rem", color: "#22c55e", fontWeight: 600 }}>Welcome, User!</p>
        ) : (
          <p style={{ fontSize: "1rem", color: "#94a3b8" }}>Please log in to continue.</p>
        )}
        <button
          onClick={() => setIsLoggedIn(v => !v)}
          style={{
            background: isLoggedIn ? "#ef4444" : "#22c55e",
            color: "#fff", border: "none", borderRadius: "8px",
            padding: "10px 28px", cursor: "pointer", fontWeight: 700, fontSize: "1rem"
          }}
        >
          {isLoggedIn ? "Logout" : "Login"}
        </button>
      </div>
    </div>
  );
}

export default Q6LoginLogout;
