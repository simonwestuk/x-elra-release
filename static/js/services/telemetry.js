/**
 * Telemetry Service for X-ELRA
 *
 * Handles telemetry payload building and queuing.
 * Note: Consent management and UI are handled in standalone.js
 * as they require DOM access.
 */

import { api, ApiError } from './api.js';
import { store } from './store.js';

// Global telemetry state (shared via window for legacy compatibility)
window.__XELRA_LAST_STRATEGY = window.__XELRA_LAST_STRATEGY || null;
window.__XELRA_LAST_ARM = window.__XELRA_LAST_ARM || null;
window.__XELRA_LAST_TELEMETRY = window.__XELRA_LAST_TELEMETRY || null;
window.__XELRA_NEXTUP_TELEMETRY = window.__XELRA_NEXTUP_TELEMETRY || null;
window.__XELRA_POLICY_VERSION = window.__XELRA_POLICY_VERSION || null;
window.__XELRA_POLICY_STACK = window.__XELRA_POLICY_STACK || [];

/**
 * Build a base telemetry payload from meta and learner ID
 * @param {Object} meta - Telemetry metadata (user_id, arm_key, etc.)
 * @param {string} learnerId - Learner ID
 * @param {Object} extra - Additional payload fields
 * @returns {Object|null} Telemetry payload or null if invalid
 */
export function buildTelemetryPayload(meta, learnerId, extra = {}) {
  if (!learnerId) return null;
  const payload = {
    learner_id: learnerId,
    ...extra,
  };
  if (meta && typeof meta === 'object') {
    if (meta.user_id !== undefined && payload.user_id === undefined) {
      payload.user_id = meta.user_id;
    }
    if (meta.arm_key && payload.arm_key === undefined) {
      payload.arm_key = meta.arm_key;
    }
    if (payload.arm === undefined && meta.arm_key) {
      payload.arm = meta.arm_key;
    }
    if (meta.policy_version && payload.policy_version === undefined) {
      payload.policy_version = meta.policy_version;
    }
    if (meta.schema_version && payload.schema_version === undefined) {
      payload.schema_version = meta.schema_version;
    }
    if (meta.request_id && payload.request_id === undefined) {
      payload.request_id = meta.request_id;
    }
  }
  return payload;
}

/**
 * Create a telemetry payload from context object
 * @param {Object} context - Context with meta, learnerId, itemId, etc.
 * @param {Object} extra - Additional fields to include
 * @returns {Object|null} Telemetry payload
 */
export function createTelemetryPayload(context = {}, extra = {}) {
  const meta = context.meta || window.__XELRA_LAST_TELEMETRY || null;
  const learnerId = context.learnerId || store.learner || null;
  const requestId = extra.request_id !== undefined
    ? extra.request_id
    : (context.requestId ?? (meta && meta.request_id));

  const payload = buildTelemetryPayload(meta, learnerId, {
    item_id: context.itemId ?? extra.item_id ?? null,
    rank: context.rank ?? extra.rank ?? null,
    strategy: context.strategy ?? extra.strategy ?? window.__XELRA_LAST_STRATEGY ?? null,
    arm: context.arm ?? extra.arm ?? window.__XELRA_LAST_ARM ?? (meta && meta.arm_key) ?? null,
    policy_version: context.policyVersion ?? extra.policy_version ?? window.__XELRA_POLICY_VERSION ?? (meta && meta.policy_version) ?? null,
    course_id: context.courseId ?? extra.course_id ?? null,
    request_id: requestId,
    ...extra,
  });
  return payload;
}

/**
 * Telemetry queue and processing
 * Note: The actual queue processing requires consent check which
 * is handled in standalone.js. This provides the queue interface.
 */
class TelemetryQueue {
  constructor() {
    this.queue = [];
    this.processing = false;
    this.consentChecker = null; // Set by standalone.js
  }

  /**
   * Set the consent checker function
   * @param {Function} checker - Async function that returns true if consent granted
   */
  setConsentChecker(checker) {
    this.consentChecker = checker;
  }

  /**
   * Add an event to the queue
   * @param {string} endpoint - API endpoint
   * @param {Object} payload - Telemetry payload
   */
  enqueue(endpoint, payload) {
    if (!payload) return;
    this.queue.push({ endpoint, payload });
    this.process();
  }

  /**
   * Process the queue (sends events if consent granted)
   */
  async process() {
    if (this.processing) return;
    const learnerId = store.learner;
    if (!learnerId) return;

    // Check consent if checker is set
    if (this.consentChecker) {
      const ok = await this.consentChecker(learnerId);
      if (!ok) return;
    }

    this.processing = true;
    try {
      while (this.queue.length) {
        const evt = this.queue[0];
        try {
          await api(evt.endpoint, { method: 'POST', body: JSON.stringify(evt.payload) });
          this.queue.shift();
        } catch (err) {
          console.error('Telemetry dispatch failed', err);
          if (err instanceof ApiError && err.status >= 400 && err.status < 500) {
            this.queue.shift();
            continue;
          }
          break;
        }
      }
    } finally {
      this.processing = false;
    }
  }

  /**
   * Get current queue length
   * @returns {number} Queue length
   */
  get length() {
    return this.queue.length;
  }
}

// Singleton queue instance
export const telemetryQueue = new TelemetryQueue();

/**
 * Post telemetry event (legacy interface)
 * @param {string} endpoint - API endpoint
 * @param {Object} context - Telemetry context
 * @param {Object} extra - Additional fields
 */
export function postTelemetry(endpoint, context, extra = {}) {
  const { items: extraItems, ...restExtra } = extra || {};
  let payload = createTelemetryPayload(context, restExtra);
  if (!payload) return;

  if (endpoint === '/v1/telemetry/impression') {
    const {
      item_id,
      rank,
      strategy,
      arm,
      course_id,
      request_id,
      source,
      ...rest
    } = payload;

    const itemsSource = Array.isArray(extraItems) ? extraItems : [
      {
        item_id,
        rank,
        strategy,
        arm,
        course_id,
        request_id,
        source,
      },
    ];

    const items = itemsSource
      .filter((item) => item && item.item_id)
      .map((item) => {
        const normalized = { item_id: item.item_id };
        if (item.rank != null) normalized.rank = item.rank;
        const itemSource = item.source ?? source;
        if (itemSource != null) normalized.source = itemSource;
        if (item.strategy != null) normalized.strategy = item.strategy;
        if (item.arm != null) normalized.arm = item.arm;
        if (item.course_id != null) normalized.course_id = item.course_id;
        if (item.request_id != null) normalized.request_id = item.request_id;
        return normalized;
      });

    if (!items.length) return;
    payload = { ...rest, items };
  }

  telemetryQueue.enqueue(endpoint, payload);
}

/**
 * Track fired impressions to avoid duplicates
 */
export const firedImpressions = new Set();

/**
 * Record an impression if not already fired
 * @param {Object} context - Telemetry context with itemId
 * @returns {boolean} True if impression was recorded
 */
export function recordImpression(context) {
  if (!context || !context.itemId) return false;
  const key = `${context.itemId}::${context.rank ?? 'X'}`;
  if (firedImpressions.has(key)) return false;
  firedImpressions.add(key);
  postTelemetry('/v1/telemetry/impression', context);
  return true;
}

export default {
  buildTelemetryPayload,
  createTelemetryPayload,
  telemetryQueue,
  postTelemetry,
  firedImpressions,
  recordImpression,
};
