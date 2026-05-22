// services/api.js — Default export: ApiService class

export default class ApiService {
  constructor(baseURL) {
    this.baseURL = baseURL.replace(/\/$/, '');
  }

  async _request(method, path, body) {
    const options = {
      method,
      headers: { 'Content-Type': 'application/json' },
    };
    if (body) options.body = JSON.stringify(body);

    const res = await fetch(this.baseURL + path, options);
    if (!res.ok) throw new Error(`HTTP ${res.status} — ${res.statusText}`);
    return res.json();
  }

  get(path)             { return this._request('GET',    path); }
  post(path, body)      { return this._request('POST',   path, body); }
  put(path, body)       { return this._request('PUT',    path, body); }
  delete(path)          { return this._request('DELETE', path); }
}
