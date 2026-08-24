/**
 * Policy and ARM Configuration for X-ELRA
 *
 * Contains experiment arm definitions, policy/routine details,
 * and helper functions for policy-related UI rendering.
 */

/**
 * Experiment ARM configurations
 * Maps group buckets (T, A, B) to their strategy and feature settings.
 *
 * All groups use the same hybrid recommender with identical weights and
 * sentiment-aware personalisation.  Only the explanation layer differs:
 *
 *   T = ARL Treatment  – Process-level structured explanations
 *                         (mode/why/next/exit + sentiment panel; no model-level card)
 *   A = B1 Control     – Traditional post-hoc feature attribution
 *                         (SHAP only, no regulatory mode, no sentiment panel)
 *   B = B3 Control     – OLM-only transparency (progress/mastery display,
 *                         no explanations of decision processes)
 *
 * allowSentiment controls the process-level sentiment panel ("Your last
 * reflection was positive").  The S signal still appears in SHAP attribution
 * for any arm with allowExplain, since all arms use sentiment in the model.
 */
export const ARM_MAP = {
  T: { strategy: 'hybrid', allowExplain: true, allowSentiment: false, allowRegulatoryMode: true, label: 'ARL Treatment (governed adaptive + structured explanations)' },
  A: { strategy: 'hybrid', allowExplain: true, allowSentiment: false, allowRegulatoryMode: false, label: 'B1 Control (model-driven + post-hoc feature attribution)' },
  B: { strategy: 'hybrid', allowExplain: false, allowSentiment: false, allowRegulatoryMode: false, label: 'B3 Control (OLM progress display)' },
};

/**
 * ARL Control Routine details (P1-P8)
 * Matches config/arl_routines.yaml
 */
export const POLICY_DETAILS = [
  { id: 'P1', title: 'Orientation Safety Net', snippet: 'gives new learners a guided starting playlist' },
  { id: 'P2', title: 'Data Integrity Control Routine', snippet: 'repairs missing mastery data before personalisation' },
  { id: 'P3', title: 'Struggling Learner Uplift', snippet: 'rebuilds fundamentals when progress stalls' },
  { id: 'P4', title: 'Lapsed Learner Re-engagement', snippet: 'nudges you back after time away' },
  { id: 'P5', title: 'Goal Attainment Accelerator', snippet: 'amplifies momentum on active goals' },
  { id: 'P6', title: 'Mastery Consolidation', snippet: 'adds deliberate practice once mastery is high' },
  { id: 'P7', title: 'Default Hybrid Pathway', snippet: 'keeps recommendations balanced when no control routine fires' },
  { id: 'P8', title: 'Affective Overload Intervention', snippet: 'suggests a break and fundamentals reset when confusion or frustration is detected' },
];

// Derived lookup maps
export const POLICY_TITLE_BY_ID = Object.fromEntries(
  POLICY_DETAILS.map(detail => [detail.id, detail.title])
);

export const POLICY_SNIPPETS = Object.fromEntries(
  POLICY_DETAILS.map(detail => [detail.title, detail.snippet])
);

// Baseline policies that apply to all learners
export const BASELINE_IDS = ['P1', 'P2', 'P7'];
export const BASELINE_GUARDRAILS = BASELINE_IDS.map(id => POLICY_TITLE_BY_ID[id]);

/**
 * Model signal descriptors for XAI explanations
 */
export const MODEL_SIGNAL_DESCRIPTORS = {
  C: {
    label: 'Content match',
    description: 'how closely the resource covers the skills you are practising.',
  },
  P: {
    label: 'Popularity',
    description: 'how many learners successfully engage with this resource.',
  },
  CF: {
    label: 'Similar learners',
    description: 'what people on a similar journey have found helpful.',
  },
  S: {
    label: 'Sentiment alignment',
    description: 'how well the tone and pacing fit your recent reflections.',
  },
  D: {
    label: 'Variety balance',
    description: 'how the system keeps your path varied and avoids repetition.',
  },
};

/**
 * Resolve a list of policy IDs/names to their full titles
 * @param {Array} list - List of policy IDs or names
 * @returns {Array} Resolved policy titles
 */
export function resolvePolicyList(list) {
  if (!Array.isArray(list) || !list.length) {
    return BASELINE_GUARDRAILS;
  }
  return list.map(name => POLICY_TITLE_BY_ID[name] || name);
}

/**
 * Get the description/snippet for a policy
 * @param {string} name - Policy ID or title
 * @returns {string} Policy description
 */
export function describePolicy(name) {
  if (!name) return 'supporting control routine';
  const direct = POLICY_SNIPPETS[name];
  if (direct) {
    return direct;
  }
  const lookup = String(name).toLowerCase();
  const detail = POLICY_DETAILS.find(
    entry => entry.id.toLowerCase() === lookup || entry.title.toLowerCase() === lookup
  );
  return detail ? detail.snippet : 'supporting control routine';
}

/**
 * Generate tooltip text for a list of policies
 * @param {Array} list - List of policy names
 * @returns {string} Formatted tooltip text
 */
export function policyTooltipText(list) {
  return resolvePolicyList(list)
    .map(name => `${name}: ${describePolicy(name)}`)
    .join(' • ');
}

/**
 * Generate a sentence summary of policies
 * @param {Array} list - List of policy names
 * @returns {string} Sentence summary
 */
export function policySentenceSummary(list) {
  const resolved = resolvePolicyList(list).map(name => `${name} (${describePolicy(name)})`);
  if (!resolved.length) {
    return 'baseline control routines';
  }
  if (resolved.length === 1) {
    return resolved[0];
  }
  if (resolved.length === 2) {
    return `${resolved[0]} and ${resolved[1]}`;
  }
  const extraCount = resolved.length - 2;
  return `${resolved[0]} and ${resolved[1]}, plus ${extraCount} further control routine${extraCount > 1 ? 's' : ''}`;
}

/**
 * Generate a detailed list of policies
 * @param {Array} list - List of policy names
 * @returns {string} Semicolon-separated list
 */
export function policyDetailListText(list) {
  return resolvePolicyList(list)
    .map(name => `${name} — ${describePolicy(name)}`)
    .join('; ');
}

/**
 * Generate a short summary of policies
 * @param {Array} list - List of policy names
 * @returns {string} Short summary
 */
export function policyShortSummary(list) {
  const resolved = resolvePolicyList(list);
  if (!resolved.length) {
    return 'baseline control routines';
  }
  if (resolved.length === 1) {
    return resolved[0];
  }
  return `${resolved[0]} and ${resolved[1]}`;
}

/**
 * Generate a tag label for policies (e.g., for badges)
 * @param {Array} list - List of policy names
 * @returns {string} Tag label
 */
export function policyTagLabel(list) {
  const resolved = resolvePolicyList(list);
  if (!resolved.length) {
    return 'Baseline control routines';
  }
  if (resolved.length === 1) {
    return resolved[0];
  }
  return `${resolved[0]} + ${resolved.length - 1} more`;
}

/**
 * Get descriptor for a model signal key
 * @param {string} key - Signal key (C, P, CF, S, D)
 * @returns {Object} Signal descriptor with label and description
 */
export function describeModelSignal(key) {
  return MODEL_SIGNAL_DESCRIPTORS[key] || {
    label: key,
    description: 'model insight used in this recommendation.',
  };
}

/**
 * Get ARM configuration by group bucket
 * @param {string} arm - Group bucket (T, A, B)
 * @returns {Object} ARM configuration
 */
export function getArmConfig(arm) {
  return ARM_MAP[arm] || ARM_MAP['T'];
}

export default {
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
};
