// Q1. Type Checker Utility
// Topics: Data Types, typeof, Strict Equality
var a
function describeType(value) {
  if (value === null) return "null";
  if (Number.isNaN(value)) return "NaN";
  if (Array.isArray(value)) return "array";
   return typeof value;
}



console.log(describeType(42));          // "number"
console.log(describeType("hello"));     // "string"
console.log(describeType(null));        // "null"
console.log(describeType([1, 2]));      // "array"
console.log(describeType(NaN));         // "NaN"
console.log(describeType({ a: 1 }));    // "object"
console.log(describeType(undefined));   // "undefined"
console.log(describeType(() => {}));    // "function"

