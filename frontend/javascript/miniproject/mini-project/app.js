// app.js — Main entry point for Weather Dashboard

import { searchCity, fetchWeather }                        from './api.js';
import { getFavorites, addFavorite, removeFavorite, isFavorite, getTheme, saveTheme, saveLastCity, getLastCity } from './storage.js';
import { debounce, validateCityName, showToast }           from './utils.js';
import { buildWeatherCard, buildFavoriteItem, createSpinner, createErrorCard, updateFavBtn } from './ui.js';

// ══════════════════════════════════════════════════════════════
//  Observer Pattern
// ══════════════════════════════════════════════════════════════
const observers = {};
function subscribe(event, handler) {
  if (!observers[event]) observers[event] = [];
  observers[event].push(handler);
}
function publish(event, data) {
  (observers[event] || []).forEach(h => h(data));
}

// ══════════════════════════════════════════════════════════════
//  App State
// ══════════════════════════════════════════════════════════════
const state = {
  currentWeather: null,
  theme:          getTheme(),
  loading:        false,
  lastQuery:      '',
};

// ══════════════════════════════════════════════════════════════
//  DOM refs
// ══════════════════════════════════════════════════════════════
const searchInput   = document.getElementById('search-input');
const searchBtn     = document.getElementById('search-btn');
const searchError   = document.getElementById('search-error');
const weatherOutput = document.getElementById('weather-output');
const favList       = document.getElementById('fav-list');
const themeToggle   = document.getElementById('theme-toggle');
const favCount      = document.getElementById('fav-count');

// ══════════════════════════════════════════════════════════════
//  Theme
// ══════════════════════════════════════════════════════════════
function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  themeToggle.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
}

themeToggle.addEventListener('click', () => {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  saveTheme(state.theme);
  applyTheme(state.theme);
});

// ══════════════════════════════════════════════════════════════
//  Search
// ══════════════════════════════════════════════════════════════
async function doSearch(query) {
  query = (query || '').trim();
  const errorMsg = validateCityName(query);
  if (errorMsg) {
    searchError.textContent = errorMsg;
    searchInput.setCustomValidity(errorMsg);
    return;
  }
  searchError.textContent = '';
  searchInput.setCustomValidity('');

  state.loading   = true;
  state.lastQuery = query;
  weatherOutput.innerHTML = '';

  const spinner = createSpinner(`Searching for "${query}"…`);
  weatherOutput.appendChild(spinner);
  searchBtn.disabled = true;

  try {
    // 1. Geocode city name → coordinates
    const cities = await searchCity(query);
    if (!cities.length) {
      weatherOutput.innerHTML = '';
      weatherOutput.appendChild(createErrorCard(`City "${query}" not found. Try a different spelling.`));
      showToast(`City "${query}" not found`, 'warning');
      return;
    }

    const city = cities[0];

    // Build a display name: "Mumbai, Maharashtra, India"
    // Guard each field — Open-Meteo may omit admin1 for some cities
    const cityLabel = [city.name, city.admin1, city.country]
      .filter(v => v && String(v).trim())
      .join(', ') || query;

    // 2. Fetch weather using coordinates
    const weather = await fetchWeather(city.latitude, city.longitude, cityLabel);

    state.currentWeather = weather;
    saveLastCity(cityLabel);

    // 3. Render card
    weatherOutput.innerHTML = '';
    const card = buildWeatherCard(weather);
    weatherOutput.appendChild(card);

    showToast(`Weather loaded for ${cityLabel}`, 'success');
    publish('weather:loaded', weather);

  } catch (err) {
    weatherOutput.innerHTML = '';
    weatherOutput.appendChild(createErrorCard(
      `Failed to load weather: ${err.message}`,
      () => doSearch(query)
    ));
    showToast(err.message, 'error');
  } finally {
    state.loading = false;
    searchBtn.disabled = false;
  }
}

// Debounced search — also fires on Enter or button click
const debouncedSearch = debounce((val) => doSearch(val), 300);

searchInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') { e.preventDefault(); doSearch(searchInput.value.trim()); }
});
searchBtn.addEventListener('click', () => doSearch(searchInput.value.trim()));
searchInput.addEventListener('input', () => {
  searchError.textContent = '';
  searchInput.setCustomValidity('');
});

// ══════════════════════════════════════════════════════════════
//  Favorites — Single event listener (Event Delegation)
// ══════════════════════════════════════════════════════════════
favList.addEventListener('click', e => {
  const action = e.target.dataset.action;

  if (action === 'remove-fav') {
    e.stopPropagation();
    const name = e.target.dataset.name;
    if (!confirm(`Remove "${name}" from favorites?`)) return;
    removeFavorite(name);
    publish('favorites:changed', { action: 'remove', name });
    return;
  }

  const li = e.target.closest('.fav-item');
  if (li && li.dataset.name) {
    searchInput.value = li.dataset.name;
    doSearch(li.dataset.name);
  }
});

favList.addEventListener('keydown', e => {
  if (e.key === 'Enter' || e.key === ' ') {
    const li = e.target.closest('.fav-item');
    if (li && !e.target.dataset.action) {
      e.preventDefault();
      doSearch(li.dataset.name);
    }
  }
});

// ══════════════════════════════════════════════════════════════
//  Weather card interactions (Event Bubbling on #weather-output)
// ══════════════════════════════════════════════════════════════
weatherOutput.addEventListener('click', e => {
  const btn = e.target.closest('[data-action="toggle-fav"]');
  if (!btn || !state.currentWeather) return;

  const cityName = state.currentWeather.city;
  if (!cityName) return;

  if (isFavorite(cityName)) {
    if (!confirm(`Remove "${cityName}" from favorites?`)) return;
    removeFavorite(cityName);
    showToast(`Removed ${cityName} from favorites`, 'info');
    publish('favorites:changed', { action: 'remove', name: cityName });
  } else {
    const added = addFavorite(state.currentWeather);
    if (added) {
      showToast(`Added ${cityName} to favorites ★`, 'success');
      publish('favorites:changed', { action: 'add', city: state.currentWeather });
    } else {
      showToast(`${cityName} is already in favorites`, 'warning');
    }
  }
  updateFavBtn(btn, state.currentWeather);
});

// ══════════════════════════════════════════════════════════════
//  Observer — re-render favorites list on any change
// ══════════════════════════════════════════════════════════════
subscribe('favorites:changed', () => renderFavorites());

function renderFavorites() {
  const favs = getFavorites();
  favList.innerHTML = '';
  favCount.textContent = favs.length ? `(${favs.length})` : '';

  if (!favs.length) {
    const empty = document.createElement('li');
    empty.className   = 'fav-empty';
    empty.textContent = 'No favorites yet';
    favList.appendChild(empty);
    return;
  }

  const frag = document.createDocumentFragment();
  favs.forEach(fav => frag.appendChild(buildFavoriteItem(fav)));
  favList.appendChild(frag);
}

// ══════════════════════════════════════════════════════════════
//  Init
// ══════════════════════════════════════════════════════════════
function init() {
  applyTheme(state.theme);
  renderFavorites();

  const lastCity = getLastCity();
  if (lastCity) {
    searchInput.value = lastCity;
    showToast(`Welcome back! Loading "${lastCity}"…`, 'info', 2000);
    setTimeout(() => doSearch(lastCity), 600);
  }
}

init();
