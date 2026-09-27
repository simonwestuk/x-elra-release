import { api } from './api.js';
import { store, setLoginInProgress, setConsentJustGranted } from './store.js';
import { showToast } from '../ui/ui.js';

let resendInt = null;
let consentTimerInt = null;
const RESEND_WAIT_SECONDS = 15 * 60;
const CONSENT_WAIT_SECONDS = 30;

// Consent state
let consentCodeRequired = false;

// Simple email validation regex
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function showEmailError(msg) {
  const el = document.getElementById('emailError');
  if (el) el.textContent = msg;
}

function clearEmailError() {
  const el = document.getElementById('emailError');
  if (el) el.textContent = '';
}

function showCodeError(msg) {
  const el = document.getElementById('codeError');
  if (el) el.textContent = msg;
}

function clearCodeError() {
  const el = document.getElementById('codeError');
  if (el) el.textContent = '';
}

function formatTime(seconds){
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}

function getOtpInputs(){
  return Array.from(document.querySelectorAll('.otp-input'));
}

function getCode(){
  return getOtpInputs().map(i => i.value).join('');
}

export function resetLogin(){
  const emailEl = document.getElementById('email');
  const stepEmail = document.getElementById('stepEmail');
  const stepCode = document.getElementById('stepCode');
  const stepConsent = document.getElementById('stepConsent');
  const loginSheet = document.querySelector('.login-sheet');
  const sentTo = document.getElementById('sentTo');
  const devCode = document.getElementById('devCode');
  const linkResend = document.getElementById('linkResend');
  if (emailEl) emailEl.value = '';
  getOtpInputs().forEach(i => { i.value = ''; });
  if (stepEmail) stepEmail.classList.remove('d-none');
  if (stepCode) stepCode.classList.add('d-none');
  if (stepConsent) stepConsent.classList.add('d-none');
  if (loginSheet) loginSheet.classList.remove('consent-active');
  if (sentTo) sentTo.textContent = '';
  if (devCode) devCode.textContent = '';
  if (linkResend) linkResend.classList.add('disabled');
  const timerEl = document.getElementById('resendTimer');
  if (timerEl) timerEl.textContent = 'in ' + formatTime(RESEND_WAIT_SECONDS);
  if (resendInt) clearInterval(resendInt);
  if (consentTimerInt) clearInterval(consentTimerInt);
}

export function signOut(){
  try {
    localStorage.clear();
  } catch (err) {
    console.warn('Failed to clear localStorage on sign out', err);
    localStorage.removeItem('token');
    localStorage.removeItem('learner_id');
  }
  resetLogin();
  const login = document.getElementById('viewLogin');
  const app = document.getElementById('viewApp');
  const btn = document.getElementById('btnSignOut');
  const navActivity = document.getElementById('navActivityIndicator');
  const navAllSkills = document.getElementById('btnAllSkillsNav');
  // Use setProperty with 'important' for iOS Safari compatibility
  if (login) {
    login.style.setProperty('display', 'flex', 'important');
    // Force repaint on iOS Safari
    void login.offsetHeight;
  }
  if (app) app.style.setProperty('display', 'none', 'important');
  if (btn) btn.style.display = 'none';
  if (navActivity) navActivity.style.display = 'none';
  if (navAllSkills) navAllSkills.style.display = 'none';
}

async function requestCode(){
  const email = document.getElementById('email').value.trim();
  clearEmailError();
  if(!email) {
    showEmailError('Please enter your email address');
    return;
  }
  if(!EMAIL_RE.test(email)) {
    showEmailError('Please enter a valid email address');
    return;
  }
  let res;
  try {
    res = await api('/v1/standalone/request_code', {
      method: 'POST',
      body: JSON.stringify({ email })
    });
  } catch (err) {
    showEmailError(err.message || 'Something went wrong. Please try again.');
    return;
  }

  // Handle failed email delivery
  if (res.delivery === 'failed') {
    showEmailError(res.error || 'Email delivery failed. Please try again.');
    return;
  }

  const stepEmail = document.getElementById('stepEmail');
  const stepCode = document.getElementById('stepCode');
  if (stepEmail) stepEmail.classList.add('d-none');
  if (stepCode) stepCode.classList.remove('d-none');
  const sentTo = document.getElementById('sentTo');
  if (sentTo) sentTo.textContent = email;
  const devCode = document.getElementById('devCode');
  if (devCode) {
    if (res.delivery === 'dev' && res.code) {
      // Dev mode: show code prominently
      devCode.innerHTML = `<span class="badge bg-warning text-dark">DEV MODE</span> Your code: <strong>${res.code}</strong>`;
    } else if (res.code) {
      // Legacy fallback
      devCode.textContent = 'DEV: your code is ' + res.code;
    } else {
      devCode.textContent = '';
    }
  }
  const inputs = getOtpInputs();
  inputs.forEach(i => { i.value = ''; });
  if (inputs[0]) inputs[0].focus();
  startResendTimer();
}

