// app.js — Main entry point. No global variables.

// Named imports from barrel file (tree-shaking: only validateEmail is bundled if using a bundler)
import { validateEmail, validatePhone, formatCurrency, formatDate, capitalize } from './utils/index.js';

// Default imports for service classes
import ApiService     from './services/api.js';
import StorageService from './services/storage.js';

// ── Instantiate services ───────────────────────────────────────────────
const api     = new ApiService('https://jsonplaceholder.typicode.com');
const storage = new StorageService('q12');

// ── Demo: validators ──────────────────────────────────────────────────
function demoValidators() {
  const tests = [
    ['Email valid',   validateEmail('alice@example.com')],
    ['Email invalid', validateEmail('not-an-email')],
    ['Phone valid',   validatePhone('9876543210')],
    ['Phone invalid', validatePhone('123')],
  ];
  const el = document.getElementById('validators-out');
  el.textContent = tests.map(([k, v]) => `${v ? '✓' : '✗'} ${k}`).join('\n');
}

// ── Demo: formatters ──────────────────────────────────────────────────
function demoFormatters() {
  const el = document.getElementById('formatters-out');
  el.textContent = [
    `formatDate:     ${formatDate(new Date().toISOString())}`,
    `formatCurrency: ${formatCurrency(99.9)}`,
    `capitalize:     ${capitalize('hello world')}`,
  ].join('\n');
}

// ── Demo: storage ─────────────────────────────────────────────────────
function demoStorage() {
  storage.set('user', { name: 'Alice', role: 'dev' });
  const user = storage.get('user');
  document.getElementById('storage-out').textContent =
    `Stored & retrieved: ${JSON.stringify(user)}`;
}

// ── Demo: API ─────────────────────────────────────────────────────────
async function demoApi() {
  const el = document.getElementById('api-out');
  el.textContent = 'Fetching…';
  try {
    const posts = await api.get('/posts?_limit=2');
    el.textContent = JSON.stringify(posts, null, 2);
  } catch (e) {
    el.textContent = 'Error: ' + e.message;
  }
}

// ── Dynamic import: Modal (loaded only on button click) ───────────────
document.getElementById('open-modal-btn').addEventListener('click', async () => {
  // Modal module is lazy-loaded — not in the initial bundle
  const { default: Modal } = await import('./components/modal.js');
  const modal = new Modal({
    title:     'Dynamic Import Modal',
    content:   'This Modal class was loaded lazily via import() — only when you clicked the button!',
    onConfirm: () => { document.getElementById('modal-result').textContent = 'Confirmed! ✓'; },
    onCancel:  () => { document.getElementById('modal-result').textContent = 'Cancelled.'; },
  });
  modal.open();
});

// ── Init ──────────────────────────────────────────────────────────────
demoValidators();
demoFormatters();
demoStorage();
demoApi();
