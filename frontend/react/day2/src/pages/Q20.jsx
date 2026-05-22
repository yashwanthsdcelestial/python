import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { fetchProducts } from '../store/slices/productsSlice';
import { addToCart, removeFromCart, incrementQty, decrementQty, clearCart } from '../store/slices/cartSlice';

function ReduxHeader() {
  const count = useSelector(s => s.cart.items.reduce((a, i) => a + i.qty, 0));
  return (
    <div style={{ background: '#1a1a2e', color: '#fff', padding: '12px 20px', borderRadius: 8, marginBottom: 20, display: 'flex', justifyContent: 'space-between' }}>
      <strong>🛍️ Redux Shop</strong>
      <span>Cart Items <span className="badge">{count}</span></span>
    </div>
  );
}

function ProductGrid() {
  const dispatch = useDispatch();
  const { items, loading } = useSelector(s => s.products);
  const cartIds = useSelector(s => new Set(s.cart.items.map(i => i.id)));

  if (loading) return <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}><div className="spinner" /><span style={{ fontSize: 14 }}>Loading products...</span></div>;

  return (
    <div>
      <h3 style={{ marginBottom: 12 }}>Products</h3>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(150px,1fr))', gap: 12 }}>
        {items.map(p => (
          <div key={p.id} style={{ background: '#f8f9fa', borderRadius: 8, padding: 14, textAlign: 'center' }}>
            <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 6 }}>{p.title}</div>
            <div style={{ color: '#4361ee', fontWeight: 700, marginBottom: 10 }}>₹{p.price}</div>
            <button
              className={`btn ${cartIds.has(p.id) ? 'btn-success' : 'btn-primary'}`}
              style={{ fontSize: 12, padding: '5px 12px', width: '100%' }}
              onClick={() => dispatch(addToCart(p))}>
              {cartIds.has(p.id) ? '✓ Added' : 'Add to Cart'}
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function CartSection() {
  const dispatch = useDispatch();
  const items = useSelector(s => s.cart.items);
  const total = useSelector(s => s.cart.items.reduce((a, i) => a + i.price * i.qty, 0));

  if (items.length === 0) return <div style={{ marginTop: 20, color: '#888', padding: 12 }}>🛒 Cart is empty</div>;

  return (
    <div style={{ marginTop: 24 }}>
      <h3 style={{ marginBottom: 12 }}>Cart</h3>
      {items.map(item => (
        <div key={item.id} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '8px 0', borderBottom: '1px solid #eee' }}>
          <span style={{ flex: 1, fontSize: 13 }}>{item.title}</span>
          <button className="btn btn-secondary" style={{ padding: '2px 8px' }} onClick={() => dispatch(decrementQty(item.id))}>−</button>
          <span style={{ minWidth: 20, textAlign: 'center', fontSize: 14 }}>{item.qty}</span>
          <button className="btn btn-secondary" style={{ padding: '2px 8px' }} onClick={() => dispatch(incrementQty(item.id))}>+</button>
          <span style={{ minWidth: 70, textAlign: 'right', fontWeight: 600, fontSize: 13 }}>₹{item.price * item.qty}</span>
          <button className="btn btn-danger" style={{ padding: '2px 8px', fontSize: 12 }} onClick={() => dispatch(removeFromCart(item.id))}>✕</button>
        </div>
      ))}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 14 }}>
        <div style={{ fontWeight: 700, fontSize: 16 }}>Total: <span style={{ color: '#4361ee' }}>₹{total}</span></div>
        <button className="btn btn-danger" style={{ fontSize: 12 }} onClick={() => dispatch(clearCart())}>Clear Cart</button>
      </div>
    </div>
  );
}

export default function Q20() {
  const dispatch = useDispatch();
  useEffect(() => { dispatch(fetchProducts()); }, [dispatch]);

  return (
    <div className="page">
      <div className="card">
        <h2>Q20 — Multi-Slice Shopping Cart (Redux Toolkit)</h2>
        <ReduxHeader />
        <ProductGrid />
        <CartSection />
      </div>
    </div>
  );
}
