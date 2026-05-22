// Q7. Closure — Memoize Function
// Topics: Closures, Caching, Higher-Order Functions

function memoize(fn) {
  // The cache is private state captured by the closure
  const cache = {};

  return function (arg) {
    const key = String(arg);

    if (key in cache) {
      console.log(`Cache hit: ${arg}`);
      return cache[key];
    }

    console.log(`Computing: ${arg}`);
    const result = fn(arg);
    cache[key] = result;
    return result;
  };
}

// --- Tests ---
const slowSquare = (n) => {
  for (let i = 0; i < 1e8; i++) {} // simulate slow computation
  return n * n;
};

const fastSquare = memoize(slowSquare);

console.log(fastSquare(5));  // Computing: 5  → 25
console.log(fastSquare(5));  // Cache hit: 5  → 25
console.log(fastSquare(10)); // Computing: 10 → 100
