// Q9. Utility Functions with Array Methods
// Topics: reduce, Set, flat, Callbacks

// Groups an array of objects by a given key property
function groupBy(arr, key) {
  return arr.reduce((acc, item) => {
    const groupKey = item[key];
    acc[groupKey] = acc[groupKey] ? [...acc[groupKey], item] : [item];
    return acc;
  }, {});
}

// Returns unique values preserving order — uses filter with indexOf (NOT Set)
function unique(arr) {
  return arr.filter((item, index) => arr.indexOf(item) === index);
}

// Splits array into chunks of given size
function chunk(arr, size) {
  return arr.reduce((acc, item, index) => {
    const chunkIndex = Math.floor(index / size);
    if (!acc[chunkIndex]) acc[chunkIndex] = [];
    acc[chunkIndex] = [...acc[chunkIndex], item];
    return acc;
  }, []);
}

// Combines two arrays into an array of [a, b] pairs
function zip(arr1, arr2) {
  return arr1.map((item, index) => [item, arr2[index]]);
}

// --- Tests ---
const people = [
  { name: "Alice", dept: "Engineering" },
  { name: "Bob", dept: "Marketing" },
  { name: "Carol", dept: "Engineering" },
  { name: "Dave", dept: "Marketing" },
  { name: "Eve", dept: "HR" },
];

console.log(groupBy(people, "dept"));
// { Engineering: [{Alice},{Carol}], Marketing: [{Bob},{Dave}], HR: [{Eve}] }

console.log(unique([1, 2, 2, 3, 4, 4, 5]));
// [1, 2, 3, 4, 5]

console.log(chunk([1, 2, 3, 4, 5, 6, 7], 3));
// [[1, 2, 3], [4, 5, 6], [7]]

console.log(zip(["a", "b", "c"], [1, 2, 3]));
// [["a", 1], ["b", 2], ["c", 3]]
