// Q12. Config Builder with Destructuring
// Topics: Destructuring, Default Values, Spread, Object.freeze

function deepFreeze(obj) {
  Object.keys(obj).forEach((key) => {
    if (typeof obj[key] === "object" && obj[key] !== null) {
      deepFreeze(obj[key]);
    }
  });
  return Object.freeze(obj);
}

function createConfig({
  server: { port: serverPort = 3000, host = "localhost" } = {},
  database: {
    url = "postgres://localhost:5432/mydb",
    poolSize = 5,
  } = {},
  logging: { level = "info", file = "app.log" } = {},
} = {}) {
  const config = {
    server: { port: serverPort, host },
    database: { url, poolSize },
    logging: { level, file },
  };

  return deepFreeze(config);
}

// --- Tests ---
const config1 = createConfig({
  server: { port: 9090 },
  logging: { level: "debug" },
});
console.log(config1);
// { server: { port: 9090, host: "localhost" },
//   database: { url: "postgres://...", poolSize: 5 },
//   logging: { level: "debug", file: "app.log" } }

const config2 = createConfig({});
console.log(config2);
// { server: { port: 3000, host: "localhost" }, ... }

// Mutation silently fails in non-strict mode, throws in strict mode
config2.server.port = 9999;
console.log(config2.server.port); // 3000 — freeze works
