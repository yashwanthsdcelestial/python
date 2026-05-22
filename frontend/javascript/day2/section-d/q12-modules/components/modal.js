// components/modal.js — Default export: Modal class (loaded via dynamic import)

export default class Modal {
  constructor({ title, content, onConfirm, onCancel } = {}) {
    this.title     = title;
    this.content   = content;
    this.onConfirm = onConfirm || (() => {});
    this.onCancel  = onCancel  || (() => {});
    this._backdrop = null;
  }

  open() {
    if (this._backdrop) return;

    const backdrop = document.createElement('div');
    backdrop.style.cssText =
      'position:fixed;inset:0;background:rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;z-index:999';

    const modal = document.createElement('div');
    modal.style.cssText =
      'background:white;border-radius:12px;padding:1.5rem;width:90%;max-width:400px;box-shadow:0 8px 40px rgba(0,0,0,.2)';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-labelledby', 'dyn-modal-title');

    modal.innerHTML = `
      <h3 id="dyn-modal-title" style="margin-bottom:.75rem">${this.title}</h3>
      <p style="color:#6b7280;font-size:14px;margin-bottom:1.25rem">${this.content}</p>
      <div style="display:flex;gap:8px;justify-content:flex-end">
        <button id="modal-cancel" style="padding:8px 16px;border:1px solid #d1d5db;border-radius:7px;background:white;cursor:pointer">Cancel</button>
        <button id="modal-confirm" style="padding:8px 16px;border:none;border-radius:7px;background:#2563eb;color:white;cursor:pointer">Confirm</button>
      </div>
    `;

    backdrop.appendChild(modal);
    document.body.appendChild(backdrop);
    this._backdrop = backdrop;

    modal.querySelector('#modal-confirm').addEventListener('click', () => { this.onConfirm(); this.close(); });
    modal.querySelector('#modal-cancel').addEventListener('click',  () => { this.onCancel();  this.close(); });
    backdrop.addEventListener('click', e => { if (e.target === backdrop) this.close(); });
    document.addEventListener('keydown', this._onKeyDown = e => { if (e.key === 'Escape') this.close(); });
    modal.querySelector('#modal-confirm').focus();
  }

  close() {
    if (this._backdrop) {
      this._backdrop.remove();
      this._backdrop = null;
      document.removeEventListener('keydown', this._onKeyDown);
    }
  }
}
