// Q5. Scope & Hoisting Bug Fix
// Topics: var vs let, Block Scope, Closures in Loops, setTimeout

// ── BUGGY CODE ──
// for (var i = 0; i < 5; i++) {
//   setTimeout(function () {
//     console.log(i);
//   }, i * 1000);
// }
// BUG: `var` is function-scoped, so all 5 callbacks share the SAME `i`.
// By the time any callback fires, the loop has finished and i === 5.
// Result: prints 5 five times.

// ────────────────────────────────────────────────────────────────
// FIX 1: Replace `var` with `let`
// `let` is block-scoped — each loop iteration creates a NEW binding of `i`
// so each callback closes over its own unique copy.
// ────────────────────────────────────────────────────────────────
for (let i = 0; i < 5; i++) {
  setTimeout(function () {
    console.log(i); // 0, 1, 2, 3, 4 — each `i` is a separate binding
  }, i * 1000);
}

// ────────────────────────────────────────────────────────────────
// FIX 2: Keep `var`, wrap setTimeout in an IIFE
// The IIFE is called immediately with the current value of `i`.
// The parameter `j` inside the IIFE is a NEW local variable that
// captures the value of `i` at that exact moment in the loop.
// ────────────────────────────────────────────────────────────────
for (var i = 0; i < 5; i++) {
  (function (j) {
    // `j` is a fresh local copy of `i` for this iteration
    setTimeout(function () {
      console.log(j); // 0, 1, 2, 3, 4
    }, j * 1000);
  })(i);
}
