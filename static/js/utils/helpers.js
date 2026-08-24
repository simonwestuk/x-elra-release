/**
 * General utility functions for X-ELRA frontend
 *
 * These are pure utility functions with no DOM or business logic dependencies.
 */

/**
 * Escape HTML special characters to prevent XSS
 * @param {string} value - String to escape
 * @returns {string} Escaped string safe for HTML insertion
 */
export const escapeHtml = (value = '') => String(value)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#39;');

/**
 * Format a day delta into a human-readable string
 * @param {number} delta - Number of days (can be fractional)
 * @returns {string} Human-readable time description
 */
export function formatDays(delta) {
  if (!Number.isFinite(delta)) return 'no recent';
  if (delta >= 1) {
    const rounded = Math.round(delta);
    return `${rounded} day${rounded === 1 ? '' : 's'}`;
  }
  const hours = Math.round(delta * 24);
  if (hours >= 1) {
    return `${hours} hour${hours === 1 ? '' : 's'}`;
  }
  return 'less than an hour';
}

/**
 * Format seconds into MM:SS format
 * @param {number} seconds - Total seconds
 * @returns {string} Formatted time string
 */
export function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

/**
 * Extract error message from various error types
 * @param {Error|Object} err - Error object
 * @param {string} fallback - Fallback message if extraction fails
 * @returns {string} Error message
 */
export function errorMessage(err, fallback) {
  // Check for ApiError with message property
  if (err && err.constructor && err.constructor.name === 'ApiError' && err.message) {
    return err.message;
  }
  if (err && typeof err.message === 'string' && err.message.trim()) {
    return err.message.trim();
  }
  return fallback;
}

/**
 * Debounce a function call
 * @param {Function} fn - Function to debounce
 * @param {number} delay - Delay in milliseconds
 * @returns {Function} Debounced function
 */
export function debounce(fn, delay) {
  let timeoutId = null;
  return function (...args) {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}

/**
 * Throttle a function call
 * @param {Function} fn - Function to throttle
 * @param {number} limit - Minimum time between calls in milliseconds
 * @returns {Function} Throttled function
 */
export function throttle(fn, limit) {
  let lastCall = 0;
  return function (...args) {
    const now = Date.now();
    if (now - lastCall >= limit) {
      lastCall = now;
      return fn.apply(this, args);
    }
  };
}

/**
 * Generate a random rotation value for visual variety
 * @param {number} range - Range of rotation in degrees (default ±2)
 * @returns {string} CSS rotation value
 */
export function randRot(range = 2) {
  return `${(Math.random() * range * 2 - range).toFixed(2)}deg`;
}

/**
 * Parse a URL query parameter
 * @param {string} name - Parameter name
 * @returns {string|null} Parameter value or null
 */
export function getQueryParam(name) {
  const url = new URL(window.location.href);
  return url.searchParams.get(name);
}

/**
 * Check if a value is a non-empty string
 * @param {*} value - Value to check
 * @returns {boolean} True if non-empty string
 */
export function isNonEmptyString(value) {
  return typeof value === 'string' && value.trim().length > 0;
}

/**
 * Clamp a number between min and max
 * @param {number} value - Value to clamp
 * @param {number} min - Minimum value
 * @param {number} max - Maximum value
 * @returns {number} Clamped value
 */
export function clamp(value, min, max) {
  return Math.min(Math.max(value, min), max);
}

export default {
  escapeHtml,
  formatDays,
  formatTime,
  errorMessage,
  debounce,
  throttle,
  randRot,
  getQueryParam,
  isNonEmptyString,
  clamp,
};
