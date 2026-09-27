const telemetryCalls = [];

jest.mock('../services/api.js', () => {
  const api = jest.fn((path, opts = {}) => {
    if (path.startsWith('/v1/telemetry/consent')) {
      return Promise.resolve({ consent_given: true });
    }
    if (path === '/v1/version') {
      return Promise.resolve({ feature_flags: { explanations: true, feature_sentiment: true, infer_sentiment: true }, live_code: {} });
    }
    telemetryCalls.push({ path, opts });
    return Promise.resolve({ ok: true });
  });
  return {
    CONFIG: { API_BASE: 'http://localhost', PIS_URL: 'http://example.com/pis', RECS_TOP_K: 3 },
    api,
    setHTMLWithScripts: jest.fn(),
    ApiError: class ApiError extends Error {},
  };
});

jest.mock('../services/store.js', () => ({
  store: { learner: 'test-learner', token: 'token', lastSentiment: null },
  hasCelebrated: jest.fn(),
  unmarkCelebrated: jest.fn(),
  isLoginInProgress: jest.fn(() => false),
  setLoginInProgress: jest.fn(),
}));

jest.mock('../services/auth.js', () => ({
  initLogin: jest.fn((cb) => cb && cb()),
  signOut: jest.fn(),
}));

jest.mock('../ui/ui.js', () => ({
  showToast: jest.fn(),
  showLoading: jest.fn(),
  hideLoading: jest.fn(),
  hideBigToast: jest.fn(),
}));

jest.mock('../ui/celebration.js', () => ({
  celebrateSkill: jest.fn(),
  renderCourseComplete: jest.fn(),
}));

const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0));

describe('standalone lesson handling', () => {
  let openLesson;
  let store;

  beforeEach(async () => {
    jest.resetModules();
    telemetryCalls.length = 0;
    document.body.className = '';
    const root = document.createElement('div');
    root.innerHTML = `
      <nav></nav>
      <main id="viewApp"></main>
      <section id="viewLogin"></section>
      <div id="board"></div>
      <div id="armBadge"></div>
      <span id="strategyName"></span>
      <div id="topK"></div>
      <div id="focusSummary"></div>
      <div id="consentBanner"><button id="btnConsent"></button></div>
      <a id="pisLink"></a>
      <button id="btnSignOut"></button>
      <button id="btnCompletedSide"></button>
      <div id="lessonPanel"><iframe id="lessonViewer"></iframe><div id="lessonAnnounce"></div></div>
      <button id="btnLessonBack"></button>
      <button id="btnMarkComplete"></button>
      <div id="latestSentiment"></div>
      <div id="bigToast"><div class="big-toast"><button></button></div></div>
      <div id="toast"></div>
      <div id="loadingOverlay"></div>
      <div id="apiErrorAlert"><span data-role="message"></span></div>
      <div id="offcanvasCompleted"></div>
      <div id="olmList"></div>
    `;
    document.body.innerHTML = '';
    document.body.appendChild(root);
    window.bootstrap = { Offcanvas: { getOrCreateInstance: jest.fn(() => ({})) } };
    window.open = jest.fn();
    ({ store } = jest.requireMock('../services/store.js'));
    store.learner = 'learner-1';
    store.token = 'token-1';
    const mod = await import('../pages/standalone.js');
    openLesson = mod.openLesson;
  });

  afterEach(() => {
    document.body.innerHTML = '';
  });

  test('openLesson loads internal lesson in iframe', () => {
    const item = { item_id: 'py-001', url: '/content/PYAI/py-basics/001.html', telemetry: { itemId: 'py-001', learnerId: store.learner } };
    openLesson(item);
    const viewer = document.getElementById('lessonViewer');
    expect(document.body.classList.contains('view-lesson')).toBe(true);
    expect(viewer.getAttribute('src')).toBe('../content/PYAI/py-basics/001.html');
    expect(viewer.dataset.itemId).toBe('py-001');
  });

  test('openLesson opens external links in new tab', () => {
    const item = { item_id: 'ext-1', url: 'https://example.com/external' };
    openLesson(item);
    expect(window.open).toHaveBeenCalledWith('https://example.com/external', '_blank', 'noopener,noreferrer');
    expect(document.body.classList.contains('view-lesson')).toBe(false);
  });

  test('code run message posts telemetry and updates announcer', async () => {
    const item = { item_id: 'py-002', url: '/content/PYAI/py-basics/002.html', telemetry: { itemId: 'py-002', learnerId: store.learner, rank: 1 } };
    openLesson(item);
    window.dispatchEvent(new MessageEvent('message', {
      origin: window.location.origin,
      data: { type: 'XELRA_CODE_RUN', item_id: 'py-002', lesson_url: '/content/PYAI/py-basics/002.html', ok: true, ms: 120 },
    }));
    await flushPromises();
    const clickEvents = telemetryCalls.filter((c) => c.path === '/v1/telemetry/click');
    expect(clickEvents.length).toBeGreaterThan(0);
    const payload = JSON.parse(clickEvents.at(-1).opts.body);
    expect(payload.action).toBe('code_run');
    expect(payload.item_id).toBe('py-002');
    expect(document.getElementById('lessonAnnounce').textContent).toContain('Code executed');
  });

  test('lesson complete message queues completion telemetry', async () => {
    store.token = null;
    const item = { item_id: 'py-003', url: '/content/PYAI/py-basics/003.html', telemetry: { itemId: 'py-003', learnerId: store.learner, rank: 1 } };
    openLesson(item);
    window.dispatchEvent(new MessageEvent('message', {
      origin: window.location.origin,
      data: { type: 'XELRA_LESSON_COMPLETE', item_id: 'py-003', lesson_url: '/content/PYAI/py-basics/003.html' },
    }));
    await flushPromises();
    const completionEvents = telemetryCalls.filter((c) => c.path === '/v1/telemetry/completion');
    expect(completionEvents.length).toBeGreaterThan(0);
    const payload = JSON.parse(completionEvents.at(-1).opts.body);
    expect(payload.item_id).toBe('py-003');
    expect(payload.action).toBe('auto');
  });
});
