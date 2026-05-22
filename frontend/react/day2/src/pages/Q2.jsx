import React, { useState } from 'react';

function getWaterState(c) {
  if (c <= 0) return 'freeze';
  if (c >= 100) return 'boil';
  return 'be liquid';
}

function CelsiusInput({ celsius, onChange }) {
  return (
    <div className="form-group">
      <label>Celsius (°C)</label>
      <input type="number" value={celsius} onChange={e => onChange(e.target.value)} />
    </div>
  );
}

function FahrenheitInput({ fahrenheit, onChange }) {
  return (
    <div className="form-group">
      <label>Fahrenheit (°F)</label>
      <input type="number" value={fahrenheit} onChange={e => onChange(e.target.value)} />
    </div>
  );
}

export default function Q2() {
  const [celsius, setCelsius] = useState('');
  const [fahrenheit, setFahrenheit] = useState('');

  const handleCelsius = val => {
    setCelsius(val);
    setFahrenheit(val === '' ? '' : ((parseFloat(val) * 9) / 5 + 32).toFixed(2));
  };
  const handleFahrenheit = val => {
    setFahrenheit(val);
    setCelsius(val === '' ? '' : (((parseFloat(val) - 32) * 5) / 9).toFixed(2));
  };

  return (
    <div className="page">
      <div className="card">
        <h2>Q2 — Temperature Converter</h2>
        <div style={{ display: 'flex', gap: 24 }}>
          <div style={{ flex: 1 }}><CelsiusInput celsius={celsius} onChange={handleCelsius} /></div>
          <div style={{ flex: 1 }}><FahrenheitInput fahrenheit={fahrenheit} onChange={handleFahrenheit} /></div>
        </div>
        {celsius !== '' && !isNaN(parseFloat(celsius)) && (
          <div className="success-banner" style={{ marginTop: 16 }}>
            At {celsius}°C, water would <strong>{getWaterState(parseFloat(celsius))}</strong>
          </div>
        )}
      </div>
    </div>
  );
}
