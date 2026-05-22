// Q2. Truthy/Falsy Filter & Null Replacer
// Topics: Truthy/Falsy, filter(), Nullish Values

const cleanData = (arr) => arr.filter(Boolean);

const replaceNulls = (arr, replacement) =>
  arr.map((item) => (item == null ? replacement : item));


const data = [0, "hello", null, 42, "", undefined, false, "world", NaN];

console.log(cleanData(data));

console.log(replaceNulls(data, "N/A"));

console.log(data);
