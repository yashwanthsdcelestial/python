import React from 'react';
import { CartProvider, useCart } from '../context/CartContext';

const PRODUCTS = [
  { id: 1, name: 'Wireless Mouse', price: 799 },
  { id: 2, name: 'USB Hub', price: 1299 },
  { id: 3, name: 'Desk Lamp', price: 549 },
  { id: 4, name: 'Notebook Set', price: 349 },
  { id: 5, name: 'Phone Stand', price: 249 },
];

function Header() {
  const { items } = useCart();
  const count = items.reduce((s, i) => s + i.qty, 0);
  return (
    <div style={{ background: '#1a1a2e', color: '#fff', padding: '12px 20px', borderRadius: 8, marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
      <strong>ShopReact</strong>
      <span>Cart <span className="badge">{count}</span></span>
    </div>
  );
}

function ProductList() {
  const { dispatch } = useCart();
  return (
    <div>
      <h3 style={{ marginBottom: 12 }}>Products</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(160px,1fr))', gap: 12 }}>
        {PRODUCTS.map(p => (
          <div key={p.id} style={{ background: '#f8f9fa', borderRadius: 8, padding: 14, textAlign: 'center' }}>
            <div style={{ fontSize: 13, fontWeight: 600 }}>{p.name}</div>
            <div style={{ color: '#4361ee', fontWeight: 700, margin: '6px 0' }}>₹{p.price}</div>
            <button className="btn btn-primary" style={{ fontSize: 12, padding: '5px 12px' }}
              onClick={() => dispatch({ type: 'ADD', payload: p })}>Add to Cart</button>
          </div>
        ))}
      </div>
    </div>
  );
}

function Cart() {
  const { items, dispatch, total } = useCart();
  if (items.length === 0) return <div style={{ marginTop: 20, color: '#888' }}>Your cart is empty</div>;
  return (
    <div style={{ marginTop: 20 }}>
      <h3 style={{ marginBottom: 12 }}>Cart</h3>
      {items.map(item => (
        <div key={item.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid #eee' }}>
          <span style={{ fontSize: 14 }}>{item.name}</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <button className="btn btn-secondary" style={{ padding: '2px 8px' }} onClick={() => dispatch({ type: 'DEC', payload: item.id })}>−</button>
            <span style={{ minWidth: 20, textAlign: 'center' }}>{item.qty}</span>
            <button className="btn btn-secondary" style={{ padding: '2px 8px' }} onClick={() => dispatch({ type: 'INC', payload: item.id })}>+</button>
            <span style={{ minWidth: 70, textAlign: 'right', fontWeight: 600 }}>₹{item.price * item.qty}</span>
            <button className="btn btn-danger" style={{ padding: '2px 8px', fontSize: 12 }} onClick={() => dispatch({ type: 'REMOVE', payload: item.id })}>✕</button>
          </div>
        </div>
      ))}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 12, fontWeight: 700, fontSize: 16 }}>
        <span>Total:</span><span style={{ color: '#4361ee' }}>₹{total}</span>
      </div>
      <button className="btn btn-danger" style={{ marginTop: 12 }} onClick={() => dispatch({ type: 'CLEAR' })}>Clear Cart</button>
    </div>
  );
}

export default function Q5() {
  return (
    <CartProvider>
      <div className="page">
        <div className="card">
          <h2>Q5 — Shopping Cart (useReducer + Context)</h2>
          <Header />
          <ProductList />
          <Cart />
        </div>
      </div>
    </CartProvider>
  );
}
