// api.js — Weather API module (ES6 module)
// Uses Open-Meteo (free, no API key needed)

const GEO_URL     = 'https://geocoding-api.open-meteo.com/v1/search';
const WEATHER_URL = 'https://api.open-meteo.com/v1/forecast';

/**
 * searchCity(name) → array of geocoding results
 * Each result has: { name, admin1, country, latitude, longitude, ... }
 */
export async function searchCity(name) {
  const res = await fetch(
    `${GEO_URL}?name=${encodeURIComponent(name)}&count=5&language=en&format=json`
  );
  if (!res.ok) throw new Error(`Geocoding failed (HTTP ${res.status})`);
  const data = await res.json();
  return data.results || [];
}

/**
 * fetchWeather(lat, lon, cityName) → normalized WeatherData object
 */
export async function fetchWeather(lat, lon, cityName) {
  if (lat == null || lon == null) throw new Error('Invalid coordinates');

  const params = new URLSearchParams({
    latitude:        lat,
    longitude:       lon,
    current_weather: true,
    hourly:          'relative_humidity_2m,apparent_temperature',
    daily:           'temperature_2m_max,temperature_2m_min,weathercode',
    wind_speed_unit: 'kmh',
    timezone:        'auto',
    forecast_days:   5,
  });

  const res = await fetch(`${WEATHER_URL}?${params}`);
  if (!res.ok) throw new Error(`Weather API failed (HTTP ${res.status})`);

  const raw = await res.json();

  // Validate expected fields exist
  if (!raw.current_weather) throw new Error('Unexpected API response format');

  return normalizeWeather(raw, cityName || 'Unknown');
}

// ── WMO weather code → label + emoji ─────────────────────────
function describeWeatherCode(code) {
  const map = {
    0:  ['Clear sky',          '☀️'],
    1:  ['Mainly clear',       '🌤️'],
    2:  ['Partly cloudy',      '⛅'],
    3:  ['Overcast',           '☁️'],
    45: ['Foggy',              '🌫️'],
    48: ['Icy fog',            '🌫️'],
    51: ['Light drizzle',      '🌦️'],
    53: ['Drizzle',            '🌦️'],
    55: ['Heavy drizzle',      '🌧️'],
    61: ['Light rain',         '🌧️'],
    63: ['Rain',               '🌧️'],
    65: ['Heavy rain',         '🌧️'],
    71: ['Light snow',         '🌨️'],
    73: ['Snow',               '❄️'],
    75: ['Heavy snow',         '❄️'],
    80: ['Light showers',      '🌦️'],
    81: ['Showers',            '🌧️'],
    82: ['Heavy showers',      '🌧️'],
    95: ['Thunderstorm',       '⛈️'],
    96: ['Thunderstorm + hail','⛈️'],
    99: ['Heavy thunderstorm', '⛈️'],
  };
  const entry = map[code] ?? ['Unknown', '🌡️'];
  return { label: entry[0], emoji: entry[1] };
}

function normalizeWeather(raw, cityName) {
  const cw = raw.current_weather;

  // Find the closest hourly index to now for humidity / feels-like
  const now       = new Date();
  const hourTimes = raw.hourly?.time ?? [];
  let   hourIndex = hourTimes.findIndex(t => new Date(t) >= now) - 1;
  if (hourIndex < 0) hourIndex = 0;

  const humidity  = raw.hourly?.relative_humidity_2m?.[hourIndex]  ?? '--';
  const feelsLike = raw.hourly?.apparent_temperature?.[hourIndex]   ?? '--';

  // 5-day forecast
  const forecast = (raw.daily?.time ?? []).map((date, i) => ({
    date,
    maxTemp: raw.daily.temperature_2m_max?.[i] ?? '--',
    minTemp: raw.daily.temperature_2m_min?.[i] ?? '--',
    desc:    describeWeatherCode(raw.daily.weathercode?.[i] ?? 0),
  }));

  const desc = describeWeatherCode(cw.weathercode ?? 0);

  return {
    city:        String(cityName),          // always a string
    lat:         raw.latitude,
    lon:         raw.longitude,
    timezone:    raw.timezone ?? '',
    temperature: Math.round(cw.temperature ?? 0),
    feelsLike:   typeof feelsLike === 'number' ? Math.round(feelsLike) : feelsLike,
    windSpeed:   Math.round(cw.windspeed ?? 0),
    humidity,
    weatherCode: cw.weathercode,
    label:       desc.label,
    emoji:       desc.emoji,
    isDay:       cw.is_day === 1,
    fetchedAt:   new Date().toISOString(),
    forecast,
  };
}
