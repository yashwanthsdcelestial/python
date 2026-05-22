import React from "react";

const IncrementButton = React.memo(({ onIncrement }) => {
  console.log("IncrementButton rendered");
  return (
    <button
      onClick={onIncrement}
      style={{
        background: "#4f8ef7", color: "#fff", border: "none",
        borderRadius: "8px", padding: "10px 24px",
        cursor: "pointer", fontWeight: 700, fontSize: "1rem"
      }}
    >
      ➕ Increment
    </button>
  );
});

export default IncrementButton;
