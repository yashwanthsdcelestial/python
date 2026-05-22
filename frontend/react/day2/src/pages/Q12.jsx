import React, { useState } from 'react';
import { Routes, Route, Navigate, Link, Outlet, useNavigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from '../context/AuthContext';

function LoginPage() {
  const { login, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || 'dashboard';
  const [creds, setCreds] = useState({ username: '', password: '' });
  const [err, setErr] = useState('');

  if (isAuthenticated) return <Navigate to={from} replace />;

  const handleLogin = e => {
    e.preventDefault();
    if (!creds.username || !creds.password) { setErr('Both fields required'); return; }
    login(creds.username);
    navigate(from, { replace: true });
  };
  return (
    <div style={{ maxWidth: 360, margin: '0 auto', padding: '24px 0' }}>
      <div className="card">
        <h3 style={{ marginBottom: 20 }}>🔐 Login</h3>
        {err && <div className="error-banner">{err}</div>}
        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label>Username</label>
            <input value={creds.username} onChange={e => setCreds(c => ({ ...c, username: e.target.value }))} />
          </div>
          <div className="form-group">
            <label>Password</label>
            <input type="password" value={creds.password} onChange={e => setCreds(c => ({ ...c, password: e.target.value }))} />
          </div>
          <button className="btn btn-primary" type="submit">Login</button>
        </form>
        <p style={{ fontSize: 12, color: '#888', marginTop: 12 }}>Any non-empty username/password works.</p>
      </div>
    </div>
  );
}

function ProtectedRoute() {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  if (!isAuthenticated) return <Navigate to="login" state={{ from: location.pathname }} replace />;
  return <Outlet />;
}

function DashboardLayout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const handleLogout = () => { logout(); navigate('login'); };
  return (
    <div>
      <div style={{ background: '#1a1a2e', color: '#fff', padding: '12px 20px', borderRadius: 8, marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', gap: 16 }}>
          <Link to="." style={{ color: '#a0c4ff', textDecoration: 'none', fontSize: 13 }}>Dashboard</Link>
          <Link to="profile" style={{ color: '#a0c4ff', textDecoration: 'none', fontSize: 13 }}>Profile</Link>
          <Link to="settings" style={{ color: '#a0c4ff', textDecoration: 'none', fontSize: 13 }}>Settings</Link>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontSize: 13 }}>
          <span>👤 {user}</span>
          <button className="btn btn-danger" style={{ fontSize: 12, padding: '4px 12px' }} onClick={handleLogout}>Logout</button>
        </div>
      </div>
      <Outlet />
    </div>
  );
}

function DashHome() { return <div className="success-banner">🏠 Welcome to the Dashboard! You are logged in.</div>; }
function ProfilePage() { const { user } = useAuth(); return <div style={{ padding: 16 }}><h4>Profile</h4><p style={{ marginTop: 8 }}>Username: <strong>{user}</strong></p></div>; }
function SettingsPage() { return <div style={{ padding: 16 }}><h4>Settings</h4><p style={{ marginTop: 8, color: '#666' }}>App settings would go here.</p></div>; }

export default function Q12() {
  return (
    <AuthProvider>
      <div className="page">
        <div className="card">
          <h2>Q12 — Protected Dashboard with Fake Auth</h2>
          <Routes>
            <Route path="login" element={<LoginPage />} />
            <Route element={<ProtectedRoute />}>
              <Route path="dashboard/*" element={<DashboardLayout />}>
                <Route index element={<DashHome />} />
                <Route path="profile" element={<ProfilePage />} />
                <Route path="settings" element={<SettingsPage />} />
              </Route>
            </Route>
            <Route index element={<Navigate to="login" replace />} />
          </Routes>
        </div>
      </div>
    </AuthProvider>
  );
}
