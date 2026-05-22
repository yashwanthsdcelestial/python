import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement, reset, incrementByAmount } from '../store/slices/counterSlice';

function CountDisplay({ label }) {
  const count = useSelector(s => s.counter.value);
  return (
    <div style={{ background: '#e0e7ff', borderRadius: 8, padding: '16px 24px', textAlign: 'center' }}>
      <div style={{ fontSize: 12, color: '#666' }}>{label}</div>
      <div style={{ fontSize: 48, fontWeight: 700, color: '#4361ee' }}>{count}</div>
    </div>
  );
}

export default function Q16() {
  const dispatch = useDispatch();
  return (
    <div className="page">
      <div className="card">
        <h2>Q16 — Redux Counter</h2>
        <p style={{ fontSize: 13, color: '#666', marginBottom: 20 }}>
          Both components below share the same Redux state — changing the count in one updates the other instantly.
        </p>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 24 }}>
          <CountDisplay label="Component A" />
          <CountDisplay label="Component B" />
        </div>
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', justifyContent: 'center' }}>
          <button className="btn btn-primary" onClick={() => dispatch(increment())}>+ Increment</button>
          <button className="btn btn-secondary" onClick={() => dispatch(decrement())}>− Decrement</button>
          <button className="btn btn-primary" onClick={() => dispatch(incrementByAmount(5))}>+5</button>
          <button className="btn btn-danger" onClick={() => dispatch(reset())}>↺ Reset</button>
        </div>
      </div>
    </div>
  );
}
