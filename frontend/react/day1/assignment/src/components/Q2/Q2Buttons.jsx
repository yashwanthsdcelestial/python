import React from "react";
import Button from "./Button";

function Q2Buttons() {
  return (
    <div>
      <h2>Q2 — Reusable Button Component</h2>
      <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
        <Button label="Save" color="#22c55e" onClick={() => alert("Saved!")} />
        <Button label="Cancel" color="#94a3b8" onClick={() => alert("Cancelled!")} />
        <Button label="Delete" color="#ef4444" onClick={() => alert("Deleted!")} />
      </div>
    </div>
  );
}

export default Q2Buttons;
