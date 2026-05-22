// Q8. Array Pipeline — Student Grade Processor
// Topics: map, filter, reduce, sort, Method Chaining

const students = [
  { name: "Alice", scores: [85, 92, 78] },
  { name: "Bob", scores: [45, 55, 60] },
  { name: "Carol", scores: [90, 95, 88] },
  { name: "Dave", scores: [30, 40, 35] },
  { name: "Eve", scores: [72, 68, 75] },
];

const result = students
  // Step 1: Compute average rounded to 2 decimal places
  .map((s) => ({
    name: s.name,
    average: Math.round((s.scores.reduce((a, b) => a + b, 0) / s.scores.length) * 100) / 100,
  }))
  // Step 2: Keep only students with average >= 60
  .filter((s) => s.average >= 60)
  // Step 3: Sort by average descending
  .sort((a, b) => b.average - a.average)
  // Step 4: Assign letter grade
  .map((s) => ({
    ...s,
    grade:
      s.average >= 90 ? "A" :
      s.average >= 80 ? "B" :
      s.average >= 70 ? "C" : "D",
  }));

console.log(result);
// [
//   { name: "Carol", average: 91,    grade: "A" },
//   { name: "Alice", average: 85,    grade: "B" },
//   { name: "Eve",   average: 71.67, grade: "C" }
// ]
