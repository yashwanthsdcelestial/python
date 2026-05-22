import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { addTodo, removeTodo, toggleTodo, clearAll } from '../store/slices/todoSlice';

function AddTodo() {
  const dispatch = useDispatch();
  const [text, setText] = useState('');
  const handleAdd = () => {
    if (!text.trim()) return;
    dispatch(addTodo(text.trim()));
    setText('');
  };
  return (
    <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
      <input style={{ flex: 1, padding: '9px 12px', border: '1.5px solid #d0d0d0', borderRadius: 7, fontSize: 14 }}
        placeholder="Add a task..." value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && handleAdd()} />
      <button className="btn btn-primary" onClick={handleAdd}>Add</button>
    </div>
  );
}

function TodoList() {
  const dispatch = useDispatch();
  const todos = useSelector(s => s.todos.items);
  if (todos.length === 0) return <div style={{ color: '#888', textAlign: 'center', padding: 24 }}>No todos yet!</div>;
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, marginBottom: 16 }}>
      {todos.map(t => (
        <div key={t.id} style={{ display: 'flex', alignItems: 'center', gap: 12, padding: '10px 14px', background: '#f8f9fa', borderRadius: 8 }}>
          <input type="checkbox" checked={t.completed} onChange={() => dispatch(toggleTodo(t.id))} style={{ width: 'auto', cursor: 'pointer' }} />
          <span style={{ flex: 1, fontSize: 14, textDecoration: t.completed ? 'line-through' : 'none', color: t.completed ? '#aaa' : '#222' }}>{t.text}</span>
          <button className="btn btn-danger" style={{ fontSize: 11, padding: '3px 8px' }} onClick={() => dispatch(removeTodo(t.id))}>✕</button>
        </div>
      ))}
    </div>
  );
}

function TodoStats() {
  const todos = useSelector(s => s.todos.items);
  const dispatch = useDispatch();
  const total = todos.length;
  const completed = todos.filter(t => t.completed).length;
  return (
    <div style={{ display: 'flex', gap: 12, justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderTop: '1px solid #eee' }}>
      <div style={{ display: 'flex', gap: 16 }}>
        <span style={{ fontSize: 13 }}>Total: <strong>{total}</strong></span>
        <span style={{ fontSize: 13, color: '#2dc653' }}>Done: <strong>{completed}</strong></span>
        <span style={{ fontSize: 13, color: '#e63946' }}>Pending: <strong>{total - completed}</strong></span>
      </div>
      {total > 0 && <button className="btn btn-danger" style={{ fontSize: 12 }} onClick={() => dispatch(clearAll())}>Clear All</button>}
    </div>
  );
}

export default function Q17() {
  return (
    <div className="page">
      <div className="card">
        <h2>Q17 — Redux Todo List</h2>
        <p style={{ fontSize: 13, color: '#666', marginBottom: 16 }}>
          AddTodo, TodoList and TodoStats are independent components all connected to the Redux store.
        </p>
        <AddTodo />
        <TodoList />
        <TodoStats />
      </div>
    </div>
  );
}
