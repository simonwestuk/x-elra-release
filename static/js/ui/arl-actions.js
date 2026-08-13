/**
 * ARL Action Handlers - UI components for ARL action types
 *
 * This module handles rendering of ARL action types:
 * - SUGGEST_BREAK: Shows a break toast with beginner-friendly guidance
 * - SPACED_REVIEW: Shows a scheduled review indicator
 * - Mode transition notifications
 * - SHOW_EXPLANATION: Shows explanation toasts
 *
 * For research study: ensures all intervention types are properly delivered
 * and visible to participants.
 */

// Track active break timers and review schedules
let activeBreakTimer = null;
let scheduledReviews = [];
let lastKnownMode = null;

/**
 * MODE_LABELS for learner-friendly mode names
 * These describe what the system is doing to help the learner
 */
const MODE_LABELS = {
  cold_start: 'Discovering',
  orientation: 'Exploring',
  nominal: 'Progressing',
  struggling: 'Supporting',
  lapsed: 'Reconnecting',
  accelerating: 'Advancing',
  consolidating: 'Reinforcing',
  diagnostic: 'Assessing',
  cooldown: 'Resting',
};

/**
 * Break tips for different modalities - beginner-friendly guidance
 */
const BREAK_TIPS = {
  stretch: [
    'Stand up and stretch your arms above your head',
    'Roll your shoulders back a few times',
    'Look away from the screen at something distant',
  ],
  rest: [
    'Step away from the problem — your brain keeps working in the background',
    'When you return, re-read your code from the beginning',
    'Fresh eyes often spot what tired eyes miss',
  ],
  walk: [
    'A short walk helps clear your mind',
    'Think about the problem in plain English while walking',
    'Movement helps memory consolidation',
  ],
  hydrate: [
    'Stay hydrated — it helps concentration',
    'Get a glass of water or a warm drink',
    'Use this time to rest your eyes too',
  ],
  eyes: [
    'Look at something 6 metres away for 20 seconds',
    'Blink several times to refresh your eyes',
    'Reduce screen brightness if it feels harsh',
  ],
  default: [
    'Step away from the screen for a few minutes',
    'When stuck, explaining the problem aloud often helps',
    'It\'s normal to need breaks — they improve learning',
  ],
};

/**
 * Create and show a break suggestion toast
 * @param {Object} params - Break suggestion parameters
 * @param {number} params.duration_minutes - Suggested break duration
 * @param {string} params.modality - Type of break (stretch, rest, etc.)
 * @param {string} params.reason - Why the break is suggested
 * @param {string} params.prompt - Message to show the learner
 */
export function showBreakSuggestion(params = {}) {
  const {
    duration_minutes = 5,
    modality = 'rest',
    reason = 'wellbeing',
    prompt = '',
  } = params;

  // Clear any existing break timer
  if (activeBreakTimer) {
    clearInterval(activeBreakTimer);
    activeBreakTimer = null;
  }

  let breakToast = document.getElementById('breakSuggestionToast');
  if (!breakToast) {
    breakToast = createBreakToastElement();
    document.body.appendChild(breakToast);
  }

  // Generate contextual message based on reason
  let message = prompt;
  if (!message) {
    if (reason === 'error_burst' || reason === 'debugging') {
      message = 'You\'ve been working hard on this. A short break can help you see the problem with fresh eyes.';
    } else if (reason === 'extended_session') {
      message = 'You\'ve been learning for a while. Taking breaks helps your brain consolidate what you\'ve learnt.';
    } else {
      message = 'A short break can help you stay focused and make better progress.';
    }
  }

  // Get tips for this modality
  const tips = BREAK_TIPS[modality] || BREAK_TIPS.default;

  const icon = getModalityIcon(modality);
  const titleEl = breakToast.querySelector('.break-toast-title');
  const messageEl = breakToast.querySelector('.break-toast-message');
  const tipsEl = breakToast.querySelector('.break-toast-tips');
  const timerEl = breakToast.querySelector('.break-toast-timer');
  const iconEl = breakToast.querySelector('.break-toast-icon');

  if (iconEl) iconEl.textContent = icon;
  if (titleEl) titleEl.textContent = `Time for a ${modality} break`;
  if (messageEl) messageEl.textContent = message;
  if (tipsEl) {
    tipsEl.innerHTML = '<ul>' + tips.map(tip => `<li>${escapeHtml(tip)}</li>`).join('') + '</ul>';
  }

  // Show with timer
  breakToast.classList.add('show');
  breakToast.setAttribute('aria-hidden', 'false');

  // Optional countdown timer
  if (duration_minutes > 0 && timerEl) {
    let remainingSeconds = duration_minutes * 60;
    timerEl.textContent = formatTime(remainingSeconds);
    timerEl.style.display = 'block';

    activeBreakTimer = setInterval(() => {
      remainingSeconds--;
      if (remainingSeconds <= 0) {
        clearInterval(activeBreakTimer);
        activeBreakTimer = null;
        timerEl.textContent = 'Break complete!';
        setTimeout(() => hideBreakSuggestion(), 3000);
      } else {
        timerEl.textContent = formatTime(remainingSeconds);
      }
    }, 1000);
  }

  // Log telemetry event
  logActionDelivery('SUGGEST_BREAK', params);
}

