import React from 'react';
import { ThemeProvider, useTheme } from '../context/ThemeContext';
import { LanguageProvider, useLang } from '../context/LanguageContext';

const TRANSLATIONS = {
  en: { welcome: 'Welcome to our Application!', greeting: 'Hello, User!', desc: 'This component is 3 levels deep and consumes both Theme and Language contexts.' },
  hi: { welcome: 'हमारे एप्लिकेशन में आपका स्वागत है!', greeting: 'नमस्ते, उपयोगकर्ता!', desc: 'यह कॉम्पोनेन्ट 3 स्तर गहरा है और दोनों Context का उपयोग करता है।' },
};

function Level3() {
  const { theme } = useTheme();
  const { lang } = useLang();
  const t = TRANSLATIONS[lang];
  return (
    <div style={{
      padding: 20, borderRadius: 10, marginTop: 8,
      background: theme === 'dark' ? '#1a1a2e' : '#e0e7ff',
      color: theme === 'dark' ? '#eee' : '#1a1a2e',
      border: `2px solid ${theme === 'dark' ? '#4361ee' : '#c0c9ff'}`
    }}>
      <div className="tag">Level 3 Component</div>
      <h3 style={{ marginTop: 10 }}>{t.greeting}</h3>
      <p style={{ marginTop: 6, fontSize: 14 }}>{t.welcome}</p>
      <p style={{ marginTop: 4, fontSize: 12, opacity: 0.8 }}>{t.desc}</p>
      <p style={{ marginTop: 8, fontSize: 12 }}>
        Theme: <strong>{theme}</strong> | Lang: <strong>{lang}</strong>
      </p>
    </div>
  );
}
function Level2() { return <div style={{ padding: '8px 0' }}><span className="tag">Level 2</span><Level3 /></div>; }
function Level1() { return <div style={{ padding: '8px 0' }}><span className="tag">Level 1</span><Level2 /></div>; }

function SettingsPanel() {
  const { theme, toggleTheme } = useTheme();
  const { lang, toggleLang } = useLang();
  return (
    <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 20 }}>
      <button className="btn btn-primary" onClick={toggleTheme}>
        {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
      </button>
      <button className="btn btn-secondary" onClick={toggleLang}>
        {lang === 'en' ? '🇮🇳 हिंदी' : '🇬🇧 English'}
      </button>
    </div>
  );
}

export default function Q4() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <div className="page">
          <div className="card">
            <h2>Q4 — Theme + Language Switcher</h2>
            <SettingsPanel />
            <Level1 />
          </div>
        </div>
      </LanguageProvider>
    </ThemeProvider>
  );
}
