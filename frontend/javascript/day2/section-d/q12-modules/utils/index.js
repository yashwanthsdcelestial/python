// utils/index.js — Barrel file re-exporting everything
// Consumers can import selectively: import { validateEmail } from './utils'
// Only the imported functions get bundled (tree-shaking friendly)

export * from './validators.js';
export * from './formatters.js';
