export const CONFIG = {
  PIS_URL: 'https://example.com/pis.pdf',
  RECS_TOP_K: 3,
  // Use same-origin if served via http(s); otherwise default to dev API
  API_BASE: (location.protocol === 'http:' || location.protocol === 'https:') ? location.origin : location.origin
};

export class ApiError extends Error {
  constructor(message, { status, statusText, data } = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.statusText = statusText;
    this.data = data;
  }
}

export async function api(path, opts = {}) {
  const isAbs = /^https?:\/\//i.test(path);
  const url = isAbs ? path : (CONFIG.API_BASE + path);
  const corsAlert = document.getElementById('corsAlert');
  if (corsAlert) corsAlert.style.display = 'none';
  try {
    const res = await fetch(url, { headers: { 'Content-Type': 'application/json' }, mode: 'cors', ...opts });
    if (!res.ok) {
      let data = null;
      let message = res.statusText ? `${res.statusText} (${res.status})` : `Request failed with status ${res.status}`;
      const contentType = res.headers.get('content-type') || '';
      let rawText = '';
      try {
        rawText = await res.text();
      } catch (_) {
        rawText = '';
      }
      if (contentType.includes('application/json')) {
        try {
          if (rawText) data = JSON.parse(rawText);
        } catch (_) {
          // leave data as null if JSON parsing fails
        }
      } else if (rawText && rawText.trim()) {
        message = rawText.trim();
      }
      if (!contentType.includes('application/json') && !rawText && res.statusText) {
        message = res.statusText;
      }
      if (data && typeof data === 'object') {
        const detail = data.detail || data.message || data.error;
        if (typeof detail === 'string' && detail.trim()) {
          message = detail.trim();
        } else if (Array.isArray(data.errors) && data.errors.length) {
          const first = data.errors[0];
          if (typeof first === 'string' && first.trim()) {
            message = first.trim();
          } else if (first && typeof first.message === 'string' && first.message.trim()) {
            message = first.message.trim();
          }
        }
      } else if (rawText && rawText.trim() && !message) {
        message = rawText.trim();
      }
      throw new ApiError(message, { status: res.status, statusText: res.statusText, data: data ?? rawText });
    }
    if (res.status === 204) return null;
    const contentType = res.headers.get('content-type') || '';
    const text = await res.text();
    if (contentType.includes('application/json')) {
      return text ? JSON.parse(text) : null;
    }
    return text;
  } catch (e) {
    if (e instanceof ApiError) throw e;
    if (corsAlert && e instanceof TypeError) corsAlert.style.display = 'block';
    throw e;
  }
}

export function setHTMLWithScripts(el, html) {
  el.innerHTML = html;
  el.querySelectorAll('script').forEach(old => {
    const s = document.createElement('script');
    if (old.src) s.src = old.src;
    s.textContent = old.textContent;
    old.parentNode.replaceChild(s, old);
  });
}
