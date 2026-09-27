import { CONFIG, api, setHTMLWithScripts, ApiError } from '../services/api.js';
import { store, hasCelebrated, unmarkCelebrated, isLoginInProgress, wasConsentJustGranted, setConsentJustGranted } from '../services/store.js';
import { signOut, initLogin } from '../services/auth.js';
import { showToast, showLoading, hideLoading, hideBigToast } from '../ui/ui.js';
import { celebrateSkill, renderCourseComplete } from '../ui/celebration.js';
import { processARLCycleActions } from '../ui/arl-actions.js';
import {
  parseFeedbackNote,
  openNoteModal,
  initNoteModal,
} from '../ui/modals.js';

// Extracted modules
import { escapeHtml, formatDays, errorMessage, randRot } from '../utils/helpers.js';
import {
  ARM_MAP,
  POLICY_DETAILS,
  POLICY_TITLE_BY_ID,
  POLICY_SNIPPETS,
  BASELINE_IDS,
  BASELINE_GUARDRAILS,
  MODEL_SIGNAL_DESCRIPTORS,
  resolvePolicyList,
  describePolicy,
  policyTooltipText,
  policySentenceSummary,
  policyDetailListText,
  policyShortSummary,
  policyTagLabel,
  describeModelSignal,
  getArmConfig,
} from '../config/policy.js';
import {
  buildTelemetryPayload,
  createTelemetryPayload,
  telemetryQueue,
  postTelemetry,
  firedImpressions,
} from '../services/telemetry.js';
import {
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
} from '../services/lesson.js';

window.__XELRA_FOCUS_SKILL_ID = window.__XELRA_FOCUS_SKILL_ID || null;

// Telemetry consent state
const telemetryConsentState = {
  known: false,
  granted: false,
  checking: false,
  waiters: [],
};

const flushConsentWaiters = (value) => {
  const pending = telemetryConsentState.waiters.splice(0);
  pending.forEach((fn) => {
    try {
      fn(value);
    } catch (err) {
      console.error('Consent waiter failed', err);
    }
  });
};

let featureFlags = {
  explanations: true,
  sentiment: true,
  liveCode: false,
  pilotMode: false,
};

// Arm-specific feature visibility (updated by applyArm)
let armFeatures = {
  allowExplain: true,
  allowSentiment: true,
  allowRegulatoryMode: true,
};

let currentExplainStart = null;
let currentExplainContext = null;
let explainDrawerInstance = null;
let currentLesson = { item: null, context: null, url: null, assetUrl: null };
let lastFocusElement = null;

// Session activity tracker with live "system thinking" messages
const sessionActivity = {
  completions: 0,
  reflections: 0,
  codeRuns: 0,
  ratings: 0,
  startTime: Date.now(),
};

// Activity message templates - feels like the system is thinking/responding
const ACTIVITY_MESSAGES = {
  idle: [
    'Listening...',
    'Ready to help',
    'Watching your progress',
  ],
  completions: [
    'Got it — updating your learning path...',
    'Nice progress! Recalculating next steps...',
    'Marked complete — finding what\'s next...',
    'Progress logged — adjusting recommendations...',
  ],
  ratings: [
    'Feedback received — learning your preferences...',
    'Thanks! Tuning recommendations...',
    'Rating noted — improving suggestions...',
    'Your input helps me help you better',
  ],
  reflections: [
    'Reflection saved — understanding your journey...',
    'Noted! Using this to guide your path...',
    'Insight captured — adapting to your needs...',
  ],
  codeRuns: [
    'Code executed — tracking your practice...',
    'Run logged — monitoring your coding...',
    'Practice noted — watching your skills grow...',
  ],
};

let activityMessageQueue = [];
let activityDisplayTimeout = null;
let currentActivityIndex = 0;

const trackActivity = (type) => {
  if (sessionActivity[type] !== undefined) {
    sessionActivity[type]++;
  }
  // Add a contextual message to the queue
  const messages = ACTIVITY_MESSAGES[type];
  if (messages && messages.length > 0) {
    const msg = messages[Math.floor(Math.random() * messages.length)];
    showActivityMessage(msg);
  }
};

const showActivityMessage = (message) => {
  const textElements = [
    document.getElementById('activityText'),
    document.getElementById('activityTextLesson'),
    document.getElementById('navActivityText')
  ].filter(Boolean);

  const dots = [
    document.querySelector('#systemActivityIndicator .activity-dot'),
    document.querySelector('#systemActivityIndicatorLesson .activity-dot'),
    document.querySelector('#navActivityIndicator .activity-dot')
  ].filter(Boolean);

  // Flash the activity dot
  dots.forEach(dot => {
    dot.classList.add('activity-pulse');
    setTimeout(() => dot.classList.remove('activity-pulse'), 600);
  });

  // Show the message with typing effect
  textElements.forEach(el => {
    el.classList.add('activity-typing');
    el.textContent = message;
  });

  // Clear any pending timeout
  if (activityDisplayTimeout) {
    clearTimeout(activityDisplayTimeout);
  }

  // After a delay, show a summary or idle message
  activityDisplayTimeout = setTimeout(() => {
    textElements.forEach(el => el.classList.remove('activity-typing'));
    showActivitySummary();
  }, 4000);
};

const showActivitySummary = () => {
  const textElements = [
    document.getElementById('activityText'),
    document.getElementById('activityTextLesson'),
    document.getElementById('navActivityText')
  ].filter(Boolean);

  const total = sessionActivity.completions + sessionActivity.reflections +
                sessionActivity.codeRuns + sessionActivity.ratings;

  let summaryText;
  if (total === 0) {
    summaryText = ACTIVITY_MESSAGES.idle[Math.floor(Math.random() * ACTIVITY_MESSAGES.idle.length)];
  } else if (total === 1) {
    summaryText = 'Adapting to your activity...';
  } else if (total < 5) {
    summaryText = `Learning from ${total} interactions...`;
  } else if (total < 10) {
    summaryText = `Building your learning profile...`;
  } else {
    summaryText = `Personalising based on ${total}+ interactions`;
  }

  textElements.forEach(el => {
    el.textContent = summaryText;
  });
};

async function loadFeatureFlags(){
  try{
    const res = await api('/v1/version');
    const flags = (res && res.feature_flags) || {};
    featureFlags.explanations = flags.explanations !== false;
    const sentimentEnabled = flags.feature_sentiment !== false && flags.infer_sentiment !== false;
    featureFlags.sentiment = sentimentEnabled;
    featureFlags.liveCode = Boolean(res && res.live_code && res.live_code.enabled);
    featureFlags.pilotMode = Boolean(flags.pilot_mode);
    if(res && res.live_code){
      if(res.live_code.engine){
        setLiveMetaAttr('engine', res.live_code.engine);
      }
      if(res.live_code.timeout_ms){
        setLiveMetaAttr('timeout-ms', res.live_code.timeout_ms);
      }
      if(res.live_code.allow_input !== undefined){
        setLiveMetaAttr('allow-input', res.live_code.allow_input);
      }
      const telemetryBase = res.live_code.telemetry_base_url || '/v1/telemetry/live';
      setLiveMetaAttr('telemetry-base-url', telemetryBase);
    } else {
      setLiveMetaAttr('telemetry-base-url', '/v1/telemetry/live');
    }
  }catch(err){
    console.warn('Failed to load version metadata', err);
  }
}

const recordImpression = (context) => {
  if (!context || !context.itemId) return;
  const requestKey = context.requestId || (context.meta && context.meta.request_id) || '';
  const key = `${context.itemId}::${requestKey}`;
  if (firedImpressions.has(key)) return;
  firedImpressions.add(key);
  postTelemetry('/v1/telemetry/impression', context, { source: 'recs' });
};

