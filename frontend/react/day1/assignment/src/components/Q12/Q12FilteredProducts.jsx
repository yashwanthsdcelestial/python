import React, { useState, useMemo } from "react";

// Generate 1000 products
const ALL_PRODUCTS = Array.from({ length: 1000 }, (_, i) => ({
  id: i + 1,
  name: `Product ${i + 1}`,
  price: Math.floor(Math.random() * 5000) + 100,
  category: ["Electronics", "Clothing", "Books", "Sports", "Home"][i % 5],
}));

const CATEGORIES = ["All", "Electronics", "Clothing", "Books", "Sports", "Home"];

function Q12FilteredProducts() {
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [counter, setCounter] = useState(0); // unrelated state to test memoization

  const filtered = useMemo(() => {
    console.log("useMemo: re-running filter...");
    return ALL_PRODUCTS.filter(p => {
      const matchSearch = p.name.toLowerCase().includes(search.toLowerCase());
      const matchCat = category === "All" || p.category === category;
      return matchSearch && matchCat;
    });
  }, [search, category]);

  return (
    <div>
      <h2>Q12 — Expensive Filter with useMemo</h2>
      <p style={{ color: "#64748b", fontSize: "0.85rem" }}>
        Unrelated counter (incrementing won't re-run the filter): <strong>{counter}</strong>
        <button onClick={() => setCounter(c => c + 1)} style={{ marginLeft: "10px", padding: "4px 12px" }}>+</button>
      </p>
      <div style={{ display: "flex", gap: "12px", marginBottom: "12px" }}>
        <input
          placeholder="Search products..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          style={{ padding: "8px 12px", borderRadius: "6px", border: "1.5px solid #cbd5e1", width: "200px" }}
        />
        <select
          value={category}
          onChange={e => setCategory(e.target.value)}
          style={{ padding: "8px 12px", borderRadius: "6px", border: "1.5px solid #cbd5e1" }}
        >
          {CATEGORIES.map(c => <option key={c}>{c}</option>)}
        </select>
      </div>
      <p style={{ color: "#4f8ef7", fontWeight: 600 }}>{filtered.length} products found</p>
      <div style={{ maxHeight: "200px", overflowY: "auto", border: "1px solid #e2e8f0", borderRadius: "8px" }}>
        {filtered.slice(0, 50).map(p => (
          <div key={p.id} style={{ padding: "6px 12px", borderBottom: "1px solid #f1f5f9", fontSize: "0.88rem" }}>
            <strong>{p.name}</strong> — {p.category} — ₹{p.price}
          </div>
        ))}
        {filtered.length > 50 && <div style={{ padding: "6px 12px", color: "#94a3b8" }}>...and {filtered.length - 50} more</div>}
      </div>
    </div>
  );
}

export default Q12FilteredProducts;