/**
 * Hide the break suggestion toast
 */
export function hideBreakSuggestion() {
  const breakToast = document.getElementById('breakSuggestionToast');
  if (breakToast) {
    breakToast.classList.remove('show');
    breakToast.setAttribute('aria-hidden', 'true');
  }
  if (activeBreakTimer) {
    clearInterval(activeBreakTimer);
    activeBreakTimer = null;
  }
}

/**
 * Show spaced review schedule indicator
 * @param {Object} params - Spaced review parameters
 * @param {number} params.base_interval_minutes - Initial interval
 * @param {number} params.interval_step_minutes - Interval increase per review
 * @param {Array} params.items - Items to review
 */
export function showSpacedReviewSchedule(params = {}) {
  const {
    base_interval_minutes = 10,
    interval_step_minutes = 5,
    items = [],
  } = params;

  if (!items.length) return;

  scheduledReviews = items.map((item, index) => ({
    item_id: item.item_id,
    difficulty: item.difficulty || 'medium',
    scheduled_at: Date.now() + (base_interval_minutes + interval_step_minutes * index) * 60 * 1000,
  }));

  let reviewIndicator = document.getElementById('spacedReviewIndicator');
  if (!reviewIndicator) {
    reviewIndicator = createReviewIndicatorElement();
    const appContainer = document.getElementById('viewApp') || document.body;
    appContainer.appendChild(reviewIndicator);
  }

  const countEl = reviewIndicator.querySelector('.review-count');
  const nextEl = reviewIndicator.querySelector('.review-next-time');

  if (countEl) countEl.textContent = `${items.length} review${items.length > 1 ? 's' : ''} scheduled`;
  if (nextEl && scheduledReviews.length) {
    const nextReview = scheduledReviews[0];
    const minutesUntil = Math.round((nextReview.scheduled_at - Date.now()) / 60000);
    nextEl.textContent = `Next in ${minutesUntil} min`;
  }

  reviewIndicator.classList.add('show');

  // Log telemetry event
  logActionDelivery('SPACED_REVIEW', params);
}

/**
 * Show mode transition notification
 * @param {string} oldMode - Previous mode
 * @param {string} newMode - New mode
 * @param {string} reason - Reason for transition
 */
export function showModeTransitionNotification(oldMode, newMode, reason = '') {
  if (!oldMode || !newMode || oldMode === newMode) return;

  const newLabel = MODE_LABELS[newMode] || newMode;

  // Update and animate the OLM mode labels instead of showing a popup
  const modeLabels = document.querySelectorAll('#modeLabel, #modeLabelLesson');
  modeLabels.forEach((label) => {
    if (label) {
      // Update the text
      label.textContent = newLabel;
      // Trigger animation
      label.classList.remove('mode-transition');
      // Force reflow to restart animation
      void label.offsetWidth;
      label.classList.add('mode-transition');
      // Remove animation class after it completes
      setTimeout(() => label.classList.remove('mode-transition'), 1500);
    }
  });

  // Also animate the regulatory mode card container for emphasis
  const modeCards = document.querySelectorAll('#regulatoryModeCard, #regulatoryModeCardLesson');
  modeCards.forEach((card) => {
    if (card) {
      card.classList.add('arl-loop-animate');
      setTimeout(() => card.classList.remove('arl-loop-animate'), 1100);
    }
  });

  // Log telemetry event
  logActionDelivery('MODE_TRANSITION', { old_mode: oldMode, new_mode: newMode, reason });
}

/**
 * Show explanation action (enhanced toast with CTA)
 * @param {Object} params - Explanation parameters
 * @param {string} params.message - Explanation message
 * @param {string} params.tone - Message tone
 * @param {Array} params.topics - Related topics
 * @param {string} params.cta - Call to action text
 */
