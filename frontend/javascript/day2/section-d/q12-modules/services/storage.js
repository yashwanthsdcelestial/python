// services/storage.js — Default export: StorageService class

export default class StorageService {
  constructor(prefix = 'app') {
    this.prefix = prefix + ':';
  }

  _key(k)       { return this.prefix + k; }
  set(k, v)     { localStorage.setItem(this._key(k), JSON.stringify(v)); }
  get(k)        { try { return JSON.parse(localStorage.getItem(this._key(k))); } catch { return null; } }
  remove(k)     { localStorage.removeItem(this._key(k)); }
  has(k)        { return localStorage.getItem(this._key(k)) !== null; }
  clear()       { Object.keys(localStorage).filter(k => k.startsWith(this.prefix)).forEach(k => localStorage.removeItem(k)); }
}