const buildExplanationHtml = (it, summarySnapshot) => {
  const sections = [];
  const summary = it?.xai && typeof it.xai.summary === 'string' ? it.xai.summary.trim() : '';
  if(summary){
    sections.push(`<p class="mb-2 fw-semibold">${escapeHtml(summary)}</p>`);
  }
  // Guardrail / control-routine rationale is process-level transparency
  // that belongs exclusively to the ARL treatment arm (Table 8: H2 Trust).
  // B1 shows only inference-level feature attribution (SHAP signals below).
  if(armFeatures.allowRegulatoryMode){
    const guardrailFacts = guardrailReasonDetails(window.__XELRA_POLICY_STACK || [], window.__XELRA_LAST_CYCLE);
    if(Array.isArray(guardrailFacts) && guardrailFacts.length){
      const guardrailItems = guardrailFacts
        .map(fact => {
          const reasons = Array.isArray(fact.reasons) && fact.reasons.length
            ? `<ul class="mb-0 ps-3">${fact.reasons.map(reason => `<li>${escapeHtml(reason)}</li>`).join('')}</ul>`
            : '';
          return `<li><strong>${escapeHtml(fact.name)}</strong>${reasons ? `<div class="mt-1">${reasons}</div>` : ''}</li>`;
        })
        .join('');
      sections.push(
        `<div class="mb-3">
          <strong>Why this was recommended</strong>
          <ul class="mb-0 ps-3">${guardrailItems}</ul>
        </div>`
      );
    }
  }
  const primaryInputs = [];
  const modelSignals = [];
  const communitySignals = [];
  const xaiOlm = it?.xai?.olm;
  const focusSkillId = (xaiOlm && Array.isArray(xaiOlm.targets) && xaiOlm.targets.length && xaiOlm.targets[0].skill_id)
    || it.focus_skill_id
    || window.__XELRA_FOCUS_SKILL_ID
    || null;
  const focusSkillObj = summarySnapshot && Array.isArray(summarySnapshot.skills)
    ? summarySnapshot.skills.find(s=> s.id === focusSkillId)
    : null;
  if(focusSkillObj){
    primaryInputs.push({
      category: 'primary',
      text: `Your mastery in ${focusSkillObj.name || focusSkillObj.id}: ${Math.round((focusSkillObj.value || 0)*100)}%`,
    });
  }
  const goalTargets = summarySnapshot && summarySnapshot.goals;
  if(goalTargets && focusSkillObj && goalTargets[focusSkillObj.id] !== undefined){
    primaryInputs.push({
      category: 'primary',
      text: `Your goal for ${focusSkillObj.name || focusSkillObj.id}: ${Math.round(goalTargets[focusSkillObj.id]*100)}%`,
    });
  }
  if(typeof it.rating === 'number'){
    const ratingPercent = Math.round((it.rating / 5) * 100);
    primaryInputs.push({
      category: 'primary',
      text: `Your rating for this resource: ${ratingPercent}% (${it.rating} out of 5)`,
    });
  }
  if(it.comment){
    communitySignals.push({
      category: 'community',
      text: 'You recently added a note about this topic.',
    });
  }
  const lastSent = store.lastSentiment;
  if(lastSent && lastSent.learner === store.learner && lastSent.text){
    communitySignals.push({
      category: 'community',
      text: 'Latest reflection captured for sentiment monitoring.',
    });
  }
  const reasons = Array.isArray(it.reasons) ? it.reasons : [];
  reasons.forEach(item => {
    if(!item) return;
    if(typeof item === 'string'){
      primaryInputs.push({ category: 'model', text: item, key: item });
    }else if(item.type === 'component' && item.component){
      // Component reasons from the recommender (C, CF, P, S)
      modelSignals.push({
        key: item.component,
        value: item.value || 0,
        weight: item.weight || 0,
        contribution: item.contribution || 0,
      });
    }else if(item.category){
      if(item.category === 'model'){
        modelSignals.push({ key: item.key || item.category, value: item.value || 0, weight: 0, contribution: 0 });
      }else if(item.category === 'community'){
        communitySignals.push({ text: item.text || '' });
      }else{
        primaryInputs.push({ text: item.text || '' });
      }
    }
  });
  const formatted = [];
  if(primaryInputs.length){
    const itemsHtml = primaryInputs
      .map(entry => `<li>${escapeHtml(entry.text || '')}</li>`)
      .join('');
    formatted.push(
      `<div class="mb-3">
        <strong>What we looked at</strong>
        <ul class="mb-0 ps-3">${itemsHtml}</ul>
      </div>`
    );
  }
  if(modelSignals.length){
    // Sort by contribution descending so the most influential signal is first
    const sorted = [...modelSignals].sort((a, b) => Math.abs(b.contribution || 0) - Math.abs(a.contribution || 0));
    const totalContrib = sorted.reduce((sum, s) => sum + Math.abs(s.contribution || 0), 0);
    const itemsHtml = sorted
      .map(entry => {
        const details = describeModelSignal(entry.key);
        const weightPct = Math.round((entry.weight || 0) * 100);
        const contribPct = totalContrib > 0
          ? Math.round(Math.abs(entry.contribution || 0) / totalContrib * 100)
          : 0;
        const featureVal = typeof entry.value === 'number' ? Math.round(entry.value * 100) : null;
        let detail = `<strong>${escapeHtml(details.label)}</strong>: weight ${weightPct}%`;
        if (featureVal !== null) {
          detail += `, signal ${featureVal}%`;
        }
        detail += `, contributed ${contribPct}%`;
        detail += ` — ${escapeHtml(details.description)}`;
        return `<li>${detail}</li>`;
      })
      .join('');
    formatted.push(
      `<div class="mb-3">
        <strong>Signals we balanced</strong>
        <ul class="mb-0 ps-3">${itemsHtml}</ul>
      </div>`
    );
  }
  if(communitySignals.length){
    const itemsHtml = communitySignals
      .map(entry => `<li>${escapeHtml(entry.text || '')}</li>`)
      .join('');
    formatted.push(
      `<div class="mb-3">
        <strong>Community signals</strong>
        <ul class="mb-0 ps-3">${itemsHtml}</ul>
      </div>`
    );
  }
  if(formatted.length){
    sections.push(formatted.join(''));
  }
  if(!sections.length && it?.xai){
    sections.push(`<p class="mb-0 text-muted">No detailed explanation was supplied for this recommendation.</p>`);
  }
  if(!sections.length){
    sections.push('<span>No explanation available.</span>');
  }
  return sections.join('');
};

/**
 * Populate the persistent model-explanation card in the OLM panel.
 * Shown for B1 (control_a) only — the arm with allowExplain but NOT
 * allowRegulatoryMode.  Treatment learners receive process-level
 * structured explanations instead; B3 has no explanations at all.
 * Renders the XAI summary text (no signal breakdown).
 */
const updateModelExplainCard = (explanationEntry, panelSuffix = '') => {
  const card = document.getElementById(`modelExplainCard${panelSuffix}`);
  const body = document.getElementById(`modelExplainBody${panelSuffix}`);
  if (!card || !body) return;

  // Hide for treatment (has regulatory mode) and B3 (no explain at all).
  // Only B1 (allowExplain && !allowRegulatoryMode) shows model-level card.
  if (!armFeatures.allowExplain || armFeatures.allowRegulatoryMode) {
    card.style.display = 'none';
    return;
  }

  const xai = explanationEntry?.xai;
  const summary = xai && typeof xai.summary === 'string' ? xai.summary.trim() : '';

  if (!summary) {
    card.style.display = 'none';
    return;
  }

  body.innerHTML = `<p class="mb-0">${escapeHtml(summary)}</p>`;
  card.style.display = 'block';
};

const announceLessonEvent = (message) => {
  const announce = document.getElementById('lessonAnnounce');
  if (!announce) return;
  announce.textContent = '';
  if (message) {
    announce.textContent = message;
  }
};

const clearLessonState = () => {
  currentLesson = { item: null, context: null, url: null, assetUrl: null };
  announceLessonEvent('');
  setLiveMetaAttr('item-id', null);
  setLiveMetaAttr('lesson-url', null);
};

const focusLessonViewer = () => {
  const viewer = document.getElementById('lessonViewer');
  if (!viewer) return;
  try {
    viewer.focus({ preventScroll: true });
  } catch (_) {
    viewer.focus();
  }
};

export function openLesson(item){
  if (!item || !item.url) return;
  if (item.url.startsWith('/content/')) {
    const viewer = document.getElementById('lessonViewer');
    const panel = document.getElementById('lessonPanel');
    const loader = document.getElementById('lessonLoader');
    if (viewer && panel) {
      lastFocusElement = (document.activeElement && document.activeElement instanceof HTMLElement)
        ? document.activeElement
        : null;
      viewer.setAttribute('aria-busy','true');
      // Show loading indicator
      if (loader) loader.classList.remove('hidden');
      viewer.addEventListener('load', () => {
        viewer.removeAttribute('aria-busy');
        // Hide loading indicator with slight delay for smooth transition
        if (loader) setTimeout(() => loader.classList.add('hidden'), 100);
      }, { once: true });
      const resolvedUrl = resolveLessonAssetUrl(item.url);
      const itemId = item.item_id || item.id || '';
      // Load lesson through template wrapper to enable xelra-md-live telemetry
      const lessonTemplateUrl = buildLessonTemplateUrl(resolvedUrl || item.url, store.learner, itemId);
      viewer.src = lessonTemplateUrl;
      viewer.dataset.itemId = itemId;
      currentLesson = {
        item,
        context: item.telemetry || null,
        url: item.url,
        assetUrl: resolvedUrl || item.url,
      };
      setLiveMetaAttr('item-id', itemId);
      setLiveMetaAttr('lesson-url', resolvedUrl || item.url);
      if (store.learner) {
        setLiveMetaAttr('learner-id', store.learner);
      }
      document.body.classList.add('view-lesson');
      panel.style.display = 'block';
      announceLessonEvent('');
      setTimeout(focusLessonViewer, 30);
      return;
    }
    window.location.href = item.url;
    return;
  }
  // External URL - open in modal iframe
  openExternalContentModal(item.url, item.title || item.name || 'Resource');
}

