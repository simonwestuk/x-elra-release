/**
 * Lesson Service for X-ELRA
 *
 * Handles lesson iframe preparation, live code injection,
 * and lesson URL resolution.
 */

// Lesson content configuration
export const LESSON_STYLE_HREF = '/static/css/lesson-content.css';
export const LESSON_SCRIPT_SRC = '/static/js/xelra-md-live.js';

// Get the live meta element from the parent document
const getLiveMeta = () => document.querySelector('meta[name="xelra-md-live"]');

/**
 * Copy xelra-md-live meta configuration from parent to iframe document
 * @param {Document} doc - The iframe document
 * @returns {HTMLMetaElement|null} The target meta element
 */
export function copyLiveMetaToDoc(doc) {
  if (!doc) return null;
  // Use head if available, otherwise fall back to documentElement for HTML fragments
  const host = doc.head || doc.documentElement;
  if (!host) return null;
  const source = getLiveMeta();
  let target = doc.querySelector('meta[name="xelra-md-live"]');
  if (!target) {
    target = doc.createElement('meta');
    target.setAttribute('name', 'xelra-md-live');
    host.appendChild(target);
  }
  // Clear existing data attributes
  const existingAttrs = Array.from(target.attributes);
  existingAttrs.forEach((attr) => {
    if (attr.name && attr.name.startsWith('data-')) {
      target.removeAttribute(attr.name);
    }
  });
  // Copy from source
  if (source) {
    Array.from(source.attributes).forEach((attr) => {
      if (attr.name && attr.name.startsWith('data-')) {
        target.setAttribute(attr.name, attr.value);
      }
    });
  }
  // Set defaults if not present
  if (!target.hasAttribute('data-engine')) {
    target.setAttribute('data-engine', 'pyodide');
  }
  if (!target.hasAttribute('data-timeout-ms')) {
    target.setAttribute('data-timeout-ms', '7000');
  }
  return target;
}

/**
 * Inject lesson styles into an iframe document
 * @param {Document} doc - The iframe document
 */
export function ensureLessonStyles(doc) {
  if (!doc) return;
  // Use head if available, otherwise fall back to documentElement for HTML fragments
  const host = doc.head || doc.documentElement;
  if (!host) return;
  const existing = doc.querySelector('link[data-xelra-lesson-style="true"]');
  if (existing) return;
  const link = doc.createElement('link');
  link.rel = 'stylesheet';
  link.href = LESSON_STYLE_HREF;
  link.setAttribute('data-xelra-lesson-style', 'true');
  host.appendChild(link);
}

/**
 * Inject xelra-md-live script into an iframe document
 * @param {Document} doc - The iframe document
 */
export function ensureLessonScript(doc) {
  if (!doc) return;
  const existing = doc.querySelector('script[data-xelra-lesson-live="true"]');
  if (existing) {
    // Re-bootstrap if already loaded
    try {
      if (doc.defaultView && doc.defaultView.XelraMdLive && typeof doc.defaultView.XelraMdLive.bootstrap === 'function') {
        doc.defaultView.XelraMdLive.bootstrap(doc);
      }
    } catch (err) {
      console.warn('Failed to re-bootstrap live code in lesson document', err);
    }
    return;
  }
  const host = doc.head || doc.body || doc.documentElement || null;
  if (!host) return;
  const script = doc.createElement('script');
  script.src = LESSON_SCRIPT_SRC;
  script.type = 'text/javascript';
  script.setAttribute('data-xelra-lesson-live', 'true');
  host.appendChild(script);
}

/**
 * Prepare a lesson document with styles, scripts, and meta configuration
 * @param {Document} doc - The iframe document
 */
export function prepareLessonDocument(doc) {
  if (!doc) return;
  const { documentElement, body } = doc;
  if (documentElement) {
    documentElement.classList.add('xelra-lesson-root');
  }
  if (body) {
    body.classList.add('xelra-lesson');
  }
  copyLiveMetaToDoc(doc);
  ensureLessonStyles(doc);
  ensureLessonScript(doc);
}

/**
 * Set an attribute on the live meta element
 * @param {string} name - Attribute name (without 'data-' prefix)
 * @param {*} value - Attribute value
 */
export function setLiveMetaAttr(name, value) {
  const liveMeta = getLiveMeta();
  if (!liveMeta) return;
  const attr = `data-${name}`;
  if (value === undefined || value === null || value === '') {
    liveMeta.removeAttribute(attr);
  } else {
    liveMeta.setAttribute(attr, String(value));
  }
}

/**
 * Resolve a lesson URL to an asset URL
 * @param {string} url - Original lesson URL
 * @returns {string} Resolved asset URL
 */
export function resolveLessonAssetUrl(url) {
  if (!url || typeof url !== 'string') return url;
  if (url.startsWith('../')) return url;
  if (url.startsWith('/content/')) {
    return `../${url.slice(1)}`;
  }
  if (url.startsWith('content/')) {
    return `../${url}`;
  }
  return url;
}

/**
 * Build a URL to load a lesson through the template wrapper
 * @param {string} contentUrl - The resolved lesson content URL
 * @param {string} learnerId - The learner ID for telemetry
 * @param {string} itemId - The item ID for telemetry
 * @returns {string} The template wrapper URL with query params
 */
export function buildLessonTemplateUrl(contentUrl, learnerId, itemId) {
  const templatePath = './lesson.html';
  const params = new URLSearchParams();
  params.set('url', contentUrl);
  if (learnerId) params.set('learner_id', learnerId);
  if (itemId) params.set('item_id', itemId);
  params.set('session_id', `session-${Date.now()}`);
  params.set('attempt_id', `attempt-${Date.now()}`);
  return `${templatePath}?${params.toString()}`;
}

/**
 * Bind load event to lesson viewer iframe
 * @param {string} viewerId - ID of the lesson viewer iframe element
 */
export function bindLessonViewer(viewerId = 'lessonViewer') {
  const viewer = document.getElementById(viewerId);
  if (!viewer) return;
  viewer.addEventListener('load', () => {
    try {
      const doc = viewer.contentDocument || viewer.contentWindow?.document || null;
      if (!doc || doc.readyState === 'uninitialized') return;
      if (doc.location && doc.location.href && doc.location.href === 'about:blank') return;
      prepareLessonDocument(doc);
    } catch (err) {
      console.warn('Failed to prepare lesson iframe document', err);
    }
  });
}

export default {
  LESSON_STYLE_HREF,
  LESSON_SCRIPT_SRC,
  copyLiveMetaToDoc,
  ensureLessonStyles,
  ensureLessonScript,
  prepareLessonDocument,
  setLiveMetaAttr,
  resolveLessonAssetUrl,
  buildLessonTemplateUrl,
  bindLessonViewer,
};
