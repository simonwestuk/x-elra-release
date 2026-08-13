// Flag to indicate an active login flow is in progress (prevents race conditions)
let loginInProgress = false;

export function setLoginInProgress(v) { loginInProgress = Boolean(v); }
export function isLoginInProgress() { return loginInProgress; }

// Flag to indicate consent was just granted (skip re-check in loadApp)
// Use sessionStorage to persist across async microtasks
const CONSENT_GRANTED_KEY = 'xelra_consent_just_granted';

export function setConsentJustGranted(v) {
  try {
    if (v) {
      sessionStorage.setItem(CONSENT_GRANTED_KEY, '1');
    } else {
      sessionStorage.removeItem(CONSENT_GRANTED_KEY);
    }
  } catch (e) {
    console.warn('sessionStorage not available', e);
  }
}

export function wasConsentJustGranted() {
  try {
    return sessionStorage.getItem(CONSENT_GRANTED_KEY) === '1';
  } catch (e) {
    return false;
  }
}

export const store = {
  set token(v){
    try {
      localStorage.setItem('token', v);
      // Verify the write succeeded (important for mobile browsers)
      if (localStorage.getItem('token') !== v) {
        console.error('localStorage write verification failed for token');
      }
    } catch (e) {
      console.error('Failed to save token to localStorage:', e);
    }
  },
  get token(){
    try {
      return localStorage.getItem('token');
    } catch (e) {
      console.error('Failed to read token from localStorage:', e);
      return null;
    }
  },
  set learner(v){
    try {
      localStorage.setItem('learner_id', v);
      // Verify the write succeeded (important for mobile browsers)
      if (localStorage.getItem('learner_id') !== v) {
        console.error('localStorage write verification failed for learner_id');
      }
    } catch (e) {
      console.error('Failed to save learner_id to localStorage:', e);
    }
  },
  get learner(){
    try {
      return localStorage.getItem('learner_id');
    } catch (e) {
      console.error('Failed to read learner_id from localStorage:', e);
      return null;
    }
  },
  set arm(v){
    try { localStorage.setItem('arm', v); } catch(e) { console.error('Failed to save arm to localStorage:', e); }
  },
  get arm(){
    try { return localStorage.getItem('arm'); } catch(e) { console.error('Failed to read arm from localStorage:', e); return null; }
  },
  set lastSentiment(v){ try{ localStorage.setItem('last_sentiment', JSON.stringify(v)); }catch(_){} },
  get lastSentiment(){ try{ return JSON.parse(localStorage.getItem('last_sentiment')||'null'); }catch(_){ return null; } }
};

export function celebrationsKey(learnerId){ return `skill_celebrations::${learnerId}`; }
export function getCelebratedSkills(learnerId){
  try {
    const raw = localStorage.getItem(celebrationsKey(learnerId));
    if (!raw) return { goal: [], full: [] };
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      const obj = { goal: parsed.map(String), full: [] };
      localStorage.setItem(celebrationsKey(learnerId), JSON.stringify(obj));
      return obj;
    }
    return {
      goal: Array.isArray(parsed.goal) ? parsed.goal.map(String) : [],
      full: Array.isArray(parsed.full) ? parsed.full.map(String) : []
    };
  } catch(_) { return { goal: [], full: [] }; }
}
export function saveCelebratedSkills(learnerId, obj){
  try { localStorage.setItem(celebrationsKey(learnerId), JSON.stringify(obj)); } catch(_) {}
}
export function hasCelebrated(learnerId, skillId, type){
  const s = String(skillId);
  const data = getCelebratedSkills(learnerId);
  return (data[type] || []).includes(s);
}
export function markCelebrated(learnerId, skillId, type){
  const s = String(skillId);
  const data = getCelebratedSkills(learnerId);
  if (!data[type].includes(s)) { data[type].push(s); saveCelebratedSkills(learnerId, data); }
}
export function unmarkCelebrated(learnerId, skillId, type){
  const s = String(skillId);
  const data = getCelebratedSkills(learnerId);
  data[type] = (data[type] || []).filter(x=>x!==s);
  saveCelebratedSkills(learnerId, data);
}
