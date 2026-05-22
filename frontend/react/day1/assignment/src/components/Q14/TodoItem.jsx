import React from "react";

const TodoItem = React.memo(({ todo, onDelete }) => {
  console.log(`TodoItem rendered: ${todo.text}`);
  return (
    <li style={{
      display: "flex", justifyContent: "space-between", alignItems: "center",
      padding: "8px 14px", background: "#f8fafc", borderRadius: "6px",
      marginBottom: "6px", border: "1px solid #e2e8f0"
    }}>
      <span style={{ fontSize: "0.95rem" }}>{todo.text}</span>
      <button
        onClick={() => onDelete(todo.id)}
        style={{
          background: "#ef4444", color: "#fff", border: "none",
          borderRadius: "5px", padding: "4px 12px", cursor: "pointer", fontWeight: 600
        }}
      >
        Delete
      </button>
    </li>
  );
});

export default TodoItem;
