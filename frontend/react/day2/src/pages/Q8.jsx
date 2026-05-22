import React, { useState } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

export default function Q8() {
  const [notes, setNotes] = useLocalStorage('q8-notes', []);
  const [input, setInput] = useState('');

  const addNote = () => {
    if (!input.trim()) return;
    setNotes(n => [...n, { id: Date.now(), text: input.trim(), created: new Date().toLocaleString() }]);
    setInput('');
  };

  const deleteNote = id => setNotes(n => n.filter(note => note.id !== id));

  return (
    <div className="page">
      <div className="card">
        <h2>Q8 — useLocalStorage Notes App</h2>
        <p style={{ fontSize: 13, color: '#666', marginBottom: 16 }}>
          Notes persist across page refreshes via <code>useLocalStorage</code> hook.
        </p>
        <div style={{ display: 'flex', gap: 8, marginBottom: 20 }}>
          <input
            style={{ flex: 1, padding: '9px 12px', border: '1.5px solid #d0d0d0', borderRadius: 7, fontSize: 14 }}
            placeholder="Type a note..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && addNote()}
          />
          <button className="btn btn-primary" onClick={addNote}>Add</button>
        </div>
        {notes.length === 0 ? (
          <div style={{ color: '#888', textAlign: 'center', padding: 32 }}>No notes yet. Add one above!</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
            {notes.map(note => (
              <div key={note.id} style={{ background: '#fffbea', border: '1px solid #ffe066', borderRadius: 8, padding: 14, display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ fontSize: 14 }}>{note.text}</div>
                  <div style={{ fontSize: 11, color: '#aaa', marginTop: 4 }}>{note.created}</div>
                </div>
                <button className="btn btn-danger" style={{ fontSize: 11, padding: '3px 8px' }} onClick={() => deleteNote(note.id)}>Delete</button>
              </div>
            ))}
          </div>
        )}
        <div style={{ marginTop: 16, fontSize: 12, color: '#888' }}>Total notes: {notes.length}</div>
      </div>
    </div>
  );
}
