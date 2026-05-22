import React, { useState } from "react";

function Q7TodoList() {
  const [input, setInput] = useState("");
  const [tasks, setTasks] = useState([]);

  const addTask = () => {
    const trimmed = input.trim();
    if (!trimmed) return;
    setTasks(t => [...t, { id: Date.now(), text: trimmed }]);
    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") addTask();
  };

  return (
    <div>
      <h2>Q7 — Simple To-Do List</h2>
      <div style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Enter a task..."
          style={{ padding: "8px 12px", borderRadius: "6px", border: "1.5px solid #cbd5e1", fontSize: "0.95rem", width: "240px" }}
        />
        <button
          onClick={addTask}
          style={{ background: "#4f8ef7", color: "#fff", border: "none", borderRadius: "6px", padding: "8px 18px", cursor: "pointer", fontWeight: 600 }}
        >
          Add
        </button>
      </div>

      {tasks.length === 0 ? (
        <p style={{ color: "#94a3b8", fontStyle: "italic" }}>No tasks yet.</p>
      ) : (
        <ul style={{ paddingLeft: "20px" }}>
          {tasks.map(t => (
            <li key={t.id} style={{ marginBottom: "6px", fontSize: "0.95rem" }}>{t.text}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Q7TodoList;
