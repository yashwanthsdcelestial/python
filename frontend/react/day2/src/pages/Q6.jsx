import React, { useReducer } from 'react';

const INIT = { step: 1, personal: { name: '', email: '', phone: '' }, address: { street: '', city: '', pincode: '' }, submitted: false };

function reducer(state, action) {
  switch (action.type) {
    case 'SET_PERSONAL': return { ...state, personal: { ...state.personal, ...action.payload } };
    case 'SET_ADDRESS': return { ...state, address: { ...state.address, ...action.payload } };
    case 'NEXT': return { ...state, step: state.step + 1 };
    case 'BACK': return { ...state, step: state.step - 1 };
    case 'SUBMIT': return { ...state, submitted: true };
    case 'RESET': return INIT;
    default: return state;
  }
}

function validatePersonal(p) {
  const e = {};
  if (!p.name.trim()) e.name = 'Required';
  if (!p.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) e.email = 'Valid email required';
  if (!p.phone.match(/^\d{10}$/)) e.phone = '10-digit number required';
  return e;
}

function validateAddress(a) {
  const e = {};
  if (!a.street.trim()) e.street = 'Required';
  if (!a.city.trim()) e.city = 'Required';
  if (!a.pincode.match(/^\d{6}$/)) e.pincode = '6-digit pincode required';
  return e;
}

export default function Q6() {
  const [state, dispatch] = useReducer(reducer, INIT);
  const [errors, setErrors] = React.useState({});

  const handleNext = () => {
    const errs = state.step === 1 ? validatePersonal(state.personal) : validateAddress(state.address);
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setErrors({});
    dispatch({ type: 'NEXT' });
  };

  const steps = ['Personal Info', 'Address', 'Review & Submit'];

  return (
    <div className="page">
      <div className="card">
        <h2>Q6 — Multi-Step Form</h2>
        <div style={{ display: 'flex', gap: 0, marginBottom: 24 }}>
          {steps.map((s, i) => (
            <div key={s} style={{ flex: 1, textAlign: 'center', padding: '8px 4px', fontSize: 13, fontWeight: 600,
              background: state.step === i + 1 ? '#4361ee' : state.step > i + 1 ? '#2dc653' : '#eee',
              color: state.step >= i + 1 ? '#fff' : '#888',
              borderRadius: i === 0 ? '8px 0 0 8px' : i === 2 ? '0 8px 8px 0' : 0 }}>
              {state.step > i + 1 ? '✓ ' : ''}{s}
            </div>
          ))}
        </div>

        {state.submitted ? (
          <>
            <div className="success-banner">🎉 Form submitted successfully!</div>
            <pre style={{ background: '#f8f9fa', padding: 16, borderRadius: 8, fontSize: 13, marginTop: 12 }}>
              {JSON.stringify({ personal: state.personal, address: state.address }, null, 2)}
            </pre>
            <button className="btn btn-secondary" style={{ marginTop: 12 }} onClick={() => dispatch({ type: 'RESET' })}>Start Over</button>
          </>
        ) : state.step === 1 ? (
          <div>
            <h3 style={{ marginBottom: 16 }}>Personal Information</h3>
            {[['name','Full Name','text'],['email','Email','email'],['phone','Phone','tel']].map(([k,l,t]) => (
              <div className="form-group" key={k}>
                <label>{l}</label>
                <input type={t} value={state.personal[k]}
                  onChange={e => dispatch({ type: 'SET_PERSONAL', payload: { [k]: e.target.value } })} />
                {errors[k] && <div className="error">{errors[k]}</div>}
              </div>
            ))}
            <button className="btn btn-primary" onClick={handleNext}>Next →</button>
          </div>
        ) : state.step === 2 ? (
          <div>
            <h3 style={{ marginBottom: 16 }}>Address</h3>
            {[['street','Street Address'],['city','City'],['pincode','Pincode']].map(([k,l]) => (
              <div className="form-group" key={k}>
                <label>{l}</label>
                <input type="text" value={state.address[k]}
                  onChange={e => dispatch({ type: 'SET_ADDRESS', payload: { [k]: e.target.value } })} />
                {errors[k] && <div className="error">{errors[k]}</div>}
              </div>
            ))}
            <div style={{ display: 'flex', gap: 12 }}>
              <button className="btn btn-secondary" onClick={() => dispatch({ type: 'BACK' })}>← Back</button>
              <button className="btn btn-primary" onClick={handleNext}>Next →</button>
            </div>
          </div>
        ) : (
          <div>
            <h3 style={{ marginBottom: 16 }}>Review & Submit</h3>
            <div style={{ background: '#f8f9fa', padding: 16, borderRadius: 8, marginBottom: 16 }}>
              <h4>Personal</h4>
              {Object.entries(state.personal).map(([k,v]) => <div key={k} style={{ fontSize: 14, margin: '4px 0' }}><strong>{k}:</strong> {v}</div>)}
              <h4 style={{ marginTop: 12 }}>Address</h4>
              {Object.entries(state.address).map(([k,v]) => <div key={k} style={{ fontSize: 14, margin: '4px 0' }}><strong>{k}:</strong> {v}</div>)}
            </div>
            <div style={{ display: 'flex', gap: 12 }}>
              <button className="btn btn-secondary" onClick={() => dispatch({ type: 'BACK' })}>← Back</button>
              <button className="btn btn-success" onClick={() => dispatch({ type: 'SUBMIT' })}>✓ Submit</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
