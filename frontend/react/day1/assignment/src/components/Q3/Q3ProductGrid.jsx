import React from "react";

function ProductCard({ image, name, price, description, onAddToCart }) {
  return (
    <div style={{
      background: "#fff", borderRadius: "12px", boxShadow: "0 2px 12px rgba(0,0,0,0.09)",
      padding: "16px", width: "180px", display: "flex", flexDirection: "column", gap: "8px"
    }}>
      <img src={image} alt={name} style={{ width: "100%", height: "120px", objectFit: "cover", borderRadius: "8px" }} />
      <h3 style={{ margin: 0, fontSize: "1rem", color: "#1a1a2e" }}>{name}</h3>
      <p style={{ margin: 0, color: "#4f8ef7", fontWeight: 700 }}>₹{price}</p>
      <p style={{ margin: 0, fontSize: "0.78rem", color: "#666" }}>{description}</p>
      <button
        onClick={onAddToCart}
        style={{
          marginTop: "auto", background: "#4f8ef7", color: "#fff", border: "none",
          borderRadius: "6px", padding: "8px", cursor: "pointer", fontWeight: 600
        }}
      >
        Add to Cart
      </button>
    </div>
  );
}

const products = [
  { id: 1, name: "Wireless Headphones", price: 1999, description: "Crystal clear audio.", image: "https://picsum.photos/seed/prod1/200/150" },
  { id: 2, name: "Mechanical Keyboard", price: 2999, description: "Tactile and fast.", image: "https://picsum.photos/seed/prod2/200/150" },
  { id: 3, name: "USB-C Hub", price: 899, description: "7-in-1 connectivity.", image: "https://picsum.photos/seed/prod3/200/150" },
  { id: 4, name: "Webcam HD", price: 1499, description: "1080p video calls.", image: "https://picsum.photos/seed/prod4/200/150" },
  { id: 5, name: "Mouse Pad XL", price: 499, description: "Smooth surface.", image: "https://picsum.photos/seed/prod5/200/150" },
  { id: 6, name: "LED Desk Lamp", price: 799, description: "Eye-care lighting.", image: "https://picsum.photos/seed/prod6/200/150" },
];

function Q3ProductGrid() {
  return (
    <div>
      <h2>Q3 — Product Card Grid</h2>
      <div style={{ display: "flex", gap: "20px", flexWrap: "wrap" }}>
        {products.map((p) => (
          <ProductCard
            key={p.id}
            {...p}
            onAddToCart={() => console.log(`Added to cart: ${p.name}`)}
          />
        ))}
      </div>
    </div>
  );
}

export default Q3ProductGrid;
