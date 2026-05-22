// q20-js-to-ts-refactor.ts
// Full TypeScript refactor with strict mode compliance.
// Run: npx ts-node q20-js-to-ts-refactor.ts

// ══════════════════════════════════════════════════════════════
//  Enums
// ══════════════════════════════════════════════════════════════

enum UserRole {
  Admin  = 'admin',
  Editor = 'editor',
  Viewer = 'viewer',
  Guest  = 'guest',
}

// ══════════════════════════════════════════════════════════════
//  Interfaces
// ══════════════════════════════════════════════════════════════

interface User {
  id:        string;
  name:      string;
  email:     string;
  role:      UserRole;
  createdAt: string;
  updatedAt: string;
  active:    boolean;
}

interface FilterCriteria {
  role?:   UserRole;
  active?: boolean;
  search?: string;          // searches name and email
}

type SortableField = keyof Pick<User, 'name' | 'email' | 'createdAt' | 'role'>;
type SortOrder     = 'asc' | 'desc';

interface PaginatedResponse<T> {
  data:       T[];
  total:      number;
  page:       number;
  limit:      number;
  totalPages: number;
}

interface ApiError {
  message: string;
  code:    number;
  field?:  string;
}

// ══════════════════════════════════════════════════════════════
//  Pure functions (refactored from JS)
// ══════════════════════════════════════════════════════════════

/** createUser — builds a new User object with generated id/timestamps */
function createUser(name: string, email: string, role: UserRole): User {
  const now = new Date().toISOString();
  return {
    id:        `usr_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`,
    name:      name.trim(),
    email:     email.trim().toLowerCase(),
    role,
    createdAt: now,
    updatedAt: now,
    active:    true,
  };
}

/** updateUser — immutable update; returns new User object */
function updateUser(user: User, updates: Partial<Omit<User, 'id' | 'createdAt'>>): User {
  return {
    ...user,
    ...updates,
    id:        user.id,          // id is immutable
    createdAt: user.createdAt,   // createdAt is immutable
    updatedAt: new Date().toISOString(),
  };
}

/** filterUsers — filter by role, active status, and search term */
function filterUsers(users: User[], criteria: FilterCriteria): User[] {
  return users.filter(user => {
    if (criteria.role !== undefined   && user.role   !== criteria.role)   return false;
    if (criteria.active !== undefined && user.active !== criteria.active) return false;
    if (criteria.search) {
      const q = criteria.search.toLowerCase();
      if (!user.name.toLowerCase().includes(q) && !user.email.toLowerCase().includes(q)) {
        return false;
      }
    }
    return true;
  });
}

/** sortUsers — type-safe sort using keyof */
function sortUsers(users: User[], sortBy: SortableField, order: SortOrder = 'asc'): User[] {
  return [...users].sort((a, b) => {
    const valA = a[sortBy];
    const valB = b[sortBy];
    const cmp  = String(valA).localeCompare(String(valB));
    return order === 'asc' ? cmp : -cmp;
  });
}

/** fetchUsers — async with pagination, proper error type */
async function fetchUsers(
  page: number = 1,
  limit: number = 10
): Promise<PaginatedResponse<User>> {
  // Simulate an API call
  await new Promise<void>(r => setTimeout(r, 10));

  // Simulate fetching from a mock DB
  const mockUsers: User[] = Array.from({ length: 25 }, (_, i) =>
    createUser(
      `User ${i + 1}`,
      `user${i + 1}@example.com`,
      Object.values(UserRole)[i % 4] as UserRole
    )
  );

  const start   = (page - 1) * limit;
  const end     = start + limit;
  const data    = mockUsers.slice(start, end);
  const total   = mockUsers.length;

  return {
    data,
    total,
    page,
    limit,
    totalPages: Math.ceil(total / limit),
  };
}

// ══════════════════════════════════════════════════════════════
//  UserService class (fully typed, private fields)
// ══════════════════════════════════════════════════════════════

class UserService {
  private users: User[]                 = [];
  private cache: Map<string, User>      = new Map();
  private readonly MAX_CACHE_SIZE = 100;

  constructor(initialUsers: User[] = []) {
    this.users = [...initialUsers];
    initialUsers.forEach(u => this.cache.set(u.id, u));
  }

  /** getUser — returns from cache first, then searches array */
  getUser(id: string): User | undefined {
    if (this.cache.has(id)) return this.cache.get(id);
    const user = this.users.find(u => u.id === id);
    if (user) this._cacheUser(user);
    return user;
  }

