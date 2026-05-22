import React, { useState, useRef } from 'react';

function fmt(ms) {
  const m = Math.floor(ms / 60000);
  const s = Math.floor((ms % 60000) / 1000);
  const cs = Math.floor((ms % 1000) / 10);
  return `${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}:${String(cs).padStart(2,'0')}`;
}

export default function Q10() {
  const [elapsed, setElapsed] = useState(0);
  const [running, setRunning] = useState(false);
  const [laps, setLaps] = useState([]);
  const intervalRef = useRef(null);
  const startTimeRef = useRef(0);
  const elapsedRef = useRef(0);

  const start = () => {
    if (running) return;
    startTimeRef.current = Date.now() - elapsedRef.current;
    intervalRef.current = setInterval(() => {
      const now = Date.now() - startTimeRef.current;
      elapsedRef.current = now;
      setElapsed(now);
    }, 10);
    setRunning(true);
  };

  const pause = () => {
    clearInterval(intervalRef.current);
    setRunning(false);
  };

  const reset = () => {
    clearInterval(intervalRef.current);
    setRunning(false);
    setElapsed(0);
    setLaps([]);
    elapsedRef.current = 0;
  };

  const lap = () => {
    if (running) setLaps(l => [...l, elapsedRef.current]);
  };

  return (
    <div className="page">
      <div className="card">
        <h2>Q10 — Stopwatch with useRef</h2>
        <div style={{ textAlign: 'center', margin: '24px 0' }}>
          <div style={{ fontFamily: 'monospace', fontSize: 56, fontWeight: 700, color: '#1a1a2e', letterSpacing: 2 }}>
            {fmt(elapsed)}
          </div>
          <div style={{ color: '#888', fontSize: 12, marginTop: 4 }}>mm:ss:cs</div>
        </div>
        <div style={{ display: 'flex', justifyContent: 'center', gap: 12, marginBottom: 24 }}>
          {!running ? (
            <button className="btn btn-success" onClick={start}>{elapsed === 0 ? '▶ Start' : '▶ Resume'}</button>
          ) : (
            <button className="btn btn-secondary" onClick={pause}>⏸ Pause</button>
          )}
          <button className="btn btn-secondary" onClick={lap} disabled={!running}>⚑ Lap</button>
          <button className="btn btn-danger" onClick={reset}>↺ Reset</button>
        </div>
        {laps.length > 0 && (
          <div>
            <h4 style={{ marginBottom: 10 }}>Lap Times</h4>
            {laps.map((l, i) => (
              <div key={i} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 0', borderBottom: '1px solid #eee', fontSize: 14 }}>
                <span style={{ color: '#888' }}>Lap {i + 1}</span>
                <span style={{ fontFamily: 'monospace', fontWeight: 600 }}>{fmt(l)}</span>
                {i > 0 && <span style={{ color: '#666', fontSize: 12 }}>+{fmt(l - laps[i-1])}</span>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
