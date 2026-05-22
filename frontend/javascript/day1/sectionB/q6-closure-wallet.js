// Q6. Closure — Wallet with Private State
// Topics: Closures, Data Privacy, Higher-Order Functions

function createWallet(ownerName, initialBalance) {
  // Private state — not accessible from outside
  let balance = initialBalance;
  const history = [];

  function deposit(amount) {
    if (amount <= 0) throw new Error("Deposit amount must be positive.");
    balance += amount;
    history.push({ type: "deposit", amount, balance });
  }

  function withdraw(amount) {
    if (amount <= 0) throw new Error("Withdrawal amount must be positive.");
    if (amount > balance) {
      throw new Error(`Insufficient balance. Current balance: ${balance}`);
    }
    balance -= amount;
    history.push({ type: "withdraw", amount, balance });
  }

  function getBalance() {
    return balance;
  }

  function getOwner() {
    return ownerName;
  }

  function getHistory() {
    // Return a shallow copy to prevent external mutation
    return [...history];
  }

  return { deposit, withdraw, getBalance, getOwner, getHistory };
}

// --- Tests ---
const wallet = createWallet("Alice", 1000);
wallet.deposit(500);
wallet.withdraw(200);

console.log(wallet.getBalance());  // 1300
console.log(wallet.getHistory());  // [{type:"deposit",amount:500,balance:1500}, {type:"withdraw",amount:200,balance:1300}]
console.log(wallet.getOwner());    // "Alice"

// Balance is truly private
console.log(wallet.balance);      // undefined

try {
  wallet.withdraw(2000);
} catch (e) {
  console.error("Error:", e.message); // Error: Insufficient balance. Current balance: 1300
}
