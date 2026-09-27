/**
 * Accessibility toolbar: text-to-speech toggle and font size controls.
 *
 * Inserts a small floating toolbar (bottom-left) that learners can expand
 * to adjust font size or hear page content read aloud via the Web Speech API.
 */

const FONT_SIZES = ['100%', '115%', '130%', '150%'];
const LS_KEY = 'xelra_a11y';

function loadPrefs() {
  try {
    return JSON.parse(localStorage.getItem(LS_KEY)) || {};
  } catch { return {}; }
}
function savePrefs(p) {
  try { localStorage.setItem(LS_KEY, JSON.stringify(p)); } catch {}
}

function createToolbar() {
  const prefs = loadPrefs();
  let fontIdx = prefs.fontIdx || 0;
  let ttsActive = false;

  // Apply saved font size
  if (fontIdx) document.documentElement.style.fontSize = FONT_SIZES[fontIdx];

  const bar = document.createElement('div');
  bar.id = 'a11yToolbar';
  bar.setAttribute('role', 'toolbar');
  bar.setAttribute('aria-label', 'Accessibility options');
  bar.innerHTML = `
    <button id="a11yToggle" class="a11y-toggle" aria-label="Accessibility options" aria-expanded="false" title="Accessibility options">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <circle cx="12" cy="4.5" r="2.5"/><path d="M12 7v5m0 0l-3 6m3-6l3 6M6 11h12"/>
      </svg>
    </button>
    <div id="a11yPanel" class="a11y-panel" style="display:none">
      <div class="a11y-row">
        <span class="a11y-label">Text size</span>
        <button id="a11yFontDown" aria-label="Decrease text size" title="Decrease text size">A&minus;</button>
        <span id="a11yFontVal" class="a11y-val">${FONT_SIZES[fontIdx]}</span>
        <button id="a11yFontUp" aria-label="Increase text size" title="Increase text size">A+</button>
      </div>
      <div class="a11y-row">
        <span class="a11y-label">Read aloud</span>
        <button id="a11yTTS" aria-label="Read page content aloud" title="Read aloud">${speechSynthesis ? 'Start' : 'N/A'}</button>
      </div>
    </div>`;

  document.body.appendChild(bar);

  const toggle = bar.querySelector('#a11yToggle');
  const panel = bar.querySelector('#a11yPanel');
  const fontVal = bar.querySelector('#a11yFontVal');
  const btnUp = bar.querySelector('#a11yFontUp');
  const btnDown = bar.querySelector('#a11yFontDown');
  const btnTTS = bar.querySelector('#a11yTTS');

  toggle.addEventListener('click', () => {
    const open = panel.style.display !== 'none';
    panel.style.display = open ? 'none' : 'flex';
    toggle.setAttribute('aria-expanded', String(!open));
  });

  const setFont = (idx) => {
    fontIdx = Math.max(0, Math.min(FONT_SIZES.length - 1, idx));
    document.documentElement.style.fontSize = FONT_SIZES[fontIdx];
    fontVal.textContent = FONT_SIZES[fontIdx];
    savePrefs({ ...loadPrefs(), fontIdx });
  };
  btnUp.addEventListener('click', () => setFont(fontIdx + 1));
  btnDown.addEventListener('click', () => setFont(fontIdx - 1));

  if (window.speechSynthesis) {
    btnTTS.addEventListener('click', () => {
      if (ttsActive) {
        speechSynthesis.cancel();
        ttsActive = false;
        btnTTS.textContent = 'Start';
        return;
      }
      // Read the main content area
      const main = document.querySelector('main') || document.querySelector('.learning-area') || document.body;
      const text = main.innerText.substring(0, 5000); // limit
      const utter = new SpeechSynthesisUtterance(text);
      utter.rate = 0.95;
      utter.onend = () => { ttsActive = false; btnTTS.textContent = 'Start'; };
      utter.onerror = () => { ttsActive = false; btnTTS.textContent = 'Start'; };
      speechSynthesis.speak(utter);
      ttsActive = true;
      btnTTS.textContent = 'Stop';
    });
  } else {
    btnTTS.disabled = true;
  }
}

// Inject styles
const style = document.createElement('style');
style.textContent = `
#a11yToolbar{position:fixed;bottom:16px;left:16px;z-index:1500;font-family:system-ui,sans-serif}
.a11y-toggle{width:40px;height:40px;border-radius:50%;border:2px solid rgba(255,255,255,.25);background:rgba(30,30,30,.9);color:#e6e6e6;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:background .15s}
.a11y-toggle:hover,.a11y-toggle:focus{background:rgba(76,110,245,.8);outline:2px solid #4c6ef5;outline-offset:2px}
.a11y-panel{display:flex;flex-direction:column;gap:8px;background:rgba(20,20,20,.95);border:1px solid rgba(255,255,255,.15);border-radius:10px;padding:10px;margin-bottom:8px;min-width:180px;position:absolute;bottom:48px;left:0}
.a11y-row{display:flex;align-items:center;gap:6px}
.a11y-label{font-size:.75rem;color:#a1a1a1;flex:1}
.a11y-val{font-size:.75rem;color:#e6e6e6;min-width:36px;text-align:center}
.a11y-panel button{padding:4px 10px;border-radius:6px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#e6e6e6;font-size:.8rem;cursor:pointer;transition:background .12s}
.a11y-panel button:hover{background:rgba(76,110,245,.4)}
.a11y-panel button:focus{outline:2px solid #4c6ef5;outline-offset:1px}
@media (prefers-reduced-motion:reduce){.a11y-toggle,.a11y-panel button{transition:none}}
`;
document.head.appendChild(style);

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', createToolbar);
} else {
  createToolbar();
}
