import React, { useState } from 'react';

function validate(fields) {
  const errors = {};
  if (!fields.name.trim()) errors.name = 'Name is required';
  if (!fields.email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) errors.email = 'Valid email required';
  if (fields.password.length < 8) errors.password = 'Min 8 characters';
  else if (!/\d/.test(fields.password)) errors.password = 'Must contain a number';
  else if (!/[!@#$%^&*]/.test(fields.password)) errors.password = 'Must contain a special character (!@#$%^&*)';
  if (fields.confirmPassword !== fields.password) errors.confirmPassword = 'Passwords do not match';
  const age = parseInt(fields.age);
  if (!fields.age || isNaN(age) || age < 18 || age > 100) errors.age = 'Age must be 18–100';
  if (!fields.gender) errors.gender = 'Please select gender';
  return errors;
}

const INIT = { name: '', email: '', password: '', confirmPassword: '', age: '', gender: '' };

export default function Q1() {
  const [fields, setFields] = useState(INIT);
  const [touched, setTouched] = useState({});
  const [submitted, setSubmitted] = useState(null);

  const errors = validate(fields);
  const isValid = Object.keys(errors).length === 0;

  const handleChange = e => setFields(f => ({ ...f, [e.target.name]: e.target.value }));
  const handleBlur = e => setTouched(t => ({ ...t, [e.target.name]: true }));

  const handleSubmit = e => {
    e.preventDefault();
    setTouched({ name:true, email:true, password:true, confirmPassword:true, age:true, gender:true });
    if (isValid) { setSubmitted(fields); setFields(INIT); }
  };

  return (
    <div className="page">
      <div className="card">
        <h2>Q1 — Multi-Field Registration Form</h2>
        {submitted && (
          <div className="success-banner">
            <strong>Registered!</strong>
            <pre style={{marginTop:8,fontSize:12}}>{JSON.stringify(submitted, null, 2)}</pre>
            <button className="btn btn-secondary" style={{marginTop:8}} onClick={() => setSubmitted(null)}>Close</button>
          </div>
        )}
        <form onSubmit={handleSubmit} noValidate>
          {[
            { name: 'name', label: 'Full Name', type: 'text' },
            { name: 'email', label: 'Email', type: 'email' },
            { name: 'password', label: 'Password', type: 'password' },
            { name: 'confirmPassword', label: 'Confirm Password', type: 'password' },
            { name: 'age', label: 'Age', type: 'number' },
          ].map(f => (
            <div className="form-group" key={f.name}>
              <label>{f.label}</label>
              <input name={f.name} type={f.type} value={fields[f.name]}
                onChange={handleChange} onBlur={handleBlur} />
              {touched[f.name] && errors[f.name] && <div className="error">{errors[f.name]}</div>}
            </div>
          ))}
          <div className="form-group">
            <label>Gender</label>
            <select name="gender" value={fields.gender} onChange={handleChange} onBlur={handleBlur}>
              <option value="">Select...</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
            {touched.gender && errors.gender && <div className="error">{errors.gender}</div>}
          </div>
          <button className="btn btn-primary" type="submit" disabled={!isValid}>Register</button>
        </form>
      </div>
    </div>
  );
}
