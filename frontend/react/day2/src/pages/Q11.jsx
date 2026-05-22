import React from 'react';
import { Routes, Route, Link, NavLink, useParams, useNavigate } from 'react-router-dom';
import { useFetch } from '../hooks/useFetch';

function BlogHome() {
  const { data, loading, error } = useFetch('https://jsonplaceholder.typicode.com/posts?_limit=10');
  return (
    <div>
      <h3 style={{ marginBottom: 16 }}>📰 Latest Posts</h3>
      {loading && <div className="spinner" />}
      {error && <div className="error-banner">{error}</div>}
      {data && data.map(p => (
        <div key={p.id} style={{ padding: '12px 0', borderBottom: '1px solid #eee' }}>
          <Link to={`posts/${p.id}`} style={{ fontWeight: 600, color: '#4361ee', textDecoration: 'none', fontSize: 14 }}>
            #{p.id} {p.title}
          </Link>
          <p style={{ fontSize: 13, color: '#666', marginTop: 4, lineHeight: 1.5 }}>{p.body.substring(0, 80)}...</p>
        </div>
      ))}
    </div>
  );
}

function PostDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { data, loading } = useFetch(`https://jsonplaceholder.typicode.com/posts/${id}`);
  return (
    <div>
      <button className="btn btn-secondary" style={{ marginBottom: 16 }} onClick={() => navigate(-1)}>← Back to Home</button>
      {loading && <div className="spinner" />}
      {data && (
        <div>
          <h3 style={{ marginBottom: 12 }}>{data.title}</h3>
          <p style={{ lineHeight: 1.8, color: '#444' }}>{data.body}</p>
          <div style={{ marginTop: 12, fontSize: 12, color: '#888' }}>Post ID: {data.id} · User ID: {data.userId}</div>
        </div>
      )}
    </div>
  );
}

function AboutPage() {
  return <div><h3>About this Blog</h3><p style={{ marginTop: 12, color: '#555', lineHeight: 1.8 }}>This is a React Router demo blog app fetching posts from JSONPlaceholder API. Built for Q11 of React Day 2 Assignments.</p></div>;
}

function NotFound() {
  const navigate = useNavigate();
  return (
    <div style={{ textAlign: 'center', padding: 32 }}>
      <div style={{ fontSize: 64 }}>🔍</div>
      <h3>404 — Page Not Found</h3>
      <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => navigate('q11')}>Go Home</button>
    </div>
  );
}

const navStyle = ({ isActive }) => ({
  padding: '6px 14px', borderRadius: 6, textDecoration: 'none', fontSize: 13, fontWeight: 600,
  background: isActive ? '#4361ee' : '#eee', color: isActive ? '#fff' : '#333'
});

export default function Q11() {
  return (
    <div className="page">
      <div className="card">
        <h2>Q11 — Multi-Page Blog with React Router</h2>
        <div style={{ display: 'flex', gap: 8, marginBottom: 24 }}>
          <NavLink to="." end style={navStyle}>🏠 Home</NavLink>
          <NavLink to="about" style={navStyle}>ℹ️ About</NavLink>
        </div>
        <Routes>
          <Route index element={<BlogHome />} />
          <Route path="posts/:id" element={<PostDetail />} />
          <Route path="about" element={<AboutPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </div>
  );
}
