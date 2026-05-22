// q19-generic-data-structures.ts
// Run: npx ts-node q19-generic-data-structures.ts

// ══════════════════════════════════════════════════════════════
//  (a) Generic Stack<T>
// ══════════════════════════════════════════════════════════════

class Stack<T> {
  private _data: T[] = [];

  push(item: T): void {
    this._data.push(item);
  }

  pop(throwOnEmpty: boolean = true): T | undefined {
    if (this.isEmpty()) {
      if (throwOnEmpty) throw new Error('Stack underflow: cannot pop from empty stack');
      return undefined;
    }
    return this._data.pop();
  }

  peek(throwOnEmpty: boolean = true): T | undefined {
    if (this.isEmpty()) {
      if (throwOnEmpty) throw new Error('Stack is empty: nothing to peek');
      return undefined;
    }
    return this._data[this._data.length - 1];
  }

  isEmpty(): boolean  { return this._data.length === 0; }
  get size(): number  { return this._data.length; }
  toArray(): T[]      { return [...this._data]; }
  clear(): void       { this._data = []; }

  toString(): string {
    return `Stack[${this._data.join(' → ')}] (top: ${this.peek(false)})`;
  }
}

// Demo
const numStack = new Stack<number>();
numStack.push(1); numStack.push(2); numStack.push(3);
console.log('=== Stack<number> ===');
console.log('Size:', numStack.size);        // 3
console.log('Peek:', numStack.peek());      // 3
console.log('Pop: ', numStack.pop());       // 3
console.log('Pop: ', numStack.pop());       // 2
console.log('Peek:', numStack.peek());      // 1
console.log('Array:', numStack.toArray()); // [1]

const strStack = new Stack<string>();
strStack.push('a'); strStack.push('b');
console.log('Stack<string>:', strStack.toString());

try {
  const empty = new Stack<number>();
  empty.pop(); // throws
} catch (e: unknown) {
  if (e instanceof Error) console.log('Expected error:', e.message);
}


// ══════════════════════════════════════════════════════════════
//  (b) Generic Dictionary<K extends string | number, V>
// ══════════════════════════════════════════════════════════════

class Dictionary<K extends string | number, V> {
  private _map: Map<K, V> = new Map();

  set(key: K, value: V): this {
    this._map.set(key, value);
    return this; // chainable
  }

  get(key: K): V | undefined {
    return this._map.get(key);
  }

  has(key: K): boolean {
    return this._map.has(key);
  }

  delete(key: K): boolean {
    return this._map.delete(key);
  }

  keys(): K[] {
    return Array.from(this._map.keys());
  }

  values(): V[] {
    return Array.from(this._map.values());
  }

  entries(): [K, V][] {
    return Array.from(this._map.entries());
  }

  forEach(callback: (value: V, key: K) => void): void {
    this._map.forEach((v, k) => callback(v, k));
  }

  get size(): number { return this._map.size; }
  clear(): void      { this._map.clear(); }

  toObject(): Record<string, V> {
    const obj: Record<string, V> = {};
    this._map.forEach((v, k) => { obj[String(k)] = v; });
    return obj;
  }
}

// Demo
console.log('\n=== Dictionary<string, number> ===');
const dict = new Dictionary<string, number>();
dict.set('age', 25).set('score', 99).set('level', 5);

console.log('get age:  ', dict.get('age'));          // 25
console.log('has score:', dict.has('score'));        // true
console.log('has xyz:  ', dict.has('xyz'));          // false
console.log('keys:     ', dict.keys());              // ['age', 'score', 'level']
console.log('values:   ', dict.values());            // [25, 99, 5]

dict.delete('level');
console.log('after delete level — size:', dict.size); // 2
console.log('toObject:', dict.toObject());

// Numeric key
const numDict = new Dictionary<number, string>();
numDict.set(1, 'one').set(2, 'two').set(3, 'three');
console.log('\nDictionary<number, string>:');
numDict.forEach((v, k) => console.log(`  ${k} → ${v}`));


// ══════════════════════════════════════════════════════════════
//  (c) Generic Result<T, E> — discriminated union (Rust-style)
// ══════════════════════════════════════════════════════════════

type OkResult<T>  = { ok: true;  value: T };
type ErrResult<E> = { ok: false; error: E };
type Result<T, E> = OkResult<T> | ErrResult<E>;

// Factory functions
function ok<T>(value: T): OkResult<T> {
  return { ok: true, value };
}

function err<E>(error: E): ErrResult<E> {
  return { ok: false, error };
}

/** unwrap — returns value or throws */
function unwrap<T, E>(result: Result<T, E>): T {
  if (result.ok) return result.value;
  throw new Error(`Unwrap failed: ${String(result.error)}`);
}

/** unwrapOr — returns value or fallback */
function unwrapOr<T, E>(result: Result<T, E>, fallback: T): T {
  return result.ok ? result.value : fallback;
}

/** map — transform the Ok value */
function mapResult<T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> {
  if (result.ok) return ok(fn(result.value));
  return result;
}

/** flatMap — chain Result-returning operations */
function flatMap<T, U, E>(result: Result<T, E>, fn: (value: T) => Result<U, E>): Result<U, E> {
  if (result.ok) return fn(result.value);
  return result;
}

/** isOk / isErr type narrowing helpers */
function isOk<T, E>(result: Result<T, E>): result is OkResult<T>  { return result.ok === true; }
function isErr<T, E>(result: Result<T, E>): result is ErrResult<E>{ return result.ok === false; }

// Demo
console.log('\n=== Result<T, E> ===');

const r1: Result<number, string> = ok(42);
const r2: Result<number, string> = err('not found');

console.log('r1 ok:     ', r1.ok);                // true
console.log('unwrap r1: ', unwrap(r1));            // 42
console.log('unwrapOr r2:', unwrapOr(r2, 0));      // 0

// map
const doubled = mapResult(r1, x => x * 2);
console.log('map *2:    ', isOk(doubled) ? doubled.value : 'err'); // 84

// flatMap chaining
function safeDivide(a: number, b: number): Result<number, string> {
  if (b === 0) return err('Division by zero');
  return ok(a / b);
}

function safeSquareRoot(n: number): Result<number, string> {
  if (n < 0) return err('Negative number');
  return ok(Math.sqrt(n));
}

const chainResult = flatMap(safeDivide(16, 4), safeSquareRoot);
console.log('chain 16/4 then sqrt:', isOk(chainResult) ? chainResult.value : chainResult.error); // 2

const divByZero = flatMap(safeDivide(10, 0), safeSquareRoot);
console.log('chain 10/0:', isErr(divByZero) ? divByZero.error : divByZero.value); // Division by zero

// Try-catch wrapper that returns a Result
function tryResult<T>(fn: () => T): Result<T, Error> {
  try   { return ok(fn()); }
  catch (e) { return err(e instanceof Error ? e : new Error(String(e))); }
}

const parsed = tryResult(() => JSON.parse('{"name":"Alice"}'));
const invalid = tryResult(() => JSON.parse('not-valid-json'));
console.log('tryResult valid:', isOk(parsed) ? parsed.value : 'err');
console.log('tryResult error:', isErr(invalid) ? invalid.error.message.slice(0, 30) : 'ok');

try {
  unwrap(r2); // should throw
} catch (e: unknown) {
  if (e instanceof Error) console.log('Expected unwrap error:', e.message);
}

console.log('\n✓ All generic data structure examples ran successfully');
