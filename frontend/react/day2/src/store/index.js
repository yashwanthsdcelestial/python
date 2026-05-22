import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './slices/counterSlice';
import todoReducer from './slices/todoSlice';
import authReducer from './slices/authSlice';
import usersReducer from './slices/usersSlice';
import productsReducer from './slices/productsSlice';
import cartReducer from './slices/cartSlice';

const preloadedAuth = (() => {
  try {
    const stored = localStorage.getItem('reduxAuth');
    return stored ? { auth: JSON.parse(stored) } : {};
  } catch { return {}; }
})();

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    todos: todoReducer,
    auth: authReducer,
    users: usersReducer,
    products: productsReducer,
    cart: cartReducer,
  },
  preloadedState: preloadedAuth,
});

store.subscribe(() => {
  const { auth } = store.getState();
  localStorage.setItem('reduxAuth', JSON.stringify(auth));
});
