// utils.js — Utility functions: debounce, toast, validation (ES6 module)

// ── Debounce (from scratch) ──────────────────────────────────
export function debounce(fn, delay) {
  let timerId = null;
  return function(...args) {
    clearTimeout(timerId);
    timerId = setTimeout(() => { timerId = null; fn.apply(this, args); }, delay);
  };
}

// ── City name validation ─────────────────────────────────────
export function validateCityName(name) {
  if (!name || !name.trim()) return 'City name cannot be empty';
  if (!/^[a-zA-Z\s\-'.]+$/.test(name.trim())) return 'City name must contain only letters, spaces, or hyphens';
  if (name.trim().length < 2) return 'City name too short';
  return '';
}

// ── Toast notification system (minimal, self-contained) ──────
let toastContainer = null;

function getToastContainer() {
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.style.cssText =
      'position:fixed;bottom:1.25rem;right:1.25rem;display:flex;flex-direction:column-reverse;gap:8px;z-index:9999;max-width:320px;pointer-events:none';
    document.body.appendChild(toastContainer);
  }
  return toastContainer;
}

export function showToast(message, type = 'info', duration = 3500) {
  const colors = { success: '#16a34a', error: '#dc2626', warning: '#d97706', info: '#0284c7' };
  const icons  = { success: '✓', error: '✕', warning: '⚠', info: 'ℹ' };

  const toast = document.createElement('div');
  toast.style.cssText = `
    background:white;border-radius:9px;padding:.75rem 1rem;
    display:flex;align-items:center;gap:10px;font-size:14px;
    box-shadow:0 4px 16px rgba(0,0,0,.12);
    border-left:4px solid ${colors[type] || colors.info};
    pointer-events:all;transform:translateX(110%);
    transition:transform .28s cubic-bezier(.4,0,.2,1);
  `;

  const icon = document.createElement('span');
  icon.textContent = icons[type] || 'ℹ';
  icon.style.cssText = `color:${colors[type]};font-weight:700;flex-shrink:0`;

  const msg = document.createElement('span');
  msg.textContent = message;
  msg.style.color = '#111827';

  toast.appendChild(icon);
  toast.appendChild(msg);
  getToastContainer().appendChild(toast);

  requestAnimationFrame(() => {
    requestAnimationFrame(() => { toast.style.transform = 'translateX(0)'; });
  });

  const dismiss = () => {
    toast.style.transform = 'translateX(110%)';
    setTimeout(() => toast.remove(), 300);
  };
  toast.addEventListener('click', dismiss);
  if (duration > 0) setTimeout(dismiss, duration);
}

// ── Format helpers ────────────────────────────────────────────
export function formatDate(isoStr) {
  return new Date(isoStr).toLocaleDateString('en-IN', { weekday: 'short', month: 'short', day: 'numeric' });
}

export function getWindDirection(deg) {
  const dirs = ['N','NE','E','SE','S','SW','W','NW'];
  return dirs[Math.round(deg / 45) % 8];
}
