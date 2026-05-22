import React, { useState, useEffect } from 'react';
import axios from 'axios';

const api = axios.create({ baseURL: 'https://jsonplaceholder.typicode.com' });

export default function Q13() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [toast, setToast] = useState(null);
  const [form, setForm] = useState({ name: '', email: '', phone: '' });
  const [editing, setEditing] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const showToast = (msg, type = 'success') => { setToast({ msg, type }); setTimeout(() => setToast(null), 3000); };

  useEffect(() => {
    setLoading(true);
    api.get('/users').then(r => { setUsers(r.data.slice(0, 6)); setLoading(false); }).catch(() => setLoading(false));
  }, []);

  const handleSubmit = async e => {
    e.preventDefault();
    setSubmitting(true);
    if (editing) {
      await api.put(`/users/${editing}`, form);
      setUsers(u => u.map(x => x.id === editing ? { ...x, ...form } : x));
      showToast('User updated!');
      setEditing(null);
    } else {
      const r = await api.post('/users', form);
      setUsers(u => [...u, { ...r.data, id: Date.now() }]);
      showToast('User created!');
    }
    setForm({ name: '', email: '', phone: '' });
    setSubmitting(false);
  };

  const handleDelete = async id => {
    await api.delete(`/users/${id}`);
    setUsers(u => u.filter(x => x.id !== id));
    showToast('User deleted!', 'error');
  };

  const startEdit = u => { setEditing(u.id); setForm({ name: u.name, email: u.email, phone: u.phone }); };

  return (
    <div className="page">
      <div className="card">
        <h2>Q13 — CRUD App with Axios</h2>
        {toast && <div className={toast.type === 'error' ? 'error-banner' : 'success-banner'} style={{ marginBottom: 12 }}>{toast.msg}</div>}
        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8, marginBottom: 20, flexWrap: 'wrap' }}>
          {[['name','Name'],['email','Email'],['phone','Phone']].map(([k,p]) => (
            <input key={k} style={{ flex: 1, minWidth: 120, padding: '8px 12px', border: '1.5px solid #d0d0d0', borderRadius: 7, fontSize: 13 }}
              placeholder={p} value={form[k]} onChange={e => setForm(f => ({ ...f, [k]: e.target.value }))} required />
          ))}
          <button className="btn btn-primary" type="submit" disabled={submitting}>
            {submitting ? '...' : editing ? 'Update' : '+ Add'}
          </button>
          {editing && <button className="btn btn-secondary" type="button" onClick={() => { setEditing(null); setForm({ name:'',email:'',phone:'' }); }}>Cancel</button>}
        </form>
        {loading ? <div className="spinner" /> : (
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13 }}>
            <thead>
              <tr style={{ background: '#f0f2f5' }}>
                {['Name','Email','Phone','Actions'].map(h => <th key={h} style={{ padding: '8px 12px', textAlign: 'left', fontWeight: 600 }}>{h}</th>)}
              </tr>
            </thead>
            <tbody>
              {users.map(u => (
                <tr key={u.id} style={{ borderBottom: '1px solid #eee' }}>
                  <td style={{ padding: '8px 12px' }}>{u.name}</td>
                  <td style={{ padding: '8px 12px', color: '#666' }}>{u.email}</td>
                  <td style={{ padding: '8px 12px', color: '#666' }}>{u.phone}</td>
                  <td style={{ padding: '8px 12px' }}>
                    <div style={{ display: 'flex', gap: 6 }}>
                      <button className="btn btn-secondary" style={{ fontSize: 11, padding: '3px 10px' }} onClick={() => startEdit(u)}>Edit</button>
                      <button className="btn btn-danger" style={{ fontSize: 11, padding: '3px 10px' }} onClick={() => handleDelete(u.id)}>Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
