import React, { createContext, useContext, useState, useEffect } from 'react';

export const ThemeContext = createContext();
export const LanguageContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'light');
  const toggleTheme = () => setTheme(t => {
    const next = t === 'light' ? 'dark' : 'light';
    localStorage.setItem('theme', next);
    return next;
  });
  return <ThemeContext.Provider value={{ theme, toggleTheme }}>{children}</ThemeContext.Provider>;
}

export function LanguageProvider({ children }) {
  const [lang, setLang] = useState(() => localStorage.getItem('lang') || 'en');
  const toggleLang = () => setLang(l => {
    const next = l === 'en' ? 'hi' : 'en';
    localStorage.setItem('lang', next);
    return next;
  });
  return <LanguageContext.Provider value={{ lang, toggleLang }}>{children}</LanguageContext.Provider>;
}

export const useTheme = () => useContext(ThemeContext);
export const useLang = () => useContext(LanguageContext);

// Cart Context (useReducer based)
export const CartContext = createContext();

function cartReducer(state, action) {
  switch (action.type) {
    case 'ADD':
      const exists = state.items.find(i => i.id === action.payload.id);
      if (exists) return { ...state, items: state.items.map(i => i.id === action.payload.id ? { ...i, qty: i.qty + 1 } : i) };
      return { ...state, items: [...state.items, { ...action.payload, qty: 1 }] };
    case 'REMOVE': return { ...state, items: state.items.filter(i => i.id !== action.payload) };
    case 'INC': return { ...state, items: state.items.map(i => i.id === action.payload ? { ...i, qty: i.qty + 1 } : i) };
    case 'DEC': return { ...state, items: state.items.map(i => i.id === action.payload && i.qty > 1 ? { ...i, qty: i.qty - 1 } : i) };
    case 'CLEAR': return { ...state, items: [] };
    default: return state;
  }
}

import { useReducer } from 'react';
export function CartProvider({ children }) {
  const [state, dispatch] = useReducer(cartReducer, { items: [] });
  const total = state.items.reduce((s, i) => s + i.price * i.qty, 0);
  return <CartContext.Provider value={{ ...state, dispatch, total }}>{children}</CartContext.Provider>;
}
export const useCart = () => useContext(CartContext);

// Auth Context (legacy, see Q12)
export const AuthContext = createContext();
import { useState as useStateAuth } from 'react';
export function AuthProvider({ children }) {
  const [authState, setAuthState] = useState(() => {
    const token = localStorage.getItem('fakeJWT');
    return { isAuthenticated: !!token, token, user: token ? 'user' : null };
  });
  const login = (user) => {
    const token = 'fake.jwt.token.' + btoa(user);
    localStorage.setItem('fakeJWT', token);
    setAuthState({ isAuthenticated: true, token, user });
  };
  const logout = () => {
    localStorage.removeItem('fakeJWT');
    setAuthState({ isAuthenticated: false, token: null, user: null });
  };
  return <AuthContext.Provider value={{ ...authState, login, logout }}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