// Store pending callback for after consent
let pendingOnSuccess = null;

async function verifyCode(onSuccess){
  const email = document.getElementById('email').value.trim();
  const code = getCode();
  clearCodeError();
  const res = await api('/v1/standalone/verify_code', {
    method: 'POST',
    body: JSON.stringify({ email, code })
  });
  if (res.ok){
    store.token = res.token;
    store.learner = res.learner_id;
    store.arm = res.arm;
    // Mark login as in progress to prevent race conditions with loadApp()
    setLoginInProgress(true);

    // Check if consent has already been given
    try {
      const consentCheck = await api(`/v1/telemetry/consent/${encodeURIComponent(res.learner_id)}`);
      if (consentCheck && consentCheck.consent_given) {
        // Already consented - proceed directly to app
        completeLogin(onSuccess, res.learner_id);
        return;
      }
    } catch (e) {
      console.warn('Consent check failed, showing consent step', e);
    }

    // Show consent step (Step 3)
    pendingOnSuccess = () => onSuccess(res.learner_id);
    showConsentStep();
  } else {
    showCodeError('Invalid code. Please check and try again.');
    showToast('Verification failed');
    // Clear OTP inputs for retry
    getOtpInputs().forEach(i => { i.value = ''; });
    const firstInput = getOtpInputs()[0];
    if (firstInput) firstInput.focus();
  }
}

async function showConsentStep() {
  const stepCode = document.getElementById('stepCode');
  const stepConsent = document.getElementById('stepConsent');
  const loginSheet = document.querySelector('.login-sheet');
  if (stepCode) stepCode.classList.add('d-none');
  if (stepConsent) stepConsent.classList.remove('d-none');
  if (loginSheet) loginSheet.classList.add('consent-active');
  // Append experiment group to consent iframe URL
  const consentIframe = document.getElementById('consentIframe');
  if (consentIframe && store.arm) {
    const url = new URL(consentIframe.src);
    url.searchParams.set('group', store.arm);
    consentIframe.src = url.toString();
  }

  // Check if consent code is required
  try {
    const config = await api('/v1/standalone/consent/config');
    consentCodeRequired = config.code_required;
  } catch (e) {
    console.warn('Failed to fetch consent config', e);
    consentCodeRequired = false;
  }

  // Show/hide code input section
  const codeSection = document.getElementById('consentCodeSection');
  const codeInput = document.getElementById('consentCodeInput');
  const codeError = document.getElementById('consentCodeError');
  if (codeSection) {
    codeSection.style.display = consentCodeRequired ? 'block' : 'none';
  }
  if (codeInput) codeInput.value = '';
  if (codeError) codeError.style.display = 'none';

  startConsentTimer();
}

function startConsentTimer() {
  const btn = document.getElementById('btnConsentContinue');
  if (!btn) return;

  let t = CONSENT_WAIT_SECONDS;
  btn.disabled = true;
  btn.className = 'btn btn-secondary';
  btn.textContent = 'Please complete the form above';

  if (consentTimerInt) clearInterval(consentTimerInt);
  consentTimerInt = setInterval(() => {
    t -= 1;
    if (t <= 0) {
      clearInterval(consentTimerInt);
      consentTimerInt = null;
      btn.disabled = false;
      btn.className = 'btn btn-success';
      btn.innerHTML = '<i class="bi bi-check2-circle me-1"></i>Continue to X-ELRA';
    }
  }, 1000);
}

function completeLogin(onSuccess, learnerId) {
  // Clear the login-in-progress flag now that login is complete
  setLoginInProgress(false);
  resetLogin();
  // Don't show the app view here — loadApp() gates it behind consent
  // and will show it once consent is verified.
  if (onSuccess) onSuccess(learnerId);
}

