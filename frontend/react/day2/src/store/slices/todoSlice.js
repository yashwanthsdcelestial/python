import { createSlice } from '@reduxjs/toolkit';

const todoSlice = createSlice({
  name: 'todos',
  initialState: { items: [] },
  reducers: {
    addTodo: (state, action) => {
      state.items.push({ id: Date.now(), text: action.payload, completed: false });
    },
    removeTodo: (state, action) => {
      state.items = state.items.filter(t => t.id !== action.payload);
    },
    toggleTodo: (state, action) => {
      const t = state.items.find(t => t.id === action.payload);
      if (t) t.completed = !t.completed;
    },
    clearAll: (state) => { state.items = []; },
  },
});

export const { addTodo, removeTodo, toggleTodo, clearAll } = todoSlice.actions;
export default todoSlice.reducer;
