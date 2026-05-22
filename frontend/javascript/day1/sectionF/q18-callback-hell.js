// Q18. Callback Hell & Refactor
// Topics: Callbacks, Error-First Pattern, Nested Async

const users = { 1: "alice", 2: "bob", 3: "carol" };
const orders = { alice: "ORD-101", bob: "ORD-102", carol: "ORD-103" };
const totals = { "ORD-101": 2500, "ORD-102": 1800, "ORD-103": 3200 };

// ── Simulated async functions (error-first callback pattern) ──

function fetchUser(userId, callback) {
  console.log(`Fetching user ${userId}...`);
  setTimeout(() => {
    if (!users[userId]) return callback(new Error("User not found"));
    callback(null, { id: userId, name: users[userId] });
  }, 1000);
}

function fetchOrders(userId, callback) {
  const name = users[userId];
  console.log(`Fetching orders for ${name}...`);
  setTimeout(() => {
    if (!name || !orders[name]) return callback(new Error("Orders not found"));
    callback(null, { orderId: orders[name] });
  }, 1000);
}

function fetchOrderTotal(orderId, callback) {
  console.log(`Fetching total for order ${orderId}...`);
  setTimeout(() => {
    if (!totals[orderId]) return callback(new Error("Order not found"));
    callback(null, { total: totals[orderId] });
  }, 1000);
}

// ════════════════════════════════════════════════════════════
// CALLBACK HELL VERSION — 3 levels of nesting
// ════════════════════════════════════════════════════════════
function getUserOrderTotalNested(userId, finalCallback) {
  fetchUser(userId, (err, user) => {
    if (err) return finalCallback(err);
    fetchOrders(user.id, (err, order) => {
      if (err) return finalCallback(err);
      fetchOrderTotal(order.orderId, (err, result) => {
        if (err) return finalCallback(err);
        finalCallback(null, { user: user.name, orderId: order.orderId, total: result.total });
      });
    });
  });
}

// ════════════════════════════════════════════════════════════
// FLATTENED VERSION — named handler functions
// ════════════════════════════════════════════════════════════
function getUserOrderTotal(userId, finalCallback) {
  function handleUser(err, user) {
    if (err) return finalCallback(err);
    fetchOrders(user.id, handleOrders.bind(null, user));
  }

  function handleOrders(user, err, order) {
    if (err) return finalCallback(err);
    fetchOrderTotal(order.orderId, handleTotal.bind(null, user, order));
  }

  function handleTotal(user, order, err, result) {
    if (err) return finalCallback(err);
    finalCallback(null, { user: user.name, orderId: order.orderId, total: result.total });
  }

  fetchUser(userId, handleUser);
}

// --- Tests ---
console.log("=== Flattened Version ===");
getUserOrderTotal(1, (err, result) => {
  if (err) return console.error("Error:", err.message);
  console.log(result); // { user: "alice", orderId: "ORD-101", total: 2500 }
});

// Error simulation: userId 10 doesn't exist
setTimeout(() => {
  console.log("\n=== Error Case (userId=10) ===");
  getUserOrderTotal(10, (err, result) => {
    if (err) return console.error("Error:", err.message); // Error: User not found
    console.log(result);
  });
}, 4000);