export function showExplanationAction(params = {}) {
  const {
    message = '',
    tone = 'neutral',
    topics = [],
    cta = '',
  } = params;

  if (!message) return;

  let explainToast = document.getElementById('explanationActionToast');
  if (!explainToast) {
    explainToast = createExplanationToastElement();
    document.body.appendChild(explainToast);
  }

  const messageEl = explainToast.querySelector('.explain-toast-message');
  const topicsEl = explainToast.querySelector('.explain-toast-topics');
  const ctaEl = explainToast.querySelector('.explain-toast-cta');

  if (messageEl) messageEl.textContent = message;
  if (topicsEl && topics.length) {
    topicsEl.innerHTML = topics.map(t => `<span class="badge bg-secondary me-1">${escapeHtml(t)}</span>`).join('');
  }
  if (ctaEl) {
    if (cta) {
      ctaEl.textContent = cta;
      ctaEl.style.display = 'inline-block';
    } else {
      ctaEl.style.display = 'none';
    }
  }

  // Apply tone styling
  explainToast.className = `explanation-action-toast tone-${tone} show`;

  // Auto-hide after 8 seconds (longer for explanations)
  setTimeout(() => {
    explainToast.classList.remove('show');
  }, 8000);

  // Log telemetry event
  logActionDelivery('SHOW_EXPLANATION', params);
}

/**
 * Process ARL cycle result and trigger appropriate UI actions
 * @param {Object} cycle - ARL cycle result
 */
export function processARLCycleActions(cycle) {
  if (!cycle || typeof cycle !== 'object') return;

  const stateBefore = cycle.controller_state_before;
  const stateAfter = cycle.controller_state_after;

  if (stateBefore && stateAfter) {
    const oldMode = stateBefore.mode;
    const newMode = stateAfter.mode;

    if (oldMode !== newMode) {
      const reason = cycle.learner_facing_fields?.why || '';
      showModeTransitionNotification(oldMode, newMode, reason);
    }

    // Update last known mode
    lastKnownMode = newMode;
  }

  const routineResults = cycle.routine_results || cycle.policy_results || [];
  for (const result of routineResults) {
    const isExecuted = result.outcome === 'EXECUTED_ACTION' ||
                       result.outcome === 'EXECUTED_NO_ACTION' ||
                       (!result.skipped && !result.error);

    if (!isExecuted) continue;

    const actions = result.actions || [];
    for (const actionResult of actions) {
      // ActionResult structure: {action_type, payload, action_name, ...}
      if (!actionResult || actionResult.error) continue;

      const action = {
        type: actionResult.action_type || actionResult.type,
        params: actionResult.payload || actionResult.params || {},
        name: actionResult.action_name || actionResult.name,
      };
      processAction(action);
    }
  }

  if (cycle.decision && cycle.decision.actions) {
    for (const action of cycle.decision.actions) {
      processAction(action);
    }
  }
}

/**
 * Process a single action and trigger appropriate UI
 * @param {Object} action - Action object with type and params
 */
function processAction(action) {
  if (!action || !action.type) return;

  const actionType = action.type.toUpperCase();
  const params = action.params || {};

  switch (actionType) {
    case 'SUGGEST_BREAK':
      showBreakSuggestion(params);
      break;

    case 'SPACED_REVIEW':
      showSpacedReviewSchedule(params);
      break;

    case 'ASSIGN_DEBUG_EXERCISE':
      break;

    case 'SHOW_EXPLANATION':
      showExplanationAction(params);
      break;

    case 'FETCH_RECOMMENDATIONS':
    case 'LOG_IMPRESSIONS':
      break;

    default:
      break;
  }
}

// ============ Helper Functions ============

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = seconds % 60;
  return `${mins}:${secs.toString().padStart(2, '0')}`;
}

function getModalityIcon(modality) {
  const icons = {
    stretch: '🧘',
    rest: '☕',
    walk: '🚶',
    hydrate: '💧',
    eyes: '👀',
  };
  return icons[modality] || '⏸️';
}

function getModeColor(mode) {
  const colors = {
    cold_start: 'info',
    orientation: 'info',
    nominal: 'primary',
    struggling: 'warning',
    lapsed: 'secondary',
    accelerating: 'success',
    consolidating: 'success',
    diagnostic: 'info',
    cooldown: 'secondary',
  };
  return colors[mode] || 'primary';
}

