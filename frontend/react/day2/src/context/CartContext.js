import React, { createContext, useContext, useReducer } from 'react';
export const CartContext = createContext();
function cartReducer(state, action) {
  switch(action.type) {
    case 'ADD': {
      const ex = state.items.find(i=>i.id===action.payload.id);
      if(ex) return {...state, items: state.items.map(i=>i.id===action.payload.id?{...i,qty:i.qty+1}:i)};
      return {...state, items: [...state.items,{...action.payload,qty:1}]};
    }
    case 'REMOVE': return {...state, items: state.items.filter(i=>i.id!==action.payload)};
    case 'INC': return {...state, items: state.items.map(i=>i.id===action.payload?{...i,qty:i.qty+1}:i)};
    case 'DEC': return {...state, items: state.items.map(i=>i.id===action.payload&&i.qty>1?{...i,qty:i.qty-1}:i)};
    case 'CLEAR': return {...state, items:[]};
    default: return state;
  }
}
export function CartProvider({children}) {
  const [state, dispatch] = useReducer(cartReducer, {items:[]});
  const total = state.items.reduce((s,i)=>s+i.price*i.qty,0);
  return <CartContext.Provider value={{...state,dispatch,total}}>{children}</CartContext.Provider>;
}
export const useCart = () => useContext(CartContext);
