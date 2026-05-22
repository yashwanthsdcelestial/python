import React from "react";

function Button({ label, color = "#4f8ef7", onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        backgroundColor: color,
        color: "#fff",
        border: "none",
        borderRadius: "8px",
        padding: "10px 22px",
        fontSize: "0.95rem",
        cursor: "pointer",
        fontWeight: 600,
        transition: "opacity 0.2s",
      }}
      onMouseOver={(e) => (e.target.style.opacity = 0.85)}
      onMouseOut={(e) => (e.target.style.opacity = 1)}
    >
      {label}
    </button>
  );
}

export default Button;
