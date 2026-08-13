/**
 * Enhanced OLM Panel Rendering - Section 4.6 Alignment
 *
 * This module handles rendering of ARL decision trace information
 * in learner-facing terms, aligned with Section 4.6 of the journal article.
 */

/**
 * Update the regulatory mode panel with Section 4.6 learner-facing fields
 * @param {Object} arlCycle - The ARL cycle result with learner_facing_fields
 * @param {string} panelSuffix - Optional suffix for element IDs (e.g., "Lesson")
 */
export function updateRegulatoryModePanel(arlCycle, panelSuffix = '') {
  if (!arlCycle || !arlCycle.learner_facing_fields) {
    console.warn('No learner_facing_fields in ARL cycle data');
    return;
  }

  const fields = arlCycle.learner_facing_fields;

  // Update mode label (Section 4.6: "Mode: Support")
  const modeLabel = document.getElementById(`modeLabel${panelSuffix}`);
  if (modeLabel && fields.mode_label) {
    modeLabel.textContent = fields.mode_label;
    // Update mode class for styling
    modeLabel.className = `mode-label mode-${fields.mode_label.toLowerCase().replace(/\s+/g, '-')}`;
  }

  // Update "Why" (Section 4.6: "Why: You appear to be finding this step difficult")
  const modeWhy = document.getElementById(`modeWhy${panelSuffix}`);
  if (modeWhy && fields.why) {
    modeWhy.textContent = fields.why;
  }

  // Update "What the system will do" (Section 4.6)
  const modeWhatSystemWillDo = document.getElementById(`modeWhatSystemWillDo${panelSuffix}`);
  if (modeWhatSystemWillDo && fields.system_behaviour) {
    modeWhatSystemWillDo.textContent = fields.system_behaviour;
  }

  // Update "What you should do next" (Section 4.6)
  const modeWhatNext = document.getElementById(`modeWhatNext${panelSuffix}`);
  if (modeWhatNext && fields.expected_action) {
    modeWhatNext.textContent = fields.expected_action;
  }

  // Update "What will change this" (Section 4.6: exit conditions)
  const modeExitConditions = document.getElementById(`modeExitConditions${panelSuffix}`);
  if (modeExitConditions && fields.exit_conditions) {
    modeExitConditions.textContent = fields.exit_conditions;
  }

  // Remove any existing suppression warning (these are internal debug messages, not for learners)
  const regulatoryCard = document.getElementById(`regulatoryModeCard${panelSuffix}`);
  if (regulatoryCard) {
    const existingWarning = regulatoryCard.querySelector('.alert-warning');
    if (existingWarning) {
      existingWarning.remove();
    }
  }
}

/**
 * Build HTML for routine evaluation path (Section 4.4)
 * @param {Array} routinePath - Array of routine evaluation results
 * @returns {string} HTML string
 */
export function buildRoutinePathHtml(routinePath) {
  if (!Array.isArray(routinePath) || routinePath.length === 0) {
    return '<p class="text-muted mb-0"><em>No routine evaluation data available</em></p>';
  }

  const routineItems = routinePath
    .map((result, index) => {
      const outcome = result.outcome || (result.skipped ? 'SKIPPED' : 'EXECUTED');
      const reason = result.reason || result.skip_reason || result.error || 'No reason provided';
      const routineName = result.routine_name || result.routine?.name || `Routine ${index + 1}`;

      // Determine badge class based on outcome
      let badgeClass = 'skipped';
      if (outcome === 'BLOCKED') badgeClass = 'blocked';
      if (outcome === 'EXECUTED_ACTION' || outcome === 'EXECUTED') badgeClass = 'executed';

      return `
        <div class="explain-item">
          <div class="d-flex align-items-center justify-content-between mb-1">
            <span class="fw-semibold">${escapeHtml(routineName)}</span>
            <span class="routine-outcome-badge ${badgeClass}">${outcome}</span>
          </div>
          <p class="explain-text small mb-0">${escapeHtml(reason)}</p>
          ${result.mode_transition ? `<div class="mt-1"><small class="text-info">→ Mode transition to: ${escapeHtml(result.mode_transition)}</small></div>` : ''}
        </div>
      `;
    })
    .join('');

  return routineItems;
}

/**
 * Build HTML for decision information (Section 4.4)
 * @param {Object} decision - Decision object from ARL cycle
 * @returns {string} HTML string
 */
export function buildDecisionHtml(decision) {
  if (!decision) {
    return '<p class="text-muted mb-0"><em>No decision data available</em></p>';
  }

  // Appendix A.3 decision schema: {action, source_routine}
  const actionName = decision.action || null;
  const sourceRoutine = decision.source_routine || null;

  return `
    <div class="explain-item">
      <span class="explain-label">Decision Type:</span>
      <span class="explain-value ${!actionName ? 'text-warning' : 'text-success'}">${actionName ? 'ACTION' : 'NO_ACTION'}</span>
    </div>
    ${actionName ? `
      <div class="explain-item">
        <span class="explain-label">Selected Action:</span>
        <span class="explain-value">${escapeHtml(actionName)}</span>
      </div>
      <div class="explain-item">
        <span class="explain-label">Source Routine:</span>
        <span class="explain-value">${escapeHtml(sourceRoutine || 'N/A')}</span>
      </div>
    ` : `
      <div class="explain-item">
        <p class="explain-text mb-0">
          <small>No action was taken at this decision point. This is a deliberate regulatory decision.</small>
        </p>
      </div>
    `}
  `;
}

/**
 * Update the explanation drawer with learner-facing content from the ARL decision trace
 * @param {Object} arlCycle - The ARL cycle result
 * @param {Object} item - The recommendation item (optional, not used in learner-facing view)
 */
export function updateExplanationDrawer(arlCycle, item) {
  if (!arlCycle || !arlCycle.learner_facing_fields) {
    console.warn('No learner_facing_fields in ARL cycle data for explanation drawer');
    return;
  }

  const fields = arlCycle.learner_facing_fields;

  // Update mode label
  const explainMode = document.getElementById('explainMode');
  if (explainMode && fields.mode_label) {
    explainMode.textContent = fields.mode_label;
  }

  // Update "Why"
  const explainModeWhy = document.getElementById('explainModeWhy');
  if (explainModeWhy && fields.why) {
    explainModeWhy.textContent = fields.why;
  }

  // Update "What the system will do"
  const explainWhatSystemWillDo = document.getElementById('explainWhatSystemWillDo');
  if (explainWhatSystemWillDo && fields.system_behaviour) {
    explainWhatSystemWillDo.textContent = fields.system_behaviour;
  }

  // Update "What you should do next"
  const explainWhatNext = document.getElementById('explainWhatNext');
  if (explainWhatNext && fields.expected_action) {
    explainWhatNext.textContent = fields.expected_action;
  }

  // Update "What will change this"
  const explainExitConditions = document.getElementById('explainExitConditions');
  if (explainExitConditions && fields.exit_conditions) {
    explainExitConditions.textContent = fields.exit_conditions;
  }
}

/**
 * Escape HTML to prevent XSS
 * @param {string} str - String to escape
 * @returns {string} Escaped string
 */
function escapeHtml(str) {
  if (typeof str !== 'string') return '';
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// Make functions available globally for existing code integration
window.ARLEnhanced = {
  updateRegulatoryModePanel,
  buildRoutinePathHtml,
  buildDecisionHtml,
  updateExplanationDrawer
};
