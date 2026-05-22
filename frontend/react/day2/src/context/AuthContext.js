import React, { createContext, useContext, useState } from 'react';
export const AuthContext = createContext();
export function AuthProvider({children}) {
  const [auth, setAuth] = useState(() => {
    const t = localStorage.getItem('fakeJWT');
    return { isAuthenticated: !!t, token: t, user: t?'user':null };
  });
  const login = (user) => {
    const token = 'fake.jwt.' + btoa(user);
    localStorage.setItem('fakeJWT', token);
    setAuth({ isAuthenticated: true, token, user });
  };
  const logout = () => {
    localStorage.removeItem('fakeJWT');
    setAuth({ isAuthenticated: false, token: null, user: null });
  };
  return <AuthContext.Provider value={{...auth, login, logout}}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
