// storage.js — localStorage + cookie helpers (ES6 module)

const FAVORITES_KEY = 'weather_favorites';
const THEME_KEY     = 'weather_theme';

// ── Favorites (localStorage) ──────────────────────────────────

export function getFavorites() {
  try {
    return JSON.parse(localStorage.getItem(FAVORITES_KEY) || '[]');
  } catch { return []; }
}

export function saveFavorites(favorites) {
  try {
    localStorage.setItem(FAVORITES_KEY, JSON.stringify(favorites));
  } catch (e) {
    if (e.name === 'QuotaExceededError') throw new Error('Storage full');
  }
}

export function addFavorite(weather) {
  // Guard: need a valid city name
  const name = weather && weather.city;
  if (!name || typeof name !== 'string') return false;

  const favs = getFavorites();
  if (favs.find(f => f.name.toLowerCase() === name.toLowerCase())) return false;

  favs.push({
    name,
    lat:     weather.lat,
    lon:     weather.lon,
    addedAt: new Date().toISOString(),
  });
  saveFavorites(favs);
  return true;
}

export function removeFavorite(cityName) {
  if (!cityName) return;
  const lower = cityName.toLowerCase();
  saveFavorites(getFavorites().filter(f => f.name.toLowerCase() !== lower));
}

export function isFavorite(cityName) {
  if (!cityName || typeof cityName !== 'string') return false;
  const lower = cityName.toLowerCase();
  return getFavorites().some(f => f.name.toLowerCase() === lower);
}

// ── Theme (localStorage) ──────────────────────────────────────

export function getTheme() {
  return localStorage.getItem(THEME_KEY) || 'light';
}

export function saveTheme(theme) {
  localStorage.setItem(THEME_KEY, theme);
}

// ── Last searched city (Cookie, expires 7 days) ───────────────

export function saveLastCity(cityName) {
  if (!cityName) return;
  const d = new Date();
  d.setTime(d.getTime() + 7 * 24 * 60 * 60 * 1000);
  document.cookie = `last_city=${encodeURIComponent(cityName)}; expires=${d.toUTCString()}; path=/; SameSite=Lax`;
}

export function getLastCity() {
  const match = document.cookie.split(';').find(c => c.trim().startsWith('last_city='));
  return match ? decodeURIComponent(match.trim().slice('last_city='.length)) : null;
}
