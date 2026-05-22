import React, { Suspense, lazy, useState } from 'react';

class ErrorBoundary extends React.Component {
  constructor(props) { super(props); this.state = { hasError: false, error: null }; }
  static getDerivedStateFromError(error) { return { hasError: true, error }; }
  componentDidCatch(err, info) { console.error('ErrorBoundary caught:', err, info); }
  render() {
    if (this.state.hasError) return (
      <div className="error-banner" style={{ borderRadius: 8, padding: 20 }}>
        <strong>💥 Something went wrong!</strong>
        <p style={{ fontSize: 13, marginTop: 6 }}>{this.state.error?.message}</p>
        <button className="btn btn-secondary" style={{ marginTop: 10 }}
          onClick={() => this.setState({ hasError: false, error: null })}>
          🔄 Try Again
        </button>
      </div>
    );
    return this.props.children;
  }
}

function Skeleton() {
  return (
    <div style={{ padding: 20 }}>
      {[1,2,3].map(i => (
        <div key={i} style={{ height: 16, background: 'linear-gradient(90deg,#eee 25%,#f5f5f5 50%,#eee 75%)', backgroundSize: '200% 100%', borderRadius: 4, marginBottom: 10, animation: 'shimmer 1.5s infinite' }} />
      ))}
      <style>{`@keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }`}</style>
    </div>
  );
}

// Lazy components defined inline
const LazyA = lazy(() => new Promise(r => setTimeout(() => r({ default: () => <div className="success-banner">✅ Component A loaded lazily!</div> }), 800)));
const LazyB = lazy(() => new Promise(r => setTimeout(() => r({ default: () => <div className="success-banner" style={{ background: '#d1ecf1', color: '#0c5460', borderColor: '#bee5eb' }}>✅ Component B loaded lazily!</div> }), 1000)));
function BuggyComponent() { throw new Error('I crashed intentionally! 🐛'); }
const LazyC = lazy(() => new Promise(r => setTimeout(() => r({ default: BuggyComponent }), 600)));

export default function Q14() {
  const [show, setShow] = useState({ a: false, b: false, c: false });

  return (
    <div className="page">
      <div className="card">
        <h2>Q14 — Error Boundary + Lazy Loading</h2>
        <p style={{ fontSize: 13, color: '#666', marginBottom: 20 }}>
          Each component is lazy-loaded with Suspense (skeleton fallback). Component C intentionally throws an error caught by the ErrorBoundary.
        </p>
        <div style={{ display: 'flex', gap: 10, marginBottom: 20, flexWrap: 'wrap' }}>
          <button className="btn btn-primary" onClick={() => setShow(s => ({ ...s, a: true }))}>Load Component A</button>
          <button className="btn btn-primary" onClick={() => setShow(s => ({ ...s, b: true }))}>Load Component B</button>
          <button className="btn btn-danger" onClick={() => setShow(s => ({ ...s, c: true }))}>Load Buggy Component C</button>
        </div>
        {show.a && (
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 12, color: '#888', marginBottom: 4 }}>Component A:</div>
            <ErrorBoundary><Suspense fallback={<Skeleton />}><LazyA /></Suspense></ErrorBoundary>
          </div>
        )}
        {show.b && (
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 12, color: '#888', marginBottom: 4 }}>Component B:</div>
            <ErrorBoundary><Suspense fallback={<Skeleton />}><LazyB /></Suspense></ErrorBoundary>
          </div>
        )}
        {show.c && (
          <div style={{ marginBottom: 12 }}>
            <div style={{ fontSize: 12, color: '#888', marginBottom: 4 }}>Component C (buggy):</div>
            <ErrorBoundary><Suspense fallback={<Skeleton />}><LazyC /></Suspense></ErrorBoundary>
          </div>
        )}
      </div>
    </div>
  );
}
