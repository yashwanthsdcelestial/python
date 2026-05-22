import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Routes, Route, Navigate, Link, Outlet, useNavigate, useLocation } from 'react-router-dom';
import { login, logout } from '../store/slices/authSlice';

function LoginPageRedux() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const isAuthenticated = useSelector(s => s.auth.isAuthenticated);
  const from = location.state?.from || 'dash';
  const [u, setU] = useState('');
  const [p, setP] = useState('');
  const [err, setErr] = useState('');

  if (isAuthenticated) return <Navigate to={from} replace />;

  const handleLogin = e => {
    e.preventDefault();
    if (!u || !p) { setErr('Both fields required'); return; }
    dispatch(login({ user: u, token: 'redux.jwt.' + btoa(u) }));
    navigate(from, { replace: true });
  };

  return (
    <div style={{ maxWidth: 360, margin: '0 auto' }}>
      <div className="card">
        <h3 style={{ marginBottom: 20 }}>🔐 Redux Auth Login</h3>
        {err && <div className="error-banner" style={{ marginBottom: 12 }}>{err}</div>}
        <form onSubmit={handleLogin}>
          <div className="form-group"><label>Username</label><input value={u} onChange={e => setU(e.target.value)} /></div>
          <div className="form-group"><label>Password</label><input type="password" value={p} onChange={e => setP(e.target.value)} /></div>
          <button className="btn btn-primary" type="submit">Login</button>
        </form>
        <p style={{ fontSize: 12, color: '#888', marginTop: 12 }}>Auth state persists via Redux + localStorage.</p>
      </div>
    </div>
  );
}

function ProtectedRouteRedux() {
  const isAuthenticated = useSelector(s => s.auth.isAuthenticated);
  const location = useLocation();
  if (!isAuthenticated) return <Navigate to="login" state={{ from: location.pathname }} replace />;
  return <Outlet />;
}

function DashLayoutRedux() {
  const dispatch = useDispatch();
  const user = useSelector(s => s.auth.user);
  const navigate = useNavigate();
  const handleLogout = () => { dispatch(logout()); navigate('login'); };
  return (
    <div>
      <div style={{ background: '#1a1a2e', color: '#fff', padding: '12px 20px', borderRadius: 8, marginBottom: 16, display: 'flex', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', gap: 14 }}>
          <Link to="." style={{ color: '#a0c4ff', fontSize: 13, textDecoration: 'none' }}>Home</Link>
          <Link to="profile" style={{ color: '#a0c4ff', fontSize: 13, textDecoration: 'none' }}>Profile</Link>
          <Link to="settings" style={{ color: '#a0c4ff', fontSize: 13, textDecoration: 'none' }}>Settings</Link>
        </div>
        <div style={{ display: 'flex', gap: 12, alignItems: 'center', fontSize: 13 }}>
          <span>👤 {user}</span>
          <button className="btn btn-danger" style={{ fontSize: 12, padding: '4px 12px' }} onClick={handleLogout}>Logout</button>
        </div>
      </div>
      <Outlet />
    </div>
  );
}

function DashHomeRedux() {
  const token = useSelector(s => s.auth.token);
  return <div className="success-banner">🏠 Logged in! Token: <code style={{ fontSize: 11 }}>{token}</code></div>;
}

export default function Q18() {
  return (
    <div className="page">
      <div className="card">
        <h2>Q18 — Redux Auth Slice + Protected Routes</h2>
        <Routes>
          <Route path="login" element={<LoginPageRedux />} />
          <Route element={<ProtectedRouteRedux />}>
            <Route path="dash/*" element={<DashLayoutRedux />}>
              <Route index element={<DashHomeRedux />} />
              <Route path="profile" element={<div style={{ padding: 16 }}>Profile Page</div>} />
              <Route path="settings" element={<div style={{ padding: 16 }}>Settings Page</div>} />
            </Route>
          </Route>
          <Route index element={<Navigate to="login" replace />} />
        </Routes>
      </div>
    </div>
  );
}
