// q17-typescript-basics.ts
// Run: tsc q17-typescript-basics.ts && node q17-typescript-basics.js
// Or:  npx ts-node q17-typescript-basics.ts

// ══════════════════════════════════════════════════════════════
//  (a) Type Guards
// ══════════════════════════════════════════════════════════════

/** isString — narrows unknown to string */
function isString(value: unknown): value is string {
  return typeof value === 'string';
}

function isNumber(value: unknown): value is number {
  return typeof value === 'number' && !isNaN(value);
}

function isArray<T>(value: unknown): value is T[] {
  return Array.isArray(value);
}

// Usage examples
const val1: unknown = 'hello';
const val2: unknown = 42;
const val3: unknown = ['a', 'b'];

if (isString(val1))  console.log('(a) isString:', val1.toUpperCase()); // HELLO
if (isNumber(val2))  console.log('(a) isNumber:', val2.toFixed(2));    // 42.00
if (isArray(val3))   console.log('(a) isArray: ', val3.length);        // 2


// ══════════════════════════════════════════════════════════════
//  (b) Generic first / last
// ══════════════════════════════════════════════════════════════

function first<T>(arr: T[]): T | undefined {
  return arr.length > 0 ? arr[0] : undefined;
}

function last<T>(arr: T[]): T | undefined {
  return arr.length > 0 ? arr[arr.length - 1] : undefined;
}

function nth<T>(arr: T[], index: number): T | undefined {
  return arr[index];
}

// Usage
console.log('\n(b) first([1,2,3]):', first([1, 2, 3]));      // 1
console.log('(b) last([1,2,3]):', last([1, 2, 3]));          // 3
console.log('(b) first(["a","b"]):', first(['a', 'b']));      // a
console.log('(b) first([]):', first([]));                     // undefined


// ══════════════════════════════════════════════════════════════
//  (c) Type-safe event handler using EventMap + keyof
// ══════════════════════════════════════════════════════════════

// Define all event types and their payloads
interface EventMap {
  click:    { x: number; y: number };
  keypress: { key: string; code: string };
  resize:   { width: number; height: number };
  submit:   { formId: string; data: Record<string, string> };
}

type EventHandler<K extends keyof EventMap> = (data: EventMap[K]) => void;

// Event emitter class — type-safe: can only subscribe to events in EventMap
class TypedEventEmitter {
  private handlers: Partial<{ [K in keyof EventMap]: EventHandler<K>[] }> = {};

  on<K extends keyof EventMap>(event: K, handler: EventHandler<K>): void {
    if (!this.handlers[event]) {
      (this.handlers as any)[event] = [];
    }
    (this.handlers[event] as EventHandler<K>[]).push(handler);
  }

  emit<K extends keyof EventMap>(event: K, data: EventMap[K]): void {
    const eventHandlers = this.handlers[event] as EventHandler<K>[] | undefined;
    eventHandlers?.forEach(h => h(data));
  }
}

const emitter = new TypedEventEmitter();

// These are fully typed — handler args inferred from EventMap
emitter.on('click',    (data) => console.log(`\n(c) click at x=${data.x}, y=${data.y}`));
emitter.on('keypress', (data) => console.log(`(c) key pressed: ${data.key}`));
emitter.on('resize',   (data) => console.log(`(c) resized to ${data.width}x${data.height}`));

emitter.emit('click',    { x: 100, y: 200 });
emitter.emit('keypress', { key: 'Enter', code: 'Enter' });
emitter.emit('resize',   { width: 1280, height: 720 });

// TypeScript compile error (uncomment to see):
// emitter.on('unknown', () => {}); // Error: not in EventMap
// emitter.emit('click', { key: 'a' }); // Error: wrong payload shape


// ══════════════════════════════════════════════════════════════
//  (d) Generic ApiResponse<T> with createResponse factory
// ══════════════════════════════════════════════════════════════

interface ApiResponse<T> {
  data:       T;
  status:     number;
  success:    boolean;
  timestamp:  string;
  error?:     string;
}

function createResponse<T>(data: T, status: number): ApiResponse<T> {
  return {
    data,
    status,
    success:   status >= 200 && status < 300,
    timestamp: new Date().toISOString(),
  };
}

function createErrorResponse<T>(error: string, status: number): ApiResponse<T | null> {
  return {
    data:      null,
    status,
    success:   false,
    timestamp: new Date().toISOString(),
    error,
  };
}

// Usage — data is fully typed
const userRes   = createResponse({ name: 'Alice', age: 25 }, 200);
const postsRes  = createResponse([{ id: 1, title: 'Hello' }], 200);
const errorRes  = createErrorResponse<{ name: string }>('Not found', 404);

console.log('\n(d) createResponse:', JSON.stringify(userRes, null, 2));
console.log('(d) posts count:', postsRes.data.length);       // 1 — typed as array
console.log('(d) error:', errorRes.error, errorRes.status);  // Not found 404

// Type safety examples (compile errors if uncommented):
// userRes.data.nonExistent; // Error: Property does not exist
// postsRes.data.name;       // Error: Property 'name' does not exist on array


// ══════════════════════════════════════════════════════════════
//  Bonus: Utility type helpers
// ══════════════════════════════════════════════════════════════

// DeepReadonly — makes all nested properties readonly
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// Nullable — wraps a type to allow null
type Nullable<T> = T | null;

// MaybePromise — value or promise of value
type MaybePromise<T> = T | Promise<T>;

// Usage
type ReadonlyUser = DeepReadonly<{ name: string; address: { city: string } }>;
const ru: ReadonlyUser = { name: 'Alice', address: { city: 'NYC' } };
// ru.name = 'Bob'; // Error: readonly
// ru.address.city = 'LA'; // Error: readonly (deep)

console.log('\n✓ All TypeScript examples compiled successfully');
