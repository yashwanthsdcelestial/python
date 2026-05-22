import React, { useState, useEffect } from 'react';
import { useDebounce } from '../hooks/useDebounce';

export default function Q9() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const debouncedQuery = useDebounce(query, 500);

  useEffect(() => {
    if (!debouncedQuery.trim()) { setResults([]); return; }
    setLoading(true);
    fetch(`https://jsonplaceholder.typicode.com/users`)
      .then(r => r.json())
      .then(data => {
        const filtered = data.filter(u =>
          u.name.toLowerCase().includes(debouncedQuery.toLowerCase()) ||
          u.email.toLowerCase().includes(debouncedQuery.toLowerCase())
        );
        setResults(filtered);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [debouncedQuery]);

  return (
    <div className="page">
      <div className="card">
        <h2>Q9 — useDebounce + Search</h2>
        <p style={{ fontSize: 13, color: '#666', marginBottom: 16 }}>
          API is called only after you stop typing for 500ms. Try searching for "Leanne" or "gmail".
        </p>
        <div className="form-group">
          <label>Search Users</label>
          <input
            type="text"
            placeholder="Type to search..."
            value={query}
            onChange={e => setQuery(e.target.value)}
          />
        </div>
        <div style={{ marginTop: 8, fontSize: 12, color: '#888' }}>
          Debounced: <code style={{ background: '#f0f2f5', padding: '1px 4px', borderRadius: 3 }}>"{debouncedQuery}"</code>
        </div>
        <div style={{ marginTop: 16 }}>
          {loading && <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}><div className="spinner" /><span style={{ fontSize: 14 }}>Searching...</span></div>}
          {!loading && debouncedQuery && results.length === 0 && (
            <div style={{ color: '#888', padding: 16, textAlign: 'center' }}>No results found for "{debouncedQuery}"</div>
          )}
          {results.map(u => (
            <div key={u.id} style={{ padding: '10px 0', borderBottom: '1px solid #eee' }}>
              <div style={{ fontWeight: 600, fontSize: 14 }}>{u.name}</div>
              <div style={{ fontSize: 12, color: '#666' }}>{u.email} · {u.phone}</div>
              <div style={{ fontSize: 12, color: '#888' }}>{u.company.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