async function handleConsentContinue() {
  const codeInput = document.getElementById('consentCodeInput');
  const codeError = document.getElementById('consentCodeError');

  // Verify code if required
  if (consentCodeRequired) {
    const code = codeInput ? codeInput.value.trim() : '';

    if (!code) {
      if (codeError) {
        codeError.textContent = 'Please enter the completion code';
        codeError.style.display = 'block';
      }
      return;
    }

    try {
      const result = await api('/v1/standalone/consent/verify', {
        method: 'POST',
        body: JSON.stringify({ code }),
      });

      if (!result.valid) {
        if (codeError) {
          codeError.textContent = result.message || 'Invalid completion code';
          codeError.style.display = 'block';
        }
        return;
      }
    } catch (e) {
      if (codeError) {
        codeError.textContent = e.message || 'Failed to verify code';
        codeError.style.display = 'block';
      }
      return;
    }

    // Clear error on success
    if (codeError) codeError.style.display = 'none';
  }

  // Record consent
  try {
    await api('/v1/telemetry/consent', {
      method: 'POST',
      body: JSON.stringify({
        learner_id: store.learner,
        consent_given: true,
      }),
    });
    // Mark that consent was just granted so loadApp skips re-checking
    setConsentJustGranted(true);
  } catch (e) {
    console.error('Failed to record consent', e);
    const codeError = document.getElementById('consentCodeError');
    if (codeError) {
      codeError.textContent = 'Failed to save consent. Please try again.';
      codeError.style.display = 'block';
    }
    return; // Don't proceed if consent recording failed
  }

  // Complete login
  if (pendingOnSuccess) {
    const callback = pendingOnSuccess;
    pendingOnSuccess = null;
    completeLogin(callback, store.learner);
  } else {
    completeLogin(null, store.learner);
  }
}

function startResendTimer(){
  const link = document.getElementById('linkResend');
  const timerEl = document.getElementById('resendTimer');
  if(!link || !timerEl) return;
  let t = RESEND_WAIT_SECONDS;
  link.classList.add('disabled');
  timerEl.textContent = 'in ' + formatTime(t);
  if (resendInt) clearInterval(resendInt);
  resendInt = setInterval(()=>{
    t -= 1;
    if (t > 0){
      timerEl.textContent = 'in ' + formatTime(t);
    } else {
      clearInterval(resendInt);
      link.classList.remove('disabled');
      timerEl.textContent = '';
    }
  },1000);
}

export function initLogin(onSuccess){
  const btnReq = document.getElementById('btnReq');
  const btnVerify = document.getElementById('btnVerify');
  const btnConsentContinue = document.getElementById('btnConsentContinue');
  const emailEl = document.getElementById('email');
  const linkResend = document.getElementById('linkResend');
  const inputs = getOtpInputs();

  if (btnReq) btnReq.addEventListener('click', requestCode);
  if (emailEl) emailEl.addEventListener('keydown', e=>{ if(e.key==='Enter'){ e.preventDefault(); requestCode(); }});
  if (btnConsentContinue) btnConsentContinue.addEventListener('click', handleConsentContinue);

  function handleVerify(){ verifyCode(onSuccess); }

  if (btnVerify) btnVerify.addEventListener('click', handleVerify);
  if (linkResend) linkResend.addEventListener('click', e=>{
    e.preventDefault();
    if (!linkResend.classList.contains('disabled')) requestCode();
  });

  inputs.forEach((input, idx) => {
    input.addEventListener('input', () => {
      input.value = input.value.replace(/\D/g, '');
      if (input.value && idx < inputs.length - 1) inputs[idx + 1].focus();
      btnVerify.disabled = getCode().length !== inputs.length;
      if (idx === inputs.length - 1 && getCode().length === inputs.length) handleVerify();
    });
    input.addEventListener('keydown', e => {
      if (e.key === 'Backspace' && !input.value && idx > 0) inputs[idx - 1].focus();
      if (e.key === 'Enter' && getCode().length === inputs.length){ e.preventDefault(); handleVerify(); }
    });
  });

  if (inputs[0]){
    inputs[0].addEventListener('paste', e => {
      const paste = (e.clipboardData || window.clipboardData).getData('text').replace(/\D/g, '');
      if (paste.length === inputs.length){
        e.preventDefault();
        inputs.forEach((inp,i)=>{ inp.value = paste[i]; });
        btnVerify.disabled = false;
        handleVerify();
      }
    });
  }
}
