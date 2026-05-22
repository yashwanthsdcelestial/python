import React, { useState, useCallback } from "react";
import TodoItem from "./TodoItem";

function Q14TodoCallback() {
  const [todos, setTodos] = useState([
    { id: 1, text: "Learn React Hooks" },
    { id: 2, text: "Practice useCallback" },
    { id: 3, text: "Build a project" },
  ]);
  const [input, setInput] = useState("");
  const [unrelated, setUnrelated] = useState(0);

  // useCallback: deleteTodo reference won't change on unrelated state updates
  const deleteTodo = useCallback((id) => {
    setTodos(prev => prev.filter(t => t.id !== id));
  }, []);

  const addTodo = () => {
    const trimmed = input.trim();
    if (!trimmed) return;
    setTodos(prev => [...prev, { id: Date.now(), text: trimmed }]);
    setInput("");
  };

  return (
    <div>
      <h2>Q14 — Todo List with useCallback + React.memo</h2>
      <p style={{ color: "#64748b", fontSize: "0.85rem" }}>
        Unrelated counter (won't re-render todo items): <strong>{unrelated}</strong>
        <button onClick={() => setUnrelated(n => n + 1)} style={{ marginLeft: "10px", padding: "4px 12px" }}>+</button>
      </p>

      <div style={{ display: "flex", gap: "8px", marginBottom: "12px" }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="New todo..."
          style={{ padding: "8px 12px", borderRadius: "6px", border: "1.5px solid #cbd5e1", width: "220px" }}
        />
        <button
          onClick={addTodo}
          style={{ background: "#4f8ef7", color: "#fff", border: "none", borderRadius: "6px", padding: "8px 18px", cursor: "pointer", fontWeight: 600 }}
        >
          Add
        </button>
      </div>

      <ul style={{ listStyle: "none", padding: 0, maxWidth: "400px" }}>
        {todos.map(todo => (
          <TodoItem key={todo.id} todo={todo} onDelete={deleteTodo} />
        ))}
      </ul>
      <p style={{ fontSize: "0.78rem", color: "#94a3b8" }}>
        Check console — TodoItem renders only when necessary.
      </p>
    </div>
  );
}

export default Q14TodoCallback;
