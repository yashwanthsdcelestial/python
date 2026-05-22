// Q4. Three Function Forms with Rest & Defaults
// Topics: Function Declaration, Expression, Arrow, Default Params, Rest Params

// ── Hoisting demo: calling the DECLARATION before its definition works ──
const prices = [500, 300, 200];
console.log("Hoisted call:", calculateTotal(prices, 0.18, 50, 30)); // 1085.6

// ── 1. Function Declaration (hoisted) ──
function calculateTotal(prices, taxRate = 0.18, ...discounts) {
  const sum = prices.reduce((acc, p) => acc + p, 0);
  const discounted = Math.max(0, discounts.reduce((acc, d) => acc - d, sum));
  return discounted * (1 + taxRate);
}

// ── 2. Function Expression (NOT hoisted) ──
// Calling before definition throws ReferenceError:
// console.log(calculateTotalExpr(prices)); // ❌ ReferenceError
const calculateTotalExpr = function (prices, taxRate = 0.18, ...discounts) {
  const sum = prices.reduce((acc, p) => acc + p, 0);
  const discounted = Math.max(0, discounts.reduce((acc, d) => acc - d, sum));
  return discounted * (1 + taxRate);
};

// ── 3. Arrow Function (NOT hoisted) ──
// Calling before definition throws ReferenceError:
// console.log(calculateTotalArrow(prices)); // ❌ ReferenceError
const calculateTotalArrow = (prices, taxRate = 0.18, ...discounts) => {
  const sum = prices.reduce((acc, p) => acc + p, 0);
  const discounted = Math.max(0, discounts.reduce((acc, d) => acc - d, sum));
  return discounted * (1 + taxRate);
};

// --- Tests ---
console.log(calculateTotal(prices, 0.18, 50, 30)); // 1085.6
console.log(calculateTotal(prices));               // 1180
console.log(calculateTotal(prices, 0.05));         // 1050

console.log(calculateTotalExpr(prices, 0.18, 50, 30)); // 1085.6
console.log(calculateTotalArrow(prices, 0.18, 50, 30)); // 1085.6

// Clamping: discounts exceed the sum → total before tax = 0
console.log(calculateTotal([100], 0.18, 200)); // 0 (not negative)
