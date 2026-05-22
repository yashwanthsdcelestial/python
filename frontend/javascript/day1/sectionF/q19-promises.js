// Q19. Promises — Convert, Chain & Run Concurrently
// Topics: Promise Constructor, .then/.catch, Promise.all, Promise.allSettled, Promise.race

const users = { 1: "alice", 2: "bob", 3: "carol" };
const orders = { alice: "ORD-101", bob: "ORD-102", carol: "ORD-103" };
const totals = { "ORD-101": 2500, "ORD-102": 1800, "ORD-103": 3200 };

// ── (a) Promise-based versions of the three async functions ──

function fetchUser(userId) {
  return new Promise((resolve, reject) => {
    console.log(`Fetching user ${userId}...`);
    setTimeout(() => {
      if (!users[userId]) return reject(new Error("User not found"));
      resolve({ id: userId, name: users[userId] });
    }, 1000);
  });
}

function fetchOrders(userId) {
  return new Promise((resolve, reject) => {
    const name = users[userId];
    console.log(`Fetching orders for ${name}...`);
    setTimeout(() => {
      if (!name || !orders[name]) return reject(new Error("Orders not found"));
      resolve({ orderId: orders[name] });
    }, 1000);
  });
}

function fetchOrderTotal(orderId) {
  return new Promise((resolve, reject) => {
    console.log(`Fetching total for order ${orderId}...`);
    setTimeout(() => {
      if (!totals[orderId]) return reject(new Error("Order not found"));
      resolve({ total: totals[orderId] });
    }, 1000);
  });
}

// ── (b) Chained with .then() — single .catch() at the end ──
console.log("=== Part (b): Chain ===");
fetchUser(1)
  .then((user) => fetchOrders(user.id))
  .then((order) => fetchOrderTotal(order.orderId))
  .then((result) => console.log("Total:", result.total)) // Total: 2500
  .catch((err) => console.error("Error:", err.message));

// ── (c) Promise.all — fetch 3 users concurrently ──
setTimeout(async () => {
  console.log("\n=== Part (c): Promise.all ===");
  try {
    const usersResult = await Promise.all([fetchUser(1), fetchUser(2), fetchUser(3)]);
    console.log(usersResult);
    // [{ id: 1, name: "alice" }, { id: 2, name: "bob" }, { id: 3, name: "carol" }]
  } catch (err) {
    console.error("Promise.all failed:", err.message);
  }
}, 4000);

// ── (d) Promise.allSettled — attempt users 1, 2, 10 (10 will fail) ──
setTimeout(async () => {
  console.log("\n=== Part (d): Promise.allSettled ===");
  const results = await Promise.allSettled([fetchUser(1), fetchUser(2), fetchUser(10)]);
  results.forEach((r) => {
    if (r.status === "fulfilled") {
      console.log("fulfilled:", r.value);
    } else {
      console.log("rejected:", r.reason.message);
    }
  });
  // fulfilled: { id: 1, name: "alice" }
  // fulfilled: { id: 2, name: "bob" }
  // rejected: User not found
}, 6000);

// ── (e) Promise.race — race fetchUser(1) against a 500ms timeout ──
setTimeout(async () => {
  console.log("\n=== Part (e): Promise.race ===");
  const timeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), 500)
  );
  try {
    // fetchUser takes 1000ms, timeout fires at 500ms → Timeout wins
    const result = await Promise.race([fetchUser(1), timeout]);
    console.log("Race winner:", result);
  } catch (err) {
    console.error("Race lost:", err.message); // Race lost: Timeout
  }

  // Now race with a 1500ms timeout → fetchUser wins
  const longTimeout = new Promise((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), 1500)
  );
  try {
    const result = await Promise.race([fetchUser(1), longTimeout]);
    console.log("Race winner:", result); // { id: 1, name: "alice" }
  } catch (err) {
    console.error("Race lost:", err.message);
  }
}, 8000);
