import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchUsers } from '../store/slices/usersSlice';

export default function Q19() {
  const dispatch = useDispatch();
  const { items, loading, error } = useSelector(s => s.users);

  useEffect(() => { dispatch(fetchUsers()); }, [dispatch]);

  return (
    <div className="page">
      <div className="card">
        <h2>Q19 — Async Users Fetcher (createAsyncThunk)</h2>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <p style={{ fontSize: 13, color: '#666' }}>Handles pending / fulfilled / rejected states.</p>
          <button className="btn btn-primary" onClick={() => dispatch(fetchUsers())} disabled={loading}>
            {loading ? '⏳ Loading...' : '↻ Refresh'}
          </button>
        </div>
        {loading && (
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, padding: 24, justifyContent: 'center' }}>
            <div className="spinner" /> <span style={{ color: '#666' }}>Fetching users...</span>
          </div>
        )}
        {error && <div className="error-banner">❌ {error}</div>}
        {!loading && items.length > 0 && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(240px,1fr))', gap: 12 }}>
            {items.map(u => (
              <div key={u.id} style={{ background: '#f8f9fa', borderRadius: 10, padding: 16 }}>
                <div style={{ fontWeight: 700, fontSize: 14 }}>{u.name}</div>
                <div style={{ fontSize: 12, color: '#4361ee', margin: '4px 0' }}>{u.email}</div>
                <div style={{ fontSize: 12, color: '#666' }}>{u.phone}</div>
                <div style={{ fontSize: 12, color: '#888', marginTop: 4 }}>🏢 {u.company.name}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
