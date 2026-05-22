// Q13. Object Transformer Utilities
// Topics: Object.keys, Object.entries, reduce, Computed Property Names

// Returns a new object with only the specified keys
const pick = (obj, keys) =>
  keys.reduce((acc, key) => {
    if (key in obj) acc[key] = obj[key];
    return acc;
  }, {});

// Returns a new object without the specified keys
const omit = (obj, keys) =>
  Object.entries(obj).reduce((acc, [k, v]) => {
    if (!keys.includes(k)) acc[k] = v;
    return acc;
  }, {});

// Transforms all keys using a function
const mapKeys = (obj, fn) =>
  Object.entries(obj).reduce((acc, [k, v]) => {
    acc[fn(k)] = v;
    return acc;
  }, {});

// Transforms all values using a function
const mapValues = (obj, fn) =>
  Object.entries(obj).reduce((acc, [k, v]) => {
    acc[k] = fn(v);
    return acc;
  }, {});

// --- Tests ---
const user = { firstName: "Alice", lastName: "Smith", age: 25, password: "secret" };

console.log(pick(user, ["firstName", "lastName"]));
// { firstName: "Alice", lastName: "Smith" }

console.log(omit(user, ["password"]));
// { firstName: "Alice", lastName: "Smith", age: 25 }

console.log(mapKeys(user, (key) => key.toUpperCase()));
// { FIRSTNAME: "Alice", LASTNAME: "Smith", AGE: 25, PASSWORD: "secret" }

console.log(mapValues({ a: 1, b: 2, c: 3 }, (val) => val * 10));
// { a: 10, b: 20, c: 30 }

// Original is NOT mutated
console.log(user);
