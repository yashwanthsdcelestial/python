// Q14. The this Problem — Fix the Context
// Topics: this, bind, Arrow Functions, setInterval

// ── BUGGY CODE (reference) ──
// const timer = {
//   seconds: 0,
//   start: function () {
//     setInterval(function () {
//       this.seconds++;          // `this` is undefined (strict) or global — NOT the timer object
//       console.log(`Elapsed: ${this.seconds}s`);
//     }, 1000);
//   },
// };

// ════════════════════════════════════════════════════════════
// FIX 1: bind(this)
// `.bind(this)` creates a new function permanently bound to the
// timer object. The callback's `this` is locked to `timer`.
// ════════════════════════════════════════════════════════════
const timer1 = {
  seconds: 0,
  intervalId: null,
  start: function () {
    this.intervalId = setInterval(
      function () {
        this.seconds++;
        console.log(`[bind] Elapsed: ${this.seconds}s`);
      }.bind(this), // bind locks `this` to the timer1 object
      1000
    );
  },
  stop: function () {
    clearInterval(this.intervalId);
  },
};

// ════════════════════════════════════════════════════════════
// FIX 2: Arrow function
// Arrow functions do NOT have their own `this`. They inherit `this`
// from the surrounding lexical scope — which is `start`'s `this`,
// i.e., the timer object.
// ════════════════════════════════════════════════════════════
const timer2 = {
  seconds: 0,
  intervalId: null,
  start: function () {
    this.intervalId = setInterval(() => {
      // Arrow function: `this` is inherited from `start`, i.e., timer2
      this.seconds++;
      console.log(`[arrow] Elapsed: ${this.seconds}s`);
    }, 1000);
  },
  stop: function () {
    clearInterval(this.intervalId);
  },
};

// ════════════════════════════════════════════════════════════
// FIX 3: const self = this
// We capture the correct `this` in a local variable before the
// callback is defined. The callback closes over `self`, which
// always refers to the timer object.
// ════════════════════════════════════════════════════════════
const timer3 = {
  seconds: 0,
  intervalId: null,
  start: function () {
    const self = this; // capture the correct `this` in a closure variable
    this.intervalId = setInterval(function () {
      self.seconds++; // `self` always points to timer3
      console.log(`[self] Elapsed: ${self.seconds}s`);
    }, 1000);
  },
  stop: function () {
    clearInterval(this.intervalId);
  },
};

// --- Demo (runs for 3 seconds each then stops) ---
timer1.start();
setTimeout(() => timer1.stop(), 3500);

setTimeout(() => {
  timer2.start();
  setTimeout(() => timer2.stop(), 3500);
}, 4000);

setTimeout(() => {
  timer3.start();
  setTimeout(() => timer3.stop(), 3500);
}, 8500);