function openExternalContentModal(url, title) {
  const modalEl = document.getElementById('externalContentModal');
  if (!modalEl) {
    window.open(url, '_blank', 'noopener,noreferrer');
    return;
  }
  const iframe = document.getElementById('externalContentFrame');
  const loader = document.getElementById('externalContentLoader');
  const fallback = document.getElementById('externalContentFallback');
  const titleEl = document.getElementById('externalContentModalLabel');
  const openBtn = document.getElementById('btnExternalContentOpen');
  const fallbackLink = document.getElementById('externalContentLink');

  // Reset state
  if (titleEl) titleEl.textContent = title;
  if (loader) loader.style.display = 'block';
  if (iframe) { iframe.style.display = 'none'; iframe.src = 'about:blank'; }
  if (fallback) fallback.style.display = 'none';
  if (openBtn) openBtn.onclick = () => window.open(url, '_blank', 'noopener,noreferrer');
  if (fallbackLink) fallbackLink.href = url;

  // Show modal
  const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
  modal.show();

  // Try to load iframe
  if (iframe) {
    iframe.onload = () => {
      if (loader) loader.style.display = 'none';
      iframe.style.display = 'block';
    };
    iframe.onerror = () => {
      if (loader) loader.style.display = 'none';
      if (fallback) fallback.style.display = 'block';
    };
    // Give slight delay before loading to ensure modal is visible
    setTimeout(() => { iframe.src = url; }, 100);
  }

  // Cleanup on modal close
  modalEl.addEventListener('hidden.bs.modal', () => {
    if (iframe) iframe.src = 'about:blank';
  }, { once: true });
}

const closeLessonView = ({ restoreFocus = true } = {}) => {
  document.body.classList.remove('view-lesson');
  const viewer = document.getElementById('lessonViewer');
  if (viewer) {
    viewer.removeAttribute('aria-busy');
    try {
      viewer.contentWindow?.postMessage({ type: 'XELRA_PARENT_RESET' }, window.location.origin);
    } catch (_) {
      // ignore cross-origin issues
    }
    viewer.src = 'about:blank';
  }
  if (restoreFocus && lastFocusElement && typeof lastFocusElement.focus === 'function') {
    lastFocusElement.focus();
  }
  clearLessonState();
};

const recordLessonCompletion = (context, { source = 'lesson', action = 'complete', lessonUrl = null } = {}) => {
  const payloadContext = context || currentLesson.context || {};
  const itemId = payloadContext.itemId || currentLesson.item?.item_id || currentLesson.item?.id || null;
  postTelemetry('/v1/telemetry/completion', payloadContext, {
    item_id: itemId,
    action,
    source,
    lesson_url: lessonUrl || currentLesson.url || null,
  });
};

window.__XELRA_CHECK_CELEBRATIONS = false;

async function markLessonComplete(source = 'manual'){
  if (!currentLesson || !currentLesson.item) {
    announceLessonEvent('Lesson marked complete.');
    return;
  }
  recordLessonCompletion(currentLesson.context, { source: 'lesson', action: source === 'manual' ? 'complete' : source, lessonUrl: currentLesson.url });
  showToast('Marked as complete');
  const learnerId = store.learner;
  const itemId = currentLesson.context?.itemId || currentLesson.item?.item_id || currentLesson.item?.id;
  closeLessonView();
  if (learnerId && itemId) {
    try {
      await sendArlEvent('completion', { item_id: itemId }, { refreshFeatures: true });
    } catch (err) {
      console.warn('Failed to sync completion with ARL', err);
    }
    window.__XELRA_CHECK_CELEBRATIONS = true;
    await loadApp({ skipArlCycle: true });
  }
}

const initExplainDrawer = () => {
  const drawer = document.getElementById('explainDrawer');
  if (!drawer) return;
  if (window.bootstrap && window.bootstrap.Offcanvas) {
    explainDrawerInstance = window.bootstrap.Offcanvas.getOrCreateInstance(drawer);
  }
  drawer.addEventListener('show.bs.offcanvas', () => {
    currentExplainStart = typeof performance !== 'undefined' ? performance.now() : Date.now();
    if (currentExplainContext) {
      postTelemetry('/v1/telemetry/explanation', currentExplainContext, {
        item_id: currentExplainContext.itemId,
        action: 'expand',
        level: 'detailed',
        source: 'recs',
        dwell_ms: 0,
      });
    }
  });
  drawer.addEventListener('hidden.bs.offcanvas', () => {
    const context = currentExplainContext;
    if (!context) return;
    const stop = typeof performance !== 'undefined' ? performance.now() : Date.now();
    const dwell = currentExplainStart ? Math.max(0, Math.round(stop - currentExplainStart)) : 0;
    postTelemetry('/v1/telemetry/explanation', context, {
      item_id: context.itemId,
      action: 'collapse',
      level: 'detailed',
      source: 'recs',
      dwell_ms: dwell,
    });
    currentExplainStart = null;
    currentExplainContext = null;
  });
};

const initModeToggle = () => {
  const toggles = [
    { header: 'modeHeaderToggle', body: 'modeBody' },
    { header: 'modeHeaderToggleLesson', body: 'modeBodyLesson' }
  ];

  toggles.forEach(({ header, body }) => {
    const headerEl = document.getElementById(header);
    const bodyEl = document.getElementById(body);
    if (!headerEl || !bodyEl) return;

    const toggle = () => {
      const expanded = headerEl.getAttribute('aria-expanded') === 'true';
      headerEl.setAttribute('aria-expanded', !expanded);
      bodyEl.style.display = expanded ? 'none' : 'block';
    };

    headerEl.addEventListener('click', toggle);
    headerEl.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggle();
      }
    });
  });
};

const updateSystemInsight = (insight, panelSuffix = '') => {
  const el = document.getElementById(`systemInsight${panelSuffix}`);
  if (!el) return;
  if (insight) {
    el.textContent = insight;
    el.style.display = 'block';
  } else {
    el.style.display = 'none';
  }
};

const generateInsight = (olmData, completedCount = 0) => {
  if (!olmData) return null;
  const skills = olmData.skills || [];
  if (skills.length === 0 && completedCount === 0) {
    return "Welcome! Complete your first lesson to start building your skill profile.";
  }
  const avgMastery = skills.length > 0
    ? Math.round(skills.reduce((sum, s) => sum + (s.value || 0), 0) / skills.length * 100)
    : 0;
  if (avgMastery >= 80) {
    return "Excellent progress! You're mastering the material well.";
  }
  if (avgMastery >= 50) {
    return "Good momentum! Keep practicing to strengthen your skills.";
  }
  if (completedCount > 0) {
    return `You've completed ${completedCount} item${completedCount === 1 ? '' : 's'}. Keep going!`;
  }
  return null;
};

window.addEventListener('message', (evt) => {
  if (!evt || typeof evt.data !== 'object') return;
  // Accept messages from same origin, null origin (srcdoc iframes), or file:// protocol
  const validOrigin = !evt.origin
    || evt.origin === 'null'
    || evt.origin === window.location.origin
    || window.location.protocol === 'file:';
  if (!validOrigin) return;
  const { type, item_id: itemId, lesson_url: lessonUrl, ok, ms } = evt.data;
  if (type === 'XELRA_CODE_RUN') {
    const context = currentLesson.context || { meta: window.__XELRA_LAST_TELEMETRY, learnerId: store.learner, itemId: itemId || (currentLesson.item && currentLesson.item.item_id) || null };
    postTelemetry('/v1/telemetry/click', context, {
      item_id: itemId || context.itemId,
      action: 'code_run',
      source: 'lesson',
      lesson_url: lessonUrl || currentLesson.url || null,
      extra_ms: ms,
      ok: ok !== false,
    });
    trackActivity('codeRuns');
    const status = ok === false ? 'Code run failed.' : 'Code executed.';
    const detail = ms ? ` (${ms}ms)` : '';
    announceLessonEvent(`${status}${detail}`);
  }
  if (type === 'XELRA_LESSON_COMPLETE') {
    markLessonComplete('auto').catch((err) => console.error('Auto completion failed', err));
  }
});

const hydrateRecommendations = (res = {}) => {
  const expMap = new Map();
  (res.explanations || []).forEach((entry) => {
    if (!entry || !entry.item_id) return;
    expMap.set(String(entry.item_id), entry);
  });
  const mergedItems = (res.items || []).map((item) => {
    const key = String(item.item_id);
    const extra = expMap.get(key);
    if (!extra) return { ...item };
    const feedback = extra.feedback || {};
    const xaiOlm = extra?.xai?.olm;
    const focusSkillId = (xaiOlm && Array.isArray(xaiOlm.targets) && xaiOlm.targets.length && xaiOlm.targets[0].skill_id)
      || extra?.components?.focus_skill_id
      || extra?.components?.skill_id
      || null;
    return {
      ...item,
      rank: extra.rank,
      reasons: extra.reasons,
      components: extra.components,
      score_breakdown: extra.score_breakdown,
      xai: extra.xai,
      comment: feedback.comment,
      rating: feedback.rating,
      focus_skill_id: focusSkillId,
      feedback,
    };
  });
  return {
    ...res,
    items: mergedItems,
  };
};

const showApiError = (message) => {
  if (!message) return;
  const wrap = document.getElementById('apiErrorAlert');
  if (!wrap) return;
  const box = wrap.querySelector('[data-role="message"]');
  if (box) box.textContent = message;
  wrap.style.display = 'block';
};

const hideApiError = () => {
  const wrap = document.getElementById('apiErrorAlert');
  if (!wrap) return;
  wrap.style.display = 'none';
  const box = wrap.querySelector('[data-role="message"]');
  if (box) box.textContent = '';
};

const timeAgo = (dateInput) => {
  if (!dateInput) return '';
  const date = typeof dateInput === 'string' ? new Date(dateInput) : dateInput;
  if (isNaN(date.getTime())) return '';
  const now = new Date();
  const diffMs = now - date;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins} minute${diffMins === 1 ? '' : 's'} ago`;
  if (diffHours < 24) return `${diffHours} hour${diffHours === 1 ? '' : 's'} ago`;
  if (diffDays === 1) return 'yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} week${Math.floor(diffDays / 7) === 1 ? '' : 's'} ago`;
  return date.toLocaleDateString();
};

