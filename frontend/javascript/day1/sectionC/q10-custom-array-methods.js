// Q10. Custom Array Method Implementations
// Topics: Prototypes, Callbacks, this

// myMap — callback receives (element, index, array)
Array.prototype.myMap = function (callback) {
  const result = [];
  for (let i = 0; i < this.length; i++) {
    result.push(callback(this[i], i, this));
  }
  return result;
};

// myFilter — callback receives (element, index, array)
Array.prototype.myFilter = function (callback) {
  const result = [];
  for (let i = 0; i < this.length; i++) {
    if (callback(this[i], i, this)) {
      result.push(this[i]);
    }
  }
  return result;
};

// myReduce — callback receives (accumulator, element, index, array)
Array.prototype.myReduce = function (callback, initialValue) {
  let acc = initialValue;
  let startIndex = 0;

  // If no initialValue, use first element as accumulator
  if (arguments.length < 2) {
    if (this.length === 0) throw new TypeError("Reduce of empty array with no initial value");
    acc = this[0];
    startIndex = 1;
  }

  for (let i = startIndex; i < this.length; i++) {
    acc = callback(acc, this[i], i, this);
  }
  return acc;
};

// --- Tests ---
const nums = [1, 2, 3, 4, 5];

console.log(nums.myMap((n) => n * 2));          // [2, 4, 6, 8, 10]
console.log(nums.myFilter((n) => n % 2 === 0)); // [2, 4]
console.log(nums.myReduce((acc, n) => acc + n, 0)); // 15

// Extra: myReduce without initial value
console.log(nums.myReduce((acc, n) => acc + n)); // 15