  /** addUser — creates and persists a new user */
  addUser(name: string, email: string, role: UserRole = UserRole.Viewer): User {
    if (!name.trim()) throw new Error('Name is required');
    if (!this._isValidEmail(email)) throw new Error('Invalid email format');
    if (this.users.some(u => u.email === email.toLowerCase())) {
      throw new Error(`Email "${email}" is already taken`);
    }

    const user = createUser(name, email, role);
    this.users.push(user);
    this._cacheUser(user);
    return user;
  }

  /** updateUserById — updates a user by ID */
  updateUserById(id: string, updates: Partial<Omit<User, 'id' | 'createdAt'>>): User {
    const idx = this.users.findIndex(u => u.id === id);
    if (idx === -1) throw new Error(`User ${id} not found`);

    const updated       = updateUser(this.users[idx], updates);
    this.users[idx]     = updated;
    this.cache.set(id, updated);
    return updated;
  }

  /** deleteUser — soft-delete by setting active = false */
  deleteUser(id: string): void {
    this.updateUserById(id, { active: false });
  }

  /** searchUsers — searches by name or email */
  searchUsers(query: string): User[] {
    if (!query.trim()) return this.users.filter(u => u.active);
    return filterUsers(this.users, { search: query, active: true });
  }

  /** getAll — filter + sort + paginate */
  getAll(
    criteria:  FilterCriteria  = {},
    sortBy:    SortableField   = 'name',
    order:     SortOrder       = 'asc',
    page:      number          = 1,
    limit:     number          = 10
  ): PaginatedResponse<User> {
    const filtered = filterUsers(this.users, criteria);
    const sorted   = sortUsers(filtered, sortBy, order);
    const start    = (page - 1) * limit;
    const data     = sorted.slice(start, start + limit);

    return {
      data,
      total:      filtered.length,
      page,
      limit,
      totalPages: Math.ceil(filtered.length / limit),
    };
  }

  get count(): number    { return this.users.length; }
  get activeCount(): number { return this.users.filter(u => u.active).length; }

  private _cacheUser(user: User): void {
    if (this.cache.size >= this.MAX_CACHE_SIZE) {
      const firstKey = this.cache.keys().next().value;
      if (firstKey !== undefined) this.cache.delete(firstKey);
    }
    this.cache.set(user.id, user);
  }

  private _isValidEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
}

// ══════════════════════════════════════════════════════════════
//  Demo
// ══════════════════════════════════════════════════════════════

console.log('=== UserService Demo ===\n');

const service = new UserService();

const alice = service.addUser('Alice Smith',  'alice@example.com', UserRole.Admin);
const bob   = service.addUser('Bob Jones',    'bob@example.com',   UserRole.Editor);
const carol = service.addUser('Carol White',  'carol@example.com', UserRole.Viewer);
const dave  = service.addUser('Dave Brown',   'dave@example.com',  UserRole.Editor);

console.log('Total users:', service.count); // 4

// getUser
const found = service.getUser(alice.id);
console.log('Found:', found?.name, found?.role); // Alice Smith admin

// updateUser
const updatedBob = service.updateUserById(bob.id, { role: UserRole.Admin });
console.log('Updated Bob role:', updatedBob.role); // admin

// searchUsers
const results = service.searchUsers('carol');
console.log('Search "carol":', results.map(u => u.name)); // ['Carol White']

// filterUsers
const editors = filterUsers([alice, bob, carol, dave], { role: UserRole.Admin });
console.log('Admins:', editors.map(u => u.name)); // Alice Smith, Bob Jones(updated)

// sortUsers
const sorted = sortUsers([alice, bob, carol, dave], 'name', 'asc');
console.log('Sorted A-Z:', sorted.map(u => u.name));

// Paginated getAll
const page1 = service.getAll({}, 'name', 'asc', 1, 2);
console.log('\nPage 1 of getAll:', page1.data.map(u => u.name), `(${page1.total} total, ${page1.totalPages} pages)`);

// deleteUser (soft)
service.deleteUser(carol.id);
console.log('\nAfter soft-delete Carol — active count:', service.activeCount); // 3

// fetchUsers (async)
(async () => {
  const paged = await fetchUsers(2, 5);
  console.log('\nfetchUsers page 2:', paged.data.map(u => u.name.slice(0, 6)), `(${paged.totalPages} pages)`);
  console.log('\n✓ All TypeScript refactor examples ran successfully');
})();

// Error handling examples
try {
  service.addUser('', 'bad', UserRole.Guest);
} catch (e: unknown) {
  if (e instanceof Error) console.log('\nExpected error (empty name):', e.message);
}

try {
  service.addUser('Duplicate', 'alice@example.com', UserRole.Viewer);
} catch (e: unknown) {
  if (e instanceof Error) console.log('Expected error (dup email):', e.message);
}
