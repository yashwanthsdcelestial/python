import React, { useState, useEffect } from "react";

function Q10UsersFetcher() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [trigger, setTrigger] = useState(0);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    fetch("https://jsonplaceholder.typicode.com/users")
      .then(res => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then(data => {
        if (!cancelled) { setUsers(data); setLoading(false); }
      })
      .catch(err => {
        if (!cancelled) { setError(err.message); setLoading(false); }
      });

    return () => { cancelled = true; };
  }, [trigger]);

  return (
    <div>
      <h2>Q10 — Users Fetcher with useEffect</h2>
      <button
        onClick={() => setTrigger(t => t + 1)}
        style={{ marginBottom: "12px", background: "#4f8ef7", color: "#fff", border: "none", borderRadius: "6px", padding: "8px 18px", cursor: "pointer", fontWeight: 600 }}
      >
        🔄 Refresh
      </button>

      {loading && <p style={{ color: "#4f8ef7" }}>Loading...</p>}
      {error && <p style={{ color: "#ef4444" }}>Error: {error}</p>}
      {!loading && !error && (
        <ul style={{ paddingLeft: "20px" }}>
          {users.map(u => (
            <li key={u.id} style={{ marginBottom: "4px" }}>
              <strong>{u.name}</strong> — {u.email}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Q10UsersFetcher;
