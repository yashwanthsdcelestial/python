// Q20. Async/Await — Sequential vs Concurrent & Retry
// Topics: async/await, try/catch, Promise.all, Sequential vs Concurrent, Retry Pattern

const users = { 1: "alice", 2: "bob", 3: "carol" };
const orders = { alice: "ORD-101", bob: "ORD-102", carol: "ORD-103" };
const totals = { "ORD-101": 2500, "ORD-102": 1800, "ORD-103": 3200 };

// ── Shared helpers ──
const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function fetchUser(userId) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!users[userId]) return reject(new Error("User not found"));
      resolve({ id: userId, name: users[userId] });
    }, 1000);
  });
}

function fetchOrders(userId) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const name = users[userId];
      if (!name || !orders[name]) return reject(new Error("Orders not found"));
      resolve({ orderId: orders[name] });
    }, 1000);
  });
}

function fetchOrderTotal(orderId) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (!totals[orderId]) return reject(new Error("Order not found"));
      resolve({ total: totals[orderId] });
    }, 1000);
  });
}

// ════════════════════════════════════════════════════════════
// Part (a): async/await with try/catch — rewrite of Q19 chain
// ════════════════════════════════════════════════════════════
async function getOrderTotal(userId) {
  try {
    const user = await fetchUser(userId);
    const order = await fetchOrders(user.id);
    const result = await fetchOrderTotal(order.orderId);
    console.log(`User: ${user.name} | Order: ${order.orderId} | Total: ${result.total}`);
  } catch (err) {
    console.error("Error:", err.message);
  }
}

// ════════════════════════════════════════════════════════════
// Part (b): Sequential fetch — one after another (~3 seconds)
// ════════════════════════════════════════════════════════════
async function fetchUsersSequential(userIds) {
  const start = Date.now();
  for (const id of userIds) {
    const user = await fetchUser(id); // waits for each before starting the next
    const elapsed = ((Date.now() - start) / 1000).toFixed(1);
    console.log(`[${elapsed}s] Fetched user ${id}: ${user.name}`);
  }
}

// ════════════════════════════════════════════════════════════
// Part (c): Concurrent fetch — all at once (~1 second)
// ════════════════════════════════════════════════════════════
async function fetchUsersConcurrent(userIds) {
  const start = Date.now();
  console.log(`[0.0s] Starting all fetches...`);
  const results = await Promise.all(userIds.map((id) => fetchUser(id)));
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);
  console.log(`[${elapsed}s] All fetched: ${results.map((u) => u.name).join(", ")}`);
}

// ════════════════════════════════════════════════════════════
// Part (d): Retry — retries a failing fetch up to maxRetries times
// ════════════════════════════════════════════════════════════
async function fetchWithRetry(userId, maxRetries) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const user = await fetchUser(userId);
      return user; // success — return immediately
    } catch (err) {
      console.log(`[retry] Attempt ${attempt} failed: ${err.message}`);
      if (attempt < maxRetries) await delay(500); // wait before next attempt
    }
  }
  throw new Error(`All ${maxRetries} attempts failed for userId ${userId}`);
}

// ── Run all parts in sequence ──
(async () => {
  console.log("=== Part (a): async/await chain ===");
  await getOrderTotal(1);
  // User: alice | Order: ORD-101 | Total: 2500

  console.log("\n=== Part (b): Sequential (~3s) ===");
  console.time("sequential");
  await fetchUsersSequential([1, 2, 3]);
  console.timeEnd("sequential"); // ~3000ms

  console.log("\n=== Part (c): Concurrent (~1s) ===");
  console.time("concurrent");
  await fetchUsersConcurrent([1, 2, 3]);
  console.timeEnd("concurrent"); // ~1000ms

  console.log("\n=== Part (d): Retry (userId=10, maxRetries=3) ===");
  try {
    await fetchWithRetry(10, 3);
  } catch (err) {
    console.error("Error:", err.message);
    // Error: All 3 attempts failed for userId 10
  }
})();
