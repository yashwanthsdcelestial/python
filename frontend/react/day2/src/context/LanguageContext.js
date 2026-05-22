import React, { createContext, useContext, useState } from 'react';
export const LanguageContext = createContext();
export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(() => localStorage.getItem('lang') || 'en');
  const toggleLang = () => setLang(l => { const n = l==='en'?'hi':'en'; localStorage.setItem('lang',n); return n; });
  return <LanguageContext.Provider value={{ lang, toggleLang }}>{children}</LanguageContext.Provider>;
}
export const useLang = () => useContext(LanguageContext);
