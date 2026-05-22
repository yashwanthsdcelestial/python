// Q11. Object Deep Merge
// Topics: Objects, Recursion, Spread Operator, Type Checking

function deepMerge(target, source) {
  // Start with a shallow copy of target to avoid mutation
  const result = { ...target };

  for (const key of Object.keys(source)) {
    const srcVal = source[key];
    const tgtVal = result[key];

    if (Array.isArray(srcVal) && Array.isArray(tgtVal)) {
      // Arrays: concatenate
      result[key] = [...tgtVal, ...srcVal];
    } else if (
      srcVal !== null &&
      typeof srcVal === "object" &&
      tgtVal !== null &&
      typeof tgtVal === "object" &&
      !Array.isArray(srcVal)
    ) {
      // Both are plain objects: recurse
      result[key] = deepMerge(tgtVal, srcVal);
    } else {
      // Primitive or null: source overrides target
      result[key] = srcVal;
    }
  }

  return result;
}

// --- Tests ---
const defaults = {
  server: { port: 3000, host: "localhost" },
  database: { url: "localhost:5432", pool: { min: 2, max: 5 } },
  features: ["auth"],
};

const overrides = {
  server: { port: 8080 },
  database: { pool: { max: 20 } },
  features: ["logging"],
  debug: true,
};

console.log(deepMerge(defaults, overrides));
// {
//   server: { port: 8080, host: "localhost" },
//   database: { url: "localhost:5432", pool: { min: 2, max: 20 } },
//   features: ["auth", "logging"],
//   debug: true
// }

// Originals are NOT mutated
console.log(defaults.server.port); // 3000
console.log(defaults.features);    // ["auth"]
