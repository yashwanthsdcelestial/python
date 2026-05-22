import React, { useState } from 'react';

const SURVEY_CONFIG = [
  { name: 'fullName', label: 'Full Name', type: 'text', required: true },
  { name: 'email', label: 'Email Address', type: 'email', required: true },
  { name: 'age', label: 'Age', type: 'number', required: true },
  { name: 'country', label: 'Country', type: 'select', required: true, options: ['India', 'USA', 'UK', 'Other'] },
  { name: 'newsletter', label: 'Subscribe to newsletter', type: 'checkbox', required: false },
];

export default function Q3() {
  const [values, setValues] = useState({});
  const [errors, setErrors] = useState({});
  const [submitted, setSubmitted] = useState(null);

  const handleChange = (name, value) => {
    setValues(v => ({ ...v, [name]: value }));
    if (errors[name]) setErrors(e => ({ ...e, [name]: '' }));
  };

  const validate = () => {
    const errs = {};
    SURVEY_CONFIG.forEach(f => {
      if (f.required && (values[f.name] === undefined || values[f.name] === '' || values[f.name] === null)) {
        errs[f.name] = `${f.label} is required`;
      }
    });
    return errs;
  };

  const handleSubmit = e => {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length) { setErrors(errs); return; }
    setSubmitted(values);
  };

  return (
    <div className="page">
      <div className="card">
        <h2>Q3 — Dynamic Survey Form</h2>
        {submitted ? (
          <>
            <div className="success-banner">✅ Survey submitted!</div>
            <pre style={{ background: '#f8f9fa', padding: 16, borderRadius: 8, fontSize: 13 }}>
              {JSON.stringify(submitted, null, 2)}
            </pre>
            <button className="btn btn-secondary" style={{ marginTop: 12 }} onClick={() => { setSubmitted(null); setValues({}); }}>
              Reset
            </button>
          </>
        ) : (
          <form onSubmit={handleSubmit} noValidate>
            {SURVEY_CONFIG.map(field => (
              <div className="form-group" key={field.name}>
                <label>{field.label}{field.required && <span style={{ color: '#e63946' }}> *</span>}</label>
                {field.type === 'select' && (
                  <select value={values[field.name] || ''} onChange={e => handleChange(field.name, e.target.value)}>
                    <option value="">Select...</option>
                    {field.options.map(o => <option key={o} value={o}>{o}</option>)}
                  </select>
                )}
                {field.type === 'checkbox' && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 4 }}>
                    <input type="checkbox" id={field.name} checked={!!values[field.name]}
                      onChange={e => handleChange(field.name, e.target.checked)} style={{ width: 'auto' }} />
                    <label htmlFor={field.name} style={{ marginBottom: 0 }}>Yes</label>
                  </div>
                )}
                {['text','email','number'].includes(field.type) && (
                  <input type={field.type} value={values[field.name] || ''}
                    onChange={e => handleChange(field.name, e.target.value)} />
                )}
                {errors[field.name] && <div className="error">{errors[field.name]}</div>}
              </div>
            ))}
            <button className="btn btn-primary" type="submit">Submit Survey</button>
          </form>
        )}
      </div>
    </div>
  );
}