function cacheGuardrailsFromCycle(cycle){
  if(!cycle || typeof cycle !== 'object'){
    return;
  }
  // Decision trace stored on window for debugging; not logged to console in production
  window.__XELRA_LAST_CYCLE = cycle;
  if (cycle.policy_version){
    window.__XELRA_POLICY_VERSION = cycle.policy_version;
  }

  try {
    processARLCycleActions(cycle);
  } catch (err) {
    console.warn('Failed to process ARL cycle actions:', err);
  }

  let names = [];
  if (Array.isArray(cycle.active_guardrails) && cycle.active_guardrails.length){
    names = cycle.active_guardrails;
  } else if (Array.isArray(cycle.policy_results)){
    names = cycle.policy_results
      .filter(entry => entry && !entry.skipped && entry.policy)
      .map(entry => {
        const payload = entry.policy;
        const id = payload.id || payload.name;
        const title = payload.title || payload.description || payload.name || payload.id;
        if (title && typeof title === 'string' && title.trim()){
          return POLICY_TITLE_BY_ID[id] || title;
        }
        if (id){
          return POLICY_TITLE_BY_ID[id] || id;
        }
        return null;
      })
      .filter(Boolean);
  }
  if (!names.length){
    return;
  }
  window.__XELRA_POLICY_STACK = Array.from(new Set(names.map(name => POLICY_TITLE_BY_ID[name] || name)));
}

function guardrailReasonDetails(guardrails, cycle){
  const details = [];
  const featureVector = cycle?.feature_vector || {};
  const metadata = featureVector.metadata || {};
  const goals = Array.isArray(featureVector.goals) ? featureVector.goals : [];
  const mastery = featureVector.mastery || {};
  guardrails.forEach(name => {
    if (typeof name !== 'string' || !name.trim()) return;
    const normalized = name.trim();
    const reasons = [];
    switch (normalized) {
      case 'Lapsed Learner Re-engagement': {
        const days = metadata.days_since_last_engagement ?? metadata.days_since_last_impression;
        if (days !== undefined){
          reasons.push(`No recent engagement for ${formatDays(days)}.`);
        }
        if (goals.length){
          const active = goals.filter(goal => {
            const target = Number(goal.target ?? 1);
            const progress = Number(goal.progress ?? 0);
            return progress + 1e-6 < target;
          });
          if (active.length){
            const label = active.map(goal => goal.skill_id || 'goal').join(', ');
            reasons.push(`Open goals still below target: ${label}.`);
          } else {
            reasons.push('Goal present but not yet completed.');
          }
        }
        break;
      }
      case 'Goal Attainment Accelerator': {
        if (typeof metadata.progress_rate === 'number'){
          const pct = (metadata.progress_rate * 100).toFixed(1);
          reasons.push(`Learner progressing steadily (≈ ${pct}% mastery gain per day in the last month).`);
        }
        if (typeof metadata.completions_last_30_days === 'number' && metadata.completions_last_30_days > 0){
          reasons.push(`${metadata.completions_last_30_days} recent completions in the last 30 days.`);
        }
        break;
      }
      case 'Struggling Learner Uplift': {
        const values = Object.values(mastery).map(Number).filter(value => !Number.isNaN(value));
        if (values.length){
          const min = Math.min(...values);
          reasons.push(`Lowest mastery is ${(min * 100).toFixed(0)}%, so we reinforce fundamentals.`);
        }
        reasons.push('No recent engagement signals; reintroducing core practice items.');
        break;
      }
      case 'Orientation Safety Net': {
        if (!Object.keys(mastery || {}).length){
          reasons.push('No mastery data available yet.');
        }
        const noLookback = !Array.isArray(featureVector.impressions) || featureVector.impressions.length === 0;
        if (noLookback){
          reasons.push('Learner has not received recommendations in the last 30 days.');
        }
        reasons.push('Provides a safe baseline pathway before other control routines run.');
        break;
      }
      case 'Data Integrity Control Routine': {
        if (typeof metadata.feature_gap === 'number' && metadata.feature_gap > 0){
          reasons.push(`Feature snapshot missing ${metadata.feature_gap} expected signals; hydrating diagnostics.`);
        }
        break;
      }
      case 'Default Hybrid Pathway': {
        reasons.push('No higher-priority control routine triggered; keeping recommendations balanced.');
        break;
      }
      default: {
        const summary = describePolicy(normalized);
        if (summary){
          reasons.push(summary);
        }
      }
    }
    details.push({ name: normalized, reasons });
  });
  return details;
}

