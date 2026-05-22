import React, { useState, useCallback, useMemo } from 'react';

const USERS = Array.from({ length: 1000 }, (_, i) => ({
  id: i + 1,
  name: `User ${i + 1}`,
  email: `user${i + 1}@example.com`,
  dept: ['Engineering', 'Design', 'Marketing', 'Sales', 'HR'][i % 5],
}));

const UserCard = React.memo(function UserCard({ user, likes, onLike }) {
  console.log(`[Render] UserCard #${user.id}`);
  return (
    <div style={{ background: '#f8f9fa', borderRadius: 8, padding: '10px 14px', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
      <div>
        <div style={{ fontWeight: 600, fontSize: 13 }}>{user.name}</div>
        <div style={{ fontSize: 11, color: '#888' }}>{user.email} · {user.dept}</div>
      </div>
      <button className="btn btn-secondary" style={{ fontSize: 12, padding: '4px 12px' }} onClick={() => onLike(user.id)}>
        ❤️ {likes}
      </button>
    </div>
  );
});

export default function Q15() {
  const [likes, setLikes] = useState({});
  const [search, setSearch] = useState('');

  const handleLike = useCallback((id) => {
    setLikes(l => ({ ...l, [id]: (l[id] || 0) + 1 }));
  }, []);

  const filtered = useMemo(() =>
    search ? USERS.filter(u => u.name.toLowerCase().includes(search.toLowerCase()) || u.dept.toLowerCase().includes(search.toLowerCase())) : USERS
  , [search]);

  return (
    <div className="page">
      <div className="card">
        <h2>Q15 — Optimized Large List (1000 items)</h2>
        <p style={{ fontSize: 13, color: '#666', marginBottom: 16 }}>
          React.memo + useCallback ensures only the liked card re-renders. useMemo filters without re-computation. Check console for render logs.
        </p>
        <div className="form-group">
          <label>Search by name or department</label>
          <input type="text" placeholder="e.g. Engineering, User 42..." value={search} onChange={e => setSearch(e.target.value)} />
        </div>
        <div style={{ fontSize: 12, color: '#888', marginBottom: 12 }}>Showing {filtered.length} of 1000 users</div>
        <div style={{ maxHeight: 400, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: 6 }}>
          {filtered.map(u => (
            <UserCard key={u.id} user={u} likes={likes[u.id] || 0} onLike={handleLike} />
          ))}
        </div>
      </div>
    </div>
  );
}