function escapeHtml(str) {
  if (typeof str !== 'string') return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

function logActionDelivery(actionType, params) {
  // Emit custom event for telemetry integration
  const event = new CustomEvent('xelra:action-delivered', {
    detail: { actionType, params, timestamp: Date.now() },
  });
  window.dispatchEvent(event);
}

// ============ Element Creators ============

function createBreakToastElement() {
  const toast = document.createElement('div');
  toast.id = 'breakSuggestionToast';
  toast.className = 'break-suggestion-toast';
  toast.setAttribute('role', 'alert');
  toast.setAttribute('aria-live', 'polite');
  toast.setAttribute('aria-hidden', 'true');
  toast.innerHTML = `
    <div class="break-toast-content">
      <button type="button" class="break-toast-close" aria-label="Dismiss">&times;</button>
      <div class="break-toast-icon">⏸️</div>
      <div class="break-toast-body">
        <div class="break-toast-title">Time for a break</div>
        <div class="break-toast-message">Consider taking a short break to stay refreshed.</div>
        <div class="break-toast-tips"></div>
        <div class="break-toast-timer" style="display:none;">5:00</div>
      </div>
      <div class="break-toast-actions">
        <button type="button" class="btn btn-sm btn-outline-light break-toast-skip">Not now</button>
        <button type="button" class="btn btn-sm btn-light break-toast-start">Take a break</button>
      </div>
    </div>
  `;

  // Bind close button
  const closeBtn = toast.querySelector('.break-toast-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', hideBreakSuggestion);
  }

  const skipBtn = toast.querySelector('.break-toast-skip');
  if (skipBtn) {
    skipBtn.addEventListener('click', hideBreakSuggestion);
  }

  return toast;
}

function createReviewIndicatorElement() {
  const indicator = document.createElement('div');
  indicator.id = 'spacedReviewIndicator';
  indicator.className = 'spaced-review-indicator';
  indicator.setAttribute('role', 'status');
  indicator.innerHTML = `
    <div class="review-indicator-icon">📚</div>
    <div class="review-indicator-body">
      <div class="review-count">Reviews scheduled</div>
      <div class="review-next-time"></div>
    </div>
    <button type="button" class="review-indicator-close" aria-label="Dismiss">&times;</button>
  `;

  const closeBtn = indicator.querySelector('.review-indicator-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      indicator.classList.remove('show');
    });
  }

  return indicator;
}

function createModeTransitionToastElement() {
  const toast = document.createElement('div');
  toast.id = 'modeTransitionToast';
  toast.className = 'mode-transition-toast';
  toast.setAttribute('role', 'status');
  toast.setAttribute('aria-live', 'polite');
  toast.setAttribute('aria-hidden', 'true');
  toast.innerHTML = `
    <div class="mode-toast-content">
      <div class="mode-toast-icon">🔄</div>
      <div class="mode-toast-body">
        <div class="mode-toast-title">Mode changed</div>
        <div class="mode-toast-message"></div>
      </div>
      <span class="mode-toast-badge badge bg-primary">Learning</span>
    </div>
  `;

  toast.addEventListener('click', () => {
    toast.classList.remove('show');
    toast.setAttribute('aria-hidden', 'true');
  });

  return toast;
}

function createExplanationToastElement() {
  const toast = document.createElement('div');
  toast.id = 'explanationActionToast';
  toast.className = 'explanation-action-toast';
  toast.setAttribute('role', 'alert');
  toast.innerHTML = `
    <div class="explain-toast-content">
      <button type="button" class="explain-toast-close" aria-label="Dismiss">&times;</button>
      <div class="explain-toast-icon">💡</div>
      <div class="explain-toast-body">
        <div class="explain-toast-message"></div>
        <div class="explain-toast-topics"></div>
        <button type="button" class="btn btn-sm btn-primary explain-toast-cta" style="display:none;"></button>
      </div>
    </div>
  `;

  const closeBtn = toast.querySelector('.explain-toast-close');
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      toast.classList.remove('show');
    });
  }

  return toast;
}

// ============ Exports for Global Access ============

window.ARLActions = {
  showBreakSuggestion,
  hideBreakSuggestion,
  showSpacedReviewSchedule,
  showModeTransitionNotification,
  showExplanationAction,
  processARLCycleActions,
};

export default {
  showBreakSuggestion,
  hideBreakSuggestion,
  showSpacedReviewSchedule,
  showModeTransitionNotification,
  showExplanationAction,
  processARLCycleActions,
};
