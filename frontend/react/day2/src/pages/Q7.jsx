import React from 'react';
import { useFetch } from '../hooks/useFetch';

function UsersList() {
  const { data, loading, error, refetch } = useFetch('https://jsonplaceholder.typicode.com/users');
  return (
    <div style={{ marginBottom: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3>Users</h3>
        <button className="btn btn-secondary" style={{ fontSize: 12 }} onClick={refetch}>↻ Refetch</button>
      </div>
      {loading && <div className="spinner" />}
      {error && <div className="error-banner">Error: {error}</div>}
      {data && data.slice(0,5).map(u => (
        <div key={u.id} style={{ padding: '6px 0', borderBottom: '1px solid #eee', fontSize: 14 }}>
          <strong>{u.name}</strong> — {u.email}
        </div>
      ))}
    </div>
  );
}

function PostsList() {
  const { data, loading, error, refetch } = useFetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
        <h3>📝 Posts</h3>
        <button className="btn btn-secondary" style={{ fontSize: 12 }} onClick={refetch}>↻ Refetch</button>
      </div>
      {loading && <div className="spinner" />}
      {error && <div className="error-banner">Error: {error}</div>}
      {data && data.map(p => (
        <div key={p.id} style={{ padding: '6px 0', borderBottom: '1px solid #eee', fontSize: 14 }}>
          <strong>#{p.id}</strong> {p.title.substring(0, 50)}...
        </div>
      ))}
    </div>
  );
}

export default function Q7() {
  return (
    <div className="page">
      <div className="card">
        <h2>Q7 — useFetch Custom Hook</h2>
        <p style={{ fontSize: 13, color: '#666', marginBottom: 20 }}>
          Same <code>useFetch</code> hook reused in two completely independent components below.
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
          <div><UsersList /></div>
          <div><PostsList /></div>
        </div>
      </div>
    </div>
  );
}
