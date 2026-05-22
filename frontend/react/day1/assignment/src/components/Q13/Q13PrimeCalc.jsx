import React, { useState, useMemo } from "react";

function countPrimes(n) {
  if (n < 2) return 0;
  const sieve = new Array(n + 1).fill(true);
  sieve[0] = sieve[1] = false;
  for (let i = 2; i * i <= n; i++) {
    if (sieve[i]) {
      for (let j = i * i; j <= n; j += i) sieve[j] = false;
    }
  }
  return sieve.filter(Boolean).length;
}

function Q13PrimeCalc() {
  const [n, setN] = useState(100);
  const [theme, setTheme] = useState("light");

  const primeCount = useMemo(() => {
    console.log("useMemo: computing primes for N =", n);
    return countPrimes(Number(n));
  }, [n]);

  const bg = theme === "dark" ? "#1a1a2e" : "#f0f4ff";
  const color = theme === "dark" ? "#e2e8f0" : "#1a1a2e";

  return (
    <div>
      <h2>Q13 — Prime Number Calculator with useMemo</h2>
      <div style={{ background: bg, color, padding: "20px", borderRadius: "12px", transition: "all 0.3s", display: "inline-block", minWidth: "320px" }}>
        <div style={{ display: "flex", gap: "12px", alignItems: "center", marginBottom: "12px" }}>
          <label><strong>N:</strong></label>
          <input
            type="number"
            value={n}
            min={0}
            max={100000}
            onChange={e => setN(e.target.value)}
            style={{ padding: "6px 10px", borderRadius: "6px", border: "1.5px solid #cbd5e1", width: "120px" }}
          />
        </div>
        <p style={{ fontSize: "1.1rem" }}>
          Primes from 1 to <strong>{n}</strong>: <span style={{ color: "#4f8ef7", fontWeight: 700, fontSize: "1.4rem" }}>{primeCount}</span>
        </p>
        <p style={{ fontSize: "0.8rem", color: "#94a3b8" }}>Toggle theme won't re-run computation (check console).</p>
        <button
          onClick={() => setTheme(t => t === "light" ? "dark" : "light")}
          style={{ background: "#4f8ef7", color: "#fff", border: "none", borderRadius: "6px", padding: "8px 16px", cursor: "pointer" }}
        >
          Toggle Theme
        </button>
      </div>
    </div>
  );
}

export default Q13PrimeCalc;
