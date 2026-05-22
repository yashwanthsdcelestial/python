// validators.js — Named exports for all validation utilities

export function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function validatePhone(phone) {
  return /^\d{10}$/.test(phone.replace(/\D/g, ''));
}

export function validatePassword(password) {
  return (
    password.length >= 8 &&
    /[A-Z]/.test(password) &&
    /[a-z]/.test(password) &&
    /[0-9]/.test(password) &&
    /[!@#$%^&*]/.test(password)
  );
}

export function validateName(name) {
  return name.trim().length >= 2 && /^[a-zA-Z\s]+$/.test(name);
}

export function validateAge(age) {
  const n = Number(age);
  return Number.isInteger(n) && n >= 18 && n <= 120;
}