async function sendArlEvent(eventType, metadata = {}, { refreshFeatures = false } = {}) {
  const token = store.token;
  const learnerId = store.learner;
  if (!token || !learnerId) {
    return;
  }
  const payload = {
    learner_id: learnerId,
    event_type: eventType,
  };
  if (metadata && Object.keys(metadata).length) {
    payload.metadata = metadata;
  }
  if (refreshFeatures) {
    payload.refresh_features = true;
  }
  try {
    const cycle = await api('/v1/arl/event', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    });
    // Cache the cycle response and update OLM panel with new mode
    if (cycle && typeof cycle === 'object') {
      cacheGuardrailsFromCycle(cycle);
      if (window.ARLEnhanced && cycle.learner_facing_fields) {
        window.ARLEnhanced.updateRegulatoryModePanel(cycle);
        window.ARLEnhanced.updateRegulatoryModePanel(cycle, 'Lesson');
      }
    }
  } catch (err) {
    console.warn('Failed to dispatch ARL event', eventType, err);
  }
}

    async function ensureConsent(learnerId, { force = false } = {}){
      if(!learnerId){ return false; }
      if(telemetryConsentState.known && !force){
        setLiveMetaAttr('telemetry-consent', telemetryConsentState.granted ? 'granted' : 'pending');
        if(telemetryConsentState.granted){
          return true;
        }
        return new Promise((resolve)=> telemetryConsentState.waiters.push(resolve));
      }
      if(telemetryConsentState.checking){
        return new Promise((resolve)=> telemetryConsentState.waiters.push(resolve));
      }
      telemetryConsentState.checking = true;
      try{
        const c = await api(`/v1/telemetry/consent/${encodeURIComponent(learnerId)}`);
        const granted = Boolean(c && c.consent_given);
        telemetryConsentState.granted = granted;
        telemetryConsentState.known = true;
        setLiveMetaAttr('telemetry-consent', granted ? 'granted' : 'pending');
        if(!granted){
          console.warn('Consent not recorded for learner. They may need to re-authenticate.');
        }
        flushConsentWaiters(granted);
        if(granted) telemetryQueue.process();
        return granted;
      }catch(err){
        console.error('Failed to check consent status:', err);
        telemetryConsentState.granted = false;
        telemetryConsentState.known = false;
        flushConsentWaiters(false);
        return false;
      }finally{
        telemetryConsentState.checking = false;
      }
    }

    telemetryQueue.setConsentChecker(ensureConsent);

    let surveyState = {
      pending: false,
      week: null,
      url: null,
      codeRequired: false,
    };

    async function checkSurveyStatus(learnerId) {
      try {
        const res = await api(`/v1/survey/status/${encodeURIComponent(learnerId)}`);
        if (res && res.survey_due && res.enabled) {
          surveyState.pending = true;
          surveyState.week = res.survey_week;
          surveyState.url = res.survey_url;
          surveyState.codeRequired = res.code_required || false;
          return true;
        }
      } catch (e) {
        console.warn('Survey status check failed:', e);
      }
      surveyState.pending = false;
      return false;
    }

    function showSurveyModal() {
      const overlay = document.getElementById('surveyOverlay');
      const iframe = document.getElementById('surveyIframe');
      const weekBadge = document.getElementById('surveyWeekBadge');
      const codeSection = document.getElementById('surveyCodeSection');
      const codeInput = document.getElementById('surveyCodeInput');
      const codeError = document.getElementById('surveyCodeError');

      if (!overlay || !iframe) return;

      if (surveyState.url) {
        const surveyUrl = new URL(surveyState.url);
        if (store.arm) surveyUrl.searchParams.set('group', store.arm);
        iframe.src = surveyUrl.toString();
      }
      if (weekBadge && surveyState.week) {
        weekBadge.textContent = `Week ${surveyState.week}`;
      }

      // Show/hide code input based on whether verification is required
      if (codeSection) {
        codeSection.style.display = surveyState.codeRequired ? 'block' : 'none';
      }
      if (codeInput) codeInput.value = '';
      if (codeError) codeError.style.display = 'none';

      overlay.style.display = 'flex';
    }

    function hideSurveyModal() {
      const overlay = document.getElementById('surveyOverlay');
      const iframe = document.getElementById('surveyIframe');
      if (overlay) overlay.style.display = 'none';
      if (iframe) iframe.src = '';
    }

    async function completeSurvey(learnerId) {
      if (!surveyState.week) return;

      const codeInput = document.getElementById('surveyCodeInput');
      const codeError = document.getElementById('surveyCodeError');
      const code = codeInput ? codeInput.value.trim() : '';

      // If code is required but not provided, show error
      if (surveyState.codeRequired && !code) {
        if (codeError) {
          codeError.textContent = 'Please enter the completion code from the survey';
          codeError.style.display = 'block';
        }
        return;
      }

      try {
        await api('/v1/survey/complete', {
          method: 'POST',
          body: JSON.stringify({
            learner_id: learnerId,
            survey_week: surveyState.week,
            code: code || null,
          }),
        });
        surveyState.pending = false;
        surveyState.week = null;
        surveyState.codeRequired = false;
        showToast('Survey completed - thank you!');
        hideSurveyModal();
      } catch (e) {
        console.error('Failed to mark survey complete:', e);
        // Check if it's a code validation error
        if (e.message && e.message.includes('code')) {
          if (codeError) {
            codeError.textContent = 'Invalid completion code. Please check and try again.';
            codeError.style.display = 'block';
          }
        } else {
          showToast('Failed to save survey completion');
          hideSurveyModal();
        }
      }
    }

    function initSurveyModal() {
      const btnDone = document.getElementById('btnSurveyDone');

      if (btnDone) {
        btnDone.addEventListener('click', () => {
          completeSurvey(store.learner);
        });
      }
    }

    async function applyArm(learnerId) {
      const armRes = await api(`/v1/telemetry/arm/${encodeURIComponent(learnerId)}`);
      const arm = armRes.arm || 'T';
      const cfg = ARM_MAP[arm] || ARM_MAP['T'];
      window.__XELRA_LAST_ARM = arm;
      window.__XELRA_LAST_STRATEGY = cfg.strategy;

      const badge = document.getElementById('armBadge');
      badge.textContent = `Arm ${arm} — ${cfg.label}`;
      const strategyEl = document.getElementById('strategyName');
      if (strategyEl) strategyEl.textContent = cfg.strategy;

      // Update arm-specific feature visibility
      // pilotMode overrides arm restrictions - all features visible to all users
      armFeatures.allowExplain = cfg.allowExplain || featureFlags.pilotMode;
      armFeatures.allowSentiment = cfg.allowSentiment || featureFlags.pilotMode;
      armFeatures.allowRegulatoryMode = cfg.allowRegulatoryMode || featureFlags.pilotMode;

      const modeBody = document.getElementById('modeBody');
      const modeBodyLesson = document.getElementById('modeBodyLesson');
      const regulatoryModeCard = document.getElementById('regulatoryModeCard');
      const regulatoryModeCardLesson = document.getElementById('regulatoryModeCardLesson');

      // Regulatory mode card (mode/why/next/exit) is shown ONLY for the ARL
      // treatment arm.  B1 (Control A) shows SHAP feature attribution via the
      // explain drawer but NOT the structured regulatory transparency card.
      // B3 (Control B) shows neither.
      if (armFeatures.allowRegulatoryMode) {
        if (regulatoryModeCard) {
          regulatoryModeCard.style.display = 'block';
        }
        if (regulatoryModeCardLesson) {
          regulatoryModeCardLesson.style.display = 'block';
        }
        if (modeBody) {
          modeBody.style.display = 'block';
        }
        if (modeBodyLesson) {
          modeBodyLesson.style.display = 'block';
        }
      } else {
        // Hide regulatory mode card for B1 and B3 arms
        if (regulatoryModeCard) {
          regulatoryModeCard.style.display = 'none';
        }
        if (regulatoryModeCardLesson) {
          regulatoryModeCardLesson.style.display = 'none';
        }
      }

      return cfg;
    }

    function impressList(){
      const cards=Array.from(document.querySelectorAll('[data-item-id]'));
      if(cards.length===0) return;
      cards.forEach((el, idx)=>{
        const context = el.__telemetryContext || null;
        if (context && context.rank === undefined) {
          context.rank = idx + 1;
        }
        recordImpression(context);
      });
    }

    function sizeClassFromScore(){ return 'card-primary'; }

    function renderScatter(learnerId, res, cfg){
      window.__XELRA_LAST_TELEMETRY = res.telemetry || null;
      if(cfg && cfg.strategy){
        window.__XELRA_LAST_STRATEGY = cfg.strategy;
      } else if(res && res.strategy){
        window.__XELRA_LAST_STRATEGY = res.strategy;
      }
      if(res && res.telemetry && res.telemetry.arm_key){
        window.__XELRA_LAST_ARM = res.telemetry.arm_key;
      } else if(res && res.arm){
        window.__XELRA_LAST_ARM = res.arm;
      }
      const telemetryMeta = window.__XELRA_LAST_TELEMETRY;
      const board=document.getElementById('board');
      board.innerHTML='';
      const armKey = window.__XELRA_LAST_ARM || (res.telemetry && res.telemetry.arm_key) || res.arm || null;
      const policyVersion = res.policy_version || (res.telemetry && res.telemetry.policy_version) || '\u2014';
      window.__XELRA_POLICY_VERSION = policyVersion;
      let policyNames = [];
      if (Array.isArray(res.active_guardrails) && res.active_guardrails.length) {
        policyNames = res.active_guardrails
          .map(name => {
            if (typeof name !== 'string') return null;
            const trimmed = name.trim();
            if (!trimmed) return null;
            return POLICY_TITLE_BY_ID[trimmed] || trimmed;
          })
          .filter(Boolean);
      } else if (Array.isArray(res.policy_results)) {
        policyNames = res.policy_results
          .filter(r => r && !r.skipped)
          .map(r => {
            const payload = r.policy;
            if (payload && typeof payload === 'object') {
              const id = payload.id || payload.name || r.policy_name;
              const title = payload.title || payload.name || payload.id;
              if (title && typeof title === 'string' && title.trim()) {
                return POLICY_TITLE_BY_ID[id] || title;
              }
              if (id) {
                return POLICY_TITLE_BY_ID[id] || id;
              }
            }
            if (typeof payload === 'string') {
              return POLICY_TITLE_BY_ID[payload] || payload;
            }
            if (typeof r.policy_name === 'string') {
              return POLICY_TITLE_BY_ID[r.policy_name] || r.policy_name;
            }
            return null;
          })
          .filter(Boolean);
      }
      if (!policyNames.length && Array.isArray(window.__XELRA_POLICY_STACK) && window.__XELRA_POLICY_STACK.length){
        policyNames = Array.from(window.__XELRA_POLICY_STACK);
      }
      window.__XELRA_POLICY_STACK = Array.from(new Set(policyNames));
      const policyStack = window.__XELRA_POLICY_STACK;
      const policyName = policyStack.length ? policyStack.join(', ') : '';
      const bundleVersion = policyVersion || 'v1';
      const guardrailTooltip = policyTooltipText(policyStack);
      const guardrailLabel = policyTagLabel(policyStack);
      const guardrailShort = policyShortSummary(policyStack);
      const guardrailTag = `<span class="guardrail-tag" title="${escapeHtml(guardrailTooltip)}">${escapeHtml(guardrailLabel)}</span>`;
      const notice = document.getElementById('arlNotice');
      const armIntro = armKey ? [
        `Your learning pathway: ${guardrailTag}.`,
        'Tap "Explain" on any recommendation to see why it was suggested.'
      ].join(' ') : '';
      window.__XELRA_ARM_NOTICE = armIntro;
      if(notice){
        if(armIntro){
          notice.innerHTML = armIntro;
          notice.style.display = 'none';
        }else{
          notice.style.display = 'none';
        }
      }
      const items = res.items||[];
      const scores = items.map(i=> i.score ?? 0); 
      const min=Math.min(...scores, 0); 
      const max=Math.max(...scores, 1);
      const summarySnapshot = window.__XELRA_LAST_OLM_SUMMARY || {};
      let focusSkillId = (items[0] && items[0].focus_skill_id) || null;
      const progressFocus = res.progress && Array.isArray(res.progress.skills_at_level) && res.progress.skills_at_level.length
        ? res.progress.skills_at_level[0]
        : (res.progress && (res.progress.focus_skill_id || res.progress.skill_id));
      if(!focusSkillId && progressFocus){
        focusSkillId = progressFocus;
      }
      if(!focusSkillId && summarySnapshot && Array.isArray(summarySnapshot.top_gaps) && summarySnapshot.top_gaps.length){
        const topGap = summarySnapshot.top_gaps[0];
        focusSkillId = typeof topGap === 'string' ? topGap : topGap && (topGap.id || topGap.skill_id);
      }
      if(!focusSkillId && summarySnapshot && Array.isArray(summarySnapshot.skills)){
        const firstLow = summarySnapshot.skills.find(s => (s.value || 0) < 1.0);
        focusSkillId = firstLow ? firstLow.id : (summarySnapshot.skills[0] && summarySnapshot.skills[0].id);
      }
      if(items[0] && !items[0].focus_skill_id){
        items[0].focus_skill_id = focusSkillId || null;
      }
      window.__XELRA_FOCUS_SKILL_ID = focusSkillId || null;

      let currentPrimary = items[0] || null;

      const renderPrimaryCard = (it, rank = 1) => {
        const sizeCls = sizeClassFromScore(it.score || 0, min, max);
        const col = document.createElement('div');
        col.className = sizeCls;
        col.style.setProperty('--rot', randRot());
        const courseId = it.course_id || (it.components && it.components.course_id) || (res.course_id || null);
        const context = {
          meta: telemetryMeta,
          learnerId,
          itemId: it.item_id,
          rank,
          strategy: window.__XELRA_LAST_STRATEGY || cfg.strategy || null,
          arm: armKey,
          policyVersion,
          courseId,
          requestId: telemetryMeta && telemetryMeta.request_id,
        };
        it.telemetry = context;

        // Meta line removed - score and sequence info not shown to learners
        const resolvedUrl = it.url ? resolveLessonAssetUrl(it.url) : '';
        const hasUrl = Boolean(resolvedUrl);
        const activeUrl = hasUrl ? resolvedUrl : '';
        const safeLinkUrl = it.url ? escapeHtml(it.url) : '';
        const escapedTitle = escapeHtml(it.title || it.item_id || 'Lesson');
        const previewTitle = escapeHtml(`Preview: ${it.title || it.item_id || 'Lesson'}`);
        const frameAttr = hasUrl ? '' : ' data-state="fallback"';
        const frameContent = hasUrl
          ? `<iframe src="${escapeHtml(activeUrl)}" title="${previewTitle}" class="rec-iframe" loading="eager" allow="clipboard-write; fullscreen"></iframe>`
          : `<div>No resource URL provided for this recommendation.</div>`;

        col.innerHTML = `<div class="card recommendation-card h-100" data-item-id="${it.item_id}">
            <div class="card-header">
              <div class="d-flex flex-wrap gap-3 align-items-start justify-content-between">
                <div class="flex-grow-1 min-width-0">
                  <h5 class="card-title mb-0">${escapedTitle}</h5>
                </div>
                <div class="control-bar">
                  <button class="btn btn-sm btn-primary btnComplete"><i class="bi bi-check2"></i> Complete</button>
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="resource-frame"${frameAttr}>
                ${frameContent}
              </div>
            </div>
          </div>`;

        if (hasUrl) {
          const lessonUrl = activeUrl || it.url || '';
          currentLesson = {
            item: it,
            context,
            url: it.url,
            assetUrl: lessonUrl,
          };
          setLiveMetaAttr('item-id', it.item_id || it.id || '');
          setLiveMetaAttr('lesson-url', lessonUrl);
          if (store.learner) {
            setLiveMetaAttr('learner-id', store.learner);
          }
        }

        const card = col.querySelector('.card');
        card.__telemetryContext = context;
        const btnComplete = col.querySelector('.btnComplete');
        const iframe = col.querySelector('.resource-frame iframe');

        // Track click interactions with the recommendation card
        let cardClickTracked = false;
        const trackCardClick = (source = 'card') => {
          if (cardClickTracked) return;
          cardClickTracked = true;
          postTelemetry('/v1/telemetry/click', context, {
            item_id: it.item_id,
            action: 'click',
            source: 'recs',
            lesson_url: it.url && it.url.startsWith('/content/') ? it.url : undefined,
          });
        };

        // Track click on card area (excluding interactive controls)
        card.addEventListener('click', (evt) => {
          const target = evt.target;
          // Skip if clicking on buttons or other interactive elements
          if (target.closest('button') || target.closest('a')) {
            return;
          }
          trackCardClick('card');
        });

        if (iframe) {
          iframe.setAttribute('aria-busy', 'true');
          iframe.addEventListener('load', () => {
            iframe.removeAttribute('aria-busy');
            try {
              const doc = iframe.contentDocument || iframe.contentWindow?.document || null;
              if (!doc || (doc.location && doc.location.href === 'about:blank')) return;
              prepareLessonDocument(doc);
            } catch (err) {
              console.warn('Failed to prepare inline lesson iframe', err);
            }
          });
        }

        // Helper to open reflection modal for this item - always start fresh
        // onClose callback is used to load the next resource after modal closes
        const openReflection = (onClose) => {
          openNoteModal({
            item: it,
            learnerId,
            rating: 0,
            noteBody: '',
            sentiment: null,
            onSave: ({ raw, sentiment, composed, rating }) => {
              it.comment = composed;
              if (rating !== undefined && rating > 0) {
                it.rating = rating;
                trackActivity('ratings');
              }
              if (raw && raw.trim()) trackActivity('reflections');
              currentPrimary = it;
              rerender();
              loadLatestSentiment(learnerId);
            },
            onClose,
          });
        };

        if (btnComplete) {
          btnComplete.addEventListener('click', async () => {
            // Disable button and show loading state
            btnComplete.disabled = true;
            const originalText = btnComplete.innerHTML;
            btnComplete.innerHTML = '<i class="bi bi-hourglass-split"></i> Saving...';
            try {
              // Post telemetry and wait for ARL event before removing card
              postTelemetry('/v1/telemetry/completion', context, {
                item_id: it.item_id,
                action: 'complete',
                source: 'recs',
                lesson_url: it.url && it.url.startsWith('/content/') ? it.url : undefined,
              });
              await sendArlEvent('completion', { item_id: it.item_id }, { refreshFeatures: true });
              // Success - show feedback modal, then load next resource when modal closes
              trackActivity('completions');
              showToast('Marked as complete');
              // Enable celebration checks for the next render (mastery may have changed)
              window.__XELRA_CHECK_CELEBRATIONS = true;
              // Open reflection modal - next resource loads only after modal closes
              openReflection(async () => {
                col.remove();
                await loadApp({ skipArlCycle: true });
              });
            } catch (e) {
              console.error(e);
              const msg = errorMessage(e, 'Failed to mark as complete');
              showToast(msg);
              // Restore button state on failure
              btnComplete.disabled = false;
              btnComplete.innerHTML = originalText;
            }
          });
        }

        board.appendChild(col);
      };

      const rerender = () => {
        board.innerHTML='';
        if(currentPrimary){
          if(!currentPrimary.focus_skill_id && window.__XELRA_FOCUS_SKILL_ID){
            currentPrimary.focus_skill_id = window.__XELRA_FOCUS_SKILL_ID;
          }
          renderPrimaryCard(currentPrimary);
          renderOLMSummary(window.__XELRA_LAST_OLM_SUMMARY || {skills:[], goals:{}}, learnerId, window.__XELRA_FOCUS_SKILL_ID);
          // Update the persistent model-explanation card in both OLM panels
          // with feature attribution from the current recommendation.
          updateModelExplainCard(currentPrimary);
          updateModelExplainCard(currentPrimary, 'Lesson');
        }
        setTimeout(()=> impressList(learnerId), 50);
      };

      rerender();
    }

      function renderLatestSentiment(data, state='loaded'){
        // Render to both OLM panel containers
        const containers = [
          document.getElementById('latestSentimentOLM'),
          document.getElementById('latestSentimentLesson')
        ].filter(Boolean);
        if(!containers.length) return;

        containers.forEach(wrap => {
          wrap.innerHTML = '';
          wrap.removeAttribute('aria-busy');
          if(state==='loading' || state==='disabled' || state==='error'){
            wrap.style.display='none';
            return;
          }

          // Extract text and check for sentiment markers
          const txt = (data && data.text) ? data.text.trim() : '';
          const sentimentMatch = txt.match(/^\[\s*(positive|neutral|negative)\s*\]/i);
          const cleanTxt = txt.replace(/^\[\s*(positive|neutral|negative)\s*\]\s*/i, '').trim();
          const hasSentimentMarker = Boolean(sentimentMatch);

          // Skip only if completely empty (no text and no sentiment marker)
          if(!cleanTxt && !hasSentimentMarker){
            wrap.style.display='none';
            return;
          }

          // Determine sentiment label - prefer explicit marker, otherwise use polarity
          const polarity = data.polarity ?? 0;
          let sentLabel;
          if (sentimentMatch) {
            sentLabel = sentimentMatch[1].toLowerCase();
          } else {
            sentLabel = polarity > 0.3 ? 'positive' : polarity < -0.3 ? 'negative' : 'neutral';
          }
          const sentIcon = sentLabel === 'positive' ? 'emoji-smile' : sentLabel === 'negative' ? 'emoji-frown' : 'emoji-neutral';
          const sentColor = sentLabel === 'positive' ? 'text-success' : sentLabel === 'negative' ? 'text-danger' : 'text-warning';

          const card = document.createElement('div');
          card.className = 'sent-card';
          card.innerHTML = `
            <p class="mb-0 small">
              <i class="bi bi-${sentIcon} me-1 ${sentColor}"></i>
              Your last reflection was <strong class="${sentColor}">${sentLabel}</strong>
            </p>`;

          wrap.appendChild(card);
          wrap.style.display = 'block';
        });
      }

    async function loadLatestSentiment(learnerId){
      // Check both global feature flag AND arm-specific sentiment visibility
      // Sentiment is only shown if: global flag enabled AND (arm allows it OR pilot mode)
      if(!featureFlags.sentiment || !armFeatures.allowSentiment){
        renderLatestSentiment(null,'disabled');
        return;
      }
      renderLatestSentiment(null,'loading');
      try{
        const res = await api(`/v1/feedback/latest_explain/${encodeURIComponent(learnerId)}`);
        if(res && res.text){
          store.lastSentiment = { learner: learnerId, ...res };
          renderLatestSentiment(res);
        }else{
          renderLatestSentiment(null);
        }
      }catch(e){
        renderLatestSentiment(null,'error');
      }
    }

    async function loadOLM(learnerId){
      try{
        const summary = await api(`/v1/olm/summary/${encodeURIComponent(learnerId)}`);
        window.__XELRA_LAST_OLM_SUMMARY = summary;
        renderOLM(summary, learnerId);
        renderOLMSummary(summary, learnerId, window.__XELRA_FOCUS_SKILL_ID);
      }catch(e){
        console.error('Failed to load learner progress:', e);
        const msg = errorMessage(e, 'Failed to load progress.');
        const target = document.getElementById('olmList');
        if(target){
          target.innerHTML = '';
          const em = document.createElement('em');
          em.textContent = msg;
          target.appendChild(em);
        }
        showApiError(msg);
      }
      loadLatestSentiment(learnerId);
    }

    async function loadCompleted(learnerId){
      const box = document.getElementById('completedList');
      if(!learnerId || !box) return;
      box.innerHTML = '<em>Loading…</em>';
      try{
        const res = await api(`/v1/recommend/completed/${encodeURIComponent(learnerId)}`);
        const items = res.items || [];
        if(items.length === 0){ box.innerHTML = '<div class="text-center py-3"><i class="bi bi-check2-circle fs-3 text-muted mb-2 d-block"></i><em>No completed items yet.</em><div class="small text-muted mt-1">Complete your first lesson to see it here!</div></div>'; return; }
        box.innerHTML = '';
        items.forEach(it=>{
          const row = document.createElement('div');
          row.className = 'mb-3';
          const when = it.completed_at ? timeAgo(it.completed_at) : '';
          row.innerHTML = `
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <strong>${escapeHtml(it.title || it.item_id)}</strong>
                <div class="small text-muted">${when ? ('Completed ' + when) : 'Completed'}</div>
              </div>
              <div class="ms-3">
                <a href="${it.url || '#'}" target="_blank" class="btn btn-sm btn-outline-light" ${it.url ? '' : 'disabled'}>
                  <i class="bi bi-box-arrow-up-right"></i>
                </a>
              </div>
            </div>`;
          box.appendChild(row);
        });
      }catch(e){
        console.error('Failed to load completed items:', e);
        const msg = errorMessage(e, 'Failed to load completed items.');
        box.innerHTML = '';
        const em = document.createElement('em');
        em.textContent = msg;
        box.appendChild(em);
        showApiError(msg);
      }
    }

    function renderOLMSummary(p, learnerId, focusSkillId){
      const focusSkillName = document.getElementById('focusSkillName');
      const focusMasteryBar = document.getElementById('focusMasteryBar');
      const focusMasteryText = document.getElementById('focusMasteryText');
      const btnFocusGoalSide = document.getElementById('btnFocusGoalSide');

      const skills = p.skills || [];
      const focusSkill = skills.find(s=> s.id === focusSkillId) || skills[0];

      if(focusSkill){
        const pct = Math.round((focusSkill.value||0)*100);
        const goal = (p.goals||{})[focusSkill.id];
        const goalPct = goal!==undefined ? Math.round(goal*100) : null;
        const goalMet = goalPct!==null ? (pct >= goalPct) : false;

        if(focusSkillName) focusSkillName.textContent = focusSkill.name || 'Unknown Skill';
        if(focusMasteryBar){
          focusMasteryBar.style.width = `${pct}%`;
          focusMasteryBar.className = `progress-bar ${goalMet ? 'bg-info' : 'bg-success'}`;
        }
        if(focusMasteryText) focusMasteryText.textContent = `Current mastery: ${pct}%`;

        if(btnFocusGoalSide){
          if(goalPct !== null){
            btnFocusGoalSide.className = 'goal-pill-small goal-pill-active';
            btnFocusGoalSide.innerHTML = `<i class="bi bi-flag-fill"></i><span id="goalLabelSide">Goal ${goalPct}%</span>`;
          }else{
            btnFocusGoalSide.className = 'goal-pill-small';
            btnFocusGoalSide.innerHTML = `<i class="bi bi-flag"></i><span id="goalLabelSide">Set goal</span>`;
          }
          btnFocusGoalSide.onclick = ()=> showGoalModal(learnerId, focusSkill, goal);
        }

        window.__XELRA_FOCUS_SKILL = focusSkill;
        window.__XELRA_FOCUS_SKILL_ID = focusSkill.id;
      }

      if(window.__XELRA_LAST_CYCLE && window.ARLEnhanced && armFeatures.allowRegulatoryMode){
        window.ARLEnhanced.updateRegulatoryModePanel(window.__XELRA_LAST_CYCLE);
        window.ARLEnhanced.updateRegulatoryModePanel(window.__XELRA_LAST_CYCLE, 'Lesson');
      }

      const completedCount = (p.completed && p.completed.length) || 0;
      const insight = generateInsight(p, completedCount);
      updateSystemInsight(insight);

      const btnCompletedSide = document.getElementById('btnCompletedSide');
      if(btnCompletedSide && p.completed && p.completed.length > 0){
        btnCompletedSide.style.display = 'block';
      }

      window.__XELRA_LAST_SUMMARY = p;
    }

    function playArlLoop(loopEl){
      if(!loopEl){
        return;
      }
      if(typeof loopEl.__arlCancel === 'function'){
        loopEl.__arlCancel();
      }
      loopEl.classList.remove('arl-loop-animate');
      loopEl.classList.remove('arl-loop-flare');
      void loopEl.offsetWidth;
      requestAnimationFrame(()=>{
        loopEl.classList.add('arl-loop-flare');
        loopEl.classList.add('arl-loop-animate');
        loopEl.addEventListener('animationend', ()=>{
          loopEl.classList.remove('arl-loop-animate');
          loopEl.classList.remove('arl-loop-flare');
        }, {once:true});
      });
      typeLoopSteps(loopEl);
    }

    function typeLoopSteps(loopEl){
      if(!loopEl){
        return;
      }
      if(typeof loopEl.__arlCancel === 'function'){
        loopEl.__arlCancel();
      }
      const stepSpans = Array.from(loopEl.querySelectorAll('.arl-loop-step-text'));
      if(!stepSpans.length){
        return;
      }
      const prefersReducedMotion =
        typeof window.matchMedia === 'function' &&
        window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      const timers = [];
      let cancelled = false;
      loopEl.__arlCancel = () => {
        cancelled = true;
        timers.forEach(clearTimeout);
        loopEl.__arlCancel = null;
      };
      stepSpans.forEach(span => {
        const text = span.dataset.stepText || '';
        if(prefersReducedMotion){
          span.textContent = text;
        }else{
          span.textContent = '';
        }
        span.classList.remove('typing');
      });
      if(prefersReducedMotion){
        loopEl.__arlCancel = null;
        return;
      }
      let stepIndex = 0;
      const typeSpeed = 24;
      const breakDelay = 220;

      const typeNext = () => {
        if(cancelled || stepIndex >= stepSpans.length){
          loopEl.__arlCancel = null;
          return;
        }
        const span = stepSpans[stepIndex];
        const text = span.dataset.stepText || '';
        let charIndex = 0;
        span.classList.add('typing');
        const tick = () => {
          if(cancelled){
            return;
          }
          if(charIndex <= text.length){
            span.textContent = text.slice(0, charIndex);
            charIndex += 1;
            timers.push(setTimeout(tick, typeSpeed));
          }else{
            span.classList.remove('typing');
            stepIndex += 1;
            timers.push(setTimeout(typeNext, breakDelay));
          }
        };
        tick();
      };

      typeNext();
    }

    function renderOLM(p, learnerId){
      const box = document.getElementById('olmList');
      box.innerHTML = '';
      const skills = p.skills || [];
      if(skills.length===0){ box.innerHTML = '<div class="text-center py-3"><i class="bi bi-bar-chart-line fs-3 text-muted mb-2 d-block"></i><em>Your skills will appear here</em><div class="small text-muted mt-1">Complete lessons to build your skill profile!</div></div>'; return; }
      skills.forEach(s=>{
        const pct = Math.round((s.value||0)*100);
        const goal = (p.goals||{})[s.id];
        const goalPct = goal!==undefined ? Math.round(goal*100) : null;
        const goalMet = goalPct!==null ? (pct >= goalPct) : false;

        if (window.__XELRA_CHECK_CELEBRATIONS) {
          if (pct === 100 && !hasCelebrated(learnerId, s.id, 'full')) {
            celebrateSkill(learnerId, s.name, s.id, 'full');
          } else if (goalMet && !hasCelebrated(learnerId, s.id, 'goal')) {
            celebrateSkill(learnerId, s.name, s.id, 'goal');
          }
        }

        const row = document.createElement('div');
        row.className = 'mb-3';
        row.innerHTML = `
          <div class="d-flex justify-content-between align-items-center mb-1">
            <strong>${s.name}</strong>
          </div>
          <div class="progress" style="height:6px;" title="Estimated mastery (not % of items completed)">
            <div class="progress-bar ${goalMet ? 'bg-info' : 'bg-success'}" style="width:${pct}%"></div>
          </div>
          <div class="d-flex justify-content-between align-items-center mt-1">
            ${goal!==undefined
              ? `<span class="badge text-bg-info">${goalMet ? 'Goal reached' : 'Goal ' + goalPct + '%'}</span>`
              : ''}
            <div class="ms-auto"></div>
            <button class="btn btn-sm btn-outline-light ${goal!==undefined?'btnClear':'btnSet'}">
              ${goal!==undefined?'Clear goal':'Set goal'}
            </button>
          </div>`;
        const btn = row.querySelector(goal!==undefined?'.btnClear':'.btnSet');
        if(goal!==undefined){ btn.addEventListener('click', ()=>clearGoal(s.id, learnerId)); }
        else{ btn.addEventListener('click', ()=>showGoalModal(learnerId, s, goal)); }
        box.appendChild(row);
      });
      window.__XELRA_CHECK_CELEBRATIONS = false;
      if(p.top_gaps && p.top_gaps.length){
        const gap = document.createElement('div');
        gap.className = 'mt-3';
        gap.innerHTML = `<strong>Next focus:</strong> ${p.top_gaps.map(g=>g.name).join(', ')}`;
        box.appendChild(gap);
      }
    }

    function showGoalModal(learnerId, skill){
      const modalEl = document.getElementById('goalModal');
      const modal = bootstrap.Modal.getOrCreateInstance(modalEl);
      const rng = document.getElementById('goalRange');
      const out = document.getElementById('goalRangeVal');
      const label = document.getElementById('goalModalLabel');
      const saveBtn = document.getElementById('goalSave');
      label.textContent = `Set goal for ${skill.name}`;
      rng.value = Math.max(80, Math.round((skill.value||0)*100));
      out.textContent = rng.value + '%';
      rng.oninput = ()=> out.textContent = rng.value + '%';
      saveBtn.onclick = async ()=>{
        const target = parseInt(rng.value,10)/100;
        try{
          await api('/v1/olm/goal',{method:'POST', body: JSON.stringify({ learner_id: learnerId, skill_id: skill.id, target })});
          try{ await api('/v1/telemetry/olm_event',{method:'POST', body: JSON.stringify({ learner_id: learnerId, skill_id: skill.id, action:'goal_set', target })}); }catch(e){}
          await sendArlEvent('goal_update', { skill_id: skill.id, target }, { refreshFeatures: true });
          modal.hide();
          window.__XELRA_CHECK_CELEBRATIONS = true;
          await loadApp({ skipArlCycle: true });
        }catch(e){
          console.error('Failed to save goal:', e);
          const msg = errorMessage(e, 'Failed to save goal');
          showToast(msg);
          showApiError(msg);
        }
      };
      modal.show();
    }

    async function clearGoal(skillId, learnerId){
      try{
        await api(`/v1/olm/goal/${encodeURIComponent(learnerId)}/${encodeURIComponent(skillId)}`, {method:'DELETE'});
        try{ await api('/v1/telemetry/olm_event',{method:'POST', body: JSON.stringify({ learner_id: learnerId, skill_id: skillId, action:'goal_clear' })}); }catch(e){}
        await sendArlEvent('goal_update', { skill_id: skillId, action: 'clear' }, { refreshFeatures: true });
        unmarkCelebrated(learnerId, skillId, 'goal');
        await loadApp({ skipArlCycle: true });
      }catch(e){
        console.error('Failed to clear goal:', e);
        const msg = errorMessage(e, 'Failed to clear goal');
        showToast(msg);
        showApiError(msg);
      }
    }

    async function loadApp(options = {}) {
      if (typeof options === 'string') {
        options = {};
      }
      const { skipArlCycle = false } = options;

      // Prevent race condition: don't interrupt an active login flow
      // (e.g., user is on the consent step after verifying OTP)
      if (isLoginInProgress()) {
        return;
      }

      const token = store.token;
      const learnerId = store.learner;

      const login = document.getElementById('viewLogin');
      const app = document.getElementById('viewApp');

      if (!login || !app) {
        console.error('viewLogin or viewApp element not found in the DOM.');
        return;
      }

      if (!token || !learnerId) {
        //console.warn('No token or learnerId found. Showing login view.');
        login.style.setProperty('display', 'flex', 'important');
        app.style.setProperty('display', 'none', 'important');
        return;
      }

      // Validate token with backend before proceeding (catches expired/invalid tokens)
      try {
        const meRes = await api('/v1/standalone/me', {
          method: 'POST',
          body: JSON.stringify({ token }),
        });
        if (!meRes.ok) {
          throw new Error('Token validation failed');
        }
      } catch (e) {
        console.warn('Token validation failed, requiring re-login:', e);
        // Clear invalid token and show login
        try {
          localStorage.removeItem('token');
          localStorage.removeItem('learner_id');
        } catch (_) {}
        login.style.setProperty('display', 'flex', 'important');
        app.style.setProperty('display', 'none', 'important');
        return;
      }

      hideApiError();

      // Check consent BEFORE showing the app — if not consented, sign out
      // so the consent step appears again on next login.
      // Skip the check if consent was just granted in the login flow.
      try {
        let ok = true;
        if (wasConsentJustGranted()) {
          // Consent was just recorded — skip the API check and clear the flag
          setConsentJustGranted(false);
        } else {
          ok = await ensureConsent(learnerId);
        }
        if (!ok) {
          console.warn('Consent not granted — signing out to re-trigger consent flow.');
          signOut();
          return;
        }

        // Consent verified — now show the app
        login.style.setProperty('display', 'none', 'important');
        app.style.setProperty('display', 'block', 'important');
        setLiveMetaAttr('learner-id', learnerId);
        document.getElementById('btnSignOut').style.display = 'inline-flex';
        const navActivity = document.getElementById('navActivityIndicator');
        if (navActivity) navActivity.style.display = 'flex';
        const navAllSkills = document.getElementById('btnAllSkillsNav');
        if (navAllSkills) navAllSkills.style.display = 'inline-flex';

        const surveyDue = await checkSurveyStatus(learnerId);
        if (surveyDue) {
          showSurveyModal();
        }

        const cfg = await applyArm(learnerId);
        if (!skipArlCycle) {
          try {
            const cycle = await api('/v1/arl', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${token}`,
              },
              body: JSON.stringify({
                learner_id: learnerId,
                refresh_features: true,
              }),
            });
            cacheGuardrailsFromCycle(cycle);
          } catch (cycleErr) {
            console.warn('ARL cycle refresh failed (continuing with previous decision):', cycleErr);
          }
        }
        await loadOLM(learnerId);

        try {
          showLoading('Loading recommendations…');
          const recs = await api('/v1/recommend/recommendations', {
            method: 'POST',
            body: JSON.stringify({
              learner_id: learnerId,
              top_k: CONFIG.RECS_TOP_K,
              strategy: cfg.strategy,
              explain_level: cfg.allowExplain ? 'short' : 'auto',
              exclude_completed: true
            }),
          });

          const hydrated = hydrateRecommendations(recs);
          if ((hydrated.items?.length ?? 0) === 0 && hydrated.progress && (hydrated.progress.active_level === null || hydrated.progress.active_level === undefined)) {
            renderCourseComplete();
          } else {
            renderScatter(learnerId, hydrated, cfg);
          }

          const topKEl = document.getElementById('topK');
          if (topKEl) topKEl.textContent = CONFIG.RECS_TOP_K;
        } catch (e) {
          console.error('Failed to load recommendations:', e);
          const msg = errorMessage(e, 'Failed to load recommendations.');
          const board = document.getElementById('board');
          if (board) {
            board.innerHTML = '';
            const card = document.createElement('div');
            card.className = 'card p-3';
            card.textContent = msg;
            board.appendChild(card);
          }
          showApiError(msg);
        } finally {
          hideLoading();
        }
      } catch (e) {
        console.error('Error loading app:', e);
        const msg = errorMessage(e, 'Failed to load the app. Please try again.');
        showApiError(msg);
        showToast(msg);
      }
    }



window.addEventListener('DOMContentLoaded', async ()=>{
      showActivitySummary();
      bindLessonViewer();
      const featuresReady = loadFeatureFlags();
      initLogin(()=>featuresReady.then(()=>loadApp()));
      const signOutBtn = document.getElementById('btnSignOut');
      if(signOutBtn) signOutBtn.addEventListener('click', signOut);
      const bigToast = document.getElementById('bigToast');
      if(bigToast){
        bigToast.addEventListener('click', hideBigToast);
        const inner = bigToast.querySelector('.big-toast');
        if(inner) inner.addEventListener('click', e=>e.stopPropagation());
        const closeBtn = bigToast.querySelector('button');
        if(closeBtn) closeBtn.addEventListener('click', hideBigToast);
      }
      const oc = document.getElementById('offcanvasCompleted');
      if (oc) {
        oc.addEventListener('show.bs.offcanvas', ()=> loadCompleted(store.learner));
      }
      initExplainDrawer();
      initNoteModal();
      initModeToggle();
      initSurveyModal();
      const backBtn = document.getElementById('btnLessonBack');
      if (backBtn) backBtn.addEventListener('click', ()=> closeLessonView());
      const markBtn = document.getElementById('btnMarkComplete');
      if (markBtn) markBtn.addEventListener('click', ()=>{
        markLessonComplete().catch(err => console.error('Manual completion failed', err));
      });
      await featuresReady;
      // Only auto-load for returning users who already have a token.
      // First-time sign-ups reach loadApp via the initLogin callback
      // after consent completes — calling it here too caused a race
      // where isLoginInProgress was still true, so loadApp returned
      // early and the app never loaded.
      if (store.token && store.learner && !isLoginInProgress()) {
        loadApp();
      }
    });
