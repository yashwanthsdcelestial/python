// ui.js — DOM rendering module (ES6 module)
// All elements built with createElement (no innerHTML for user data)

import { isFavorite } from './storage.js';
import { formatDate } from './utils.js';

// ── Build a weather card ──────────────────────────────────────
export function buildWeatherCard(weather, onFavoriteToggle) {
  const card = document.createElement('div');
  card.className = 'weather-card';
  card.dataset.city = weather.city;

  // Header row
  const header = document.createElement('div');
  header.className = 'card-header';

  const cityName = document.createElement('h2');
  cityName.className   = 'card-city';
  cityName.textContent = weather.city;

  const favBtn = document.createElement('button');
  favBtn.className   = 'fav-btn';
  favBtn.dataset.city = weather.city;
  favBtn.dataset.action = 'toggle-fav';
  updateFavBtn(favBtn, weather);

  header.appendChild(cityName);
  header.appendChild(favBtn);

  // Timezone
  const tz = document.createElement('p');
  tz.className   = 'card-tz';
  tz.textContent = weather.timezone;

  // Main weather display
  const main = document.createElement('div');
  main.className = 'card-main';

  const emoji = document.createElement('span');
  emoji.className   = 'weather-emoji';
  emoji.textContent = weather.emoji;
  emoji.setAttribute('aria-label', weather.label);
  emoji.setAttribute('role', 'img');

  const tempWrap = document.createElement('div');
  const temp     = document.createElement('span');
  temp.className   = 'card-temp';
  temp.textContent = `${weather.temperature}°C`;

  const desc = document.createElement('span');
  desc.className   = 'card-desc';
  desc.textContent = weather.label;

  tempWrap.appendChild(temp);
  tempWrap.appendChild(desc);
  main.appendChild(emoji);
  main.appendChild(tempWrap);

  // Stats grid
  const stats = document.createElement('div');
  stats.className = 'card-stats';

  [
    ['💧', 'Humidity',   `${weather.humidity}%`],
    ['💨', 'Wind',       `${weather.windSpeed} km/h`],
    ['🌡️', 'Feels like', `${weather.feelsLike}°C`],
    ['🕐', 'Updated',    new Date(weather.fetchedAt).toLocaleTimeString()],
  ].forEach(([icon, label, value]) => {
    const stat = document.createElement('div');
    stat.className = 'stat-item';

    const statIcon = document.createElement('span');
    statIcon.textContent = icon;
    statIcon.setAttribute('aria-hidden', 'true');

    const statLabel = document.createElement('span');
    statLabel.className   = 'stat-label';
    statLabel.textContent = label;

    const statVal = document.createElement('span');
    statVal.className   = 'stat-value';
    statVal.textContent = value;

    stat.appendChild(statIcon);
    stat.appendChild(statLabel);
    stat.appendChild(statVal);
    stats.appendChild(stat);
  });

  // 5-day forecast
  const forecastSection = document.createElement('div');
  forecastSection.className = 'forecast-section';

  const forecastTitle = document.createElement('h3');
  forecastTitle.className   = 'forecast-title';
  forecastTitle.textContent = '5-Day Forecast';

  const forecastRow = document.createElement('div');
  forecastRow.className = 'forecast-row';

  weather.forecast.slice(0, 5).forEach(day => {
    const dayEl = document.createElement('div');
    dayEl.className = 'forecast-day';

    const dateEl = document.createElement('div');
    dateEl.className   = 'forecast-date';
    dateEl.textContent = formatDate(day.date);

    const iconEl = document.createElement('div');
    iconEl.className   = 'forecast-icon';
    iconEl.textContent = day.desc.emoji;
    iconEl.setAttribute('aria-label', day.desc.label);

    const tempRangeEl = document.createElement('div');
    tempRangeEl.className = 'forecast-temp';

    const maxEl = document.createElement('span');
    maxEl.className   = 'temp-max';
    maxEl.textContent = `${Math.round(day.maxTemp)}°`;

    const minEl = document.createElement('span');
    minEl.className   = 'temp-min';
    minEl.textContent = `${Math.round(day.minTemp)}°`;

    tempRangeEl.appendChild(maxEl);
    tempRangeEl.appendChild(minEl);
    dayEl.appendChild(dateEl);
    dayEl.appendChild(iconEl);
    dayEl.appendChild(tempRangeEl);
    forecastRow.appendChild(dayEl);
  });

  forecastSection.appendChild(forecastTitle);
  forecastSection.appendChild(forecastRow);

  card.appendChild(header);
  card.appendChild(tz);
  card.appendChild(main);
  card.appendChild(stats);
  card.appendChild(forecastSection);

  // Event delegation handled in app.js via bubbling
  return card;
}

export function updateFavBtn(btn, weather) {
  const faved = isFavorite(weather.city);
  btn.textContent = faved ? '★' : '☆';
  btn.title       = faved ? 'Remove from favorites' : 'Add to favorites';
  btn.setAttribute('aria-label', faved ? `Remove ${weather.city} from favorites` : `Add ${weather.city} to favorites`);
  btn.classList.toggle('faved', faved);
}

// ── Build the favorites sidebar list ─────────────────────────
export function buildFavoriteItem(fav) {
  const li = document.createElement('li');
  li.className    = 'fav-item';
  li.dataset.name = fav.name;
  li.dataset.lat  = fav.lat;
  li.dataset.lon  = fav.lon;
  li.setAttribute('role', 'option');
  li.setAttribute('tabindex', '0');
  li.setAttribute('aria-label', `Load weather for ${fav.name}`);

  const nameEl = document.createElement('span');
  nameEl.className   = 'fav-name';
  nameEl.textContent = fav.name;

  const removeBtn = document.createElement('button');
  removeBtn.className     = 'fav-remove';
  removeBtn.textContent   = '×';
  removeBtn.dataset.action = 'remove-fav';
  removeBtn.dataset.name   = fav.name;
  removeBtn.setAttribute('aria-label', `Remove ${fav.name} from favorites`);

  li.appendChild(nameEl);
  li.appendChild(removeBtn);
  return li;
}

// ── Spinner helper ────────────────────────────────────────────
export function createSpinner(text = 'Loading…') {
  const wrap = document.createElement('div');
  wrap.className = 'spinner-wrap';

  const spin = document.createElement('div');
  spin.className = 'spinner';
  spin.setAttribute('aria-hidden', 'true');

  const label = document.createElement('p');
  label.className   = 'spinner-label';
  label.textContent = text;

  wrap.appendChild(spin);
  wrap.appendChild(label);
  return wrap;
}

// ── Error card helper ─────────────────────────────────────────
export function createErrorCard(message, onRetry) {
  const div = document.createElement('div');
  div.className = 'error-card';
  div.setAttribute('role', 'alert');

  const icon = document.createElement('span');
  icon.textContent = '⚠️';
  icon.setAttribute('aria-hidden', 'true');

  const msg = document.createElement('p');
  msg.className   = 'error-msg';
  msg.textContent = message;

  div.appendChild(icon);
  div.appendChild(msg);

  if (onRetry) {
    const btn = document.createElement('button');
    btn.className   = 'retry-btn';
    btn.textContent = '↺ Retry';
    btn.addEventListener('click', onRetry);
    div.appendChild(btn);
  }

  return div;
}
