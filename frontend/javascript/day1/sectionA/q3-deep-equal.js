// Q3. Deep Equality Checker
// Topics: Type Checking, Recursion, Object Comparison

function deepEqual(a, b) {

  if (a === null && b === null) return true;
  if (a === null || b === null) return false;

  // Primitives: use strict equality
  if (typeof a !== "object" && typeof b !== "object") return a === b;

  // Type mismatch (e.g., object vs array)
  if (typeof a !== typeof b) return false;
  if (Array.isArray(a) !== Array.isArray(b)) return false;

  // Both are arrays or objects — check keys/length
  const keysA = Object.keys(a);
  const keysB = Object.keys(b);

  if (keysA.length !== keysB.length) return false;

  // Recursively compare each property
  for (const key of keysA) {
    if (!keysB.includes(key)) return false;
    if (!deepEqual(a[key], b[key])) return false;
  }

  return true;
}

// --- Tests ---
console.log(deepEqual({ a: 1, b: { c: 2 } }, { a: 1, b: { c: 2 } })); // true
console.log(deepEqual([1, [2, 3]], [1, [2, 3]]));                       // true
console.log(deepEqual({ a: 1 }, { a: "1" }));                           // false
console.log(deepEqual(null, null));                                      // true
console.log(deepEqual(null, {}));                                        // false
