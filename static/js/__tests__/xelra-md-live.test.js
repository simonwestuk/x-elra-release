const { JSDOM } = require('jsdom');
const XelraMdLive = require('../xelra-md-live.js');

const { __test } = XelraMdLive;

describe('xelra-md-live', () => {
  beforeEach(() => {
    global.fetch = jest.fn(() => Promise.resolve({ ok: true }));
  });

  afterEach(() => {
    jest.useRealTimers();
    delete global.loadPyodide;
    delete global.Sk;
    delete global.__PYODIDE_STUB_FACTORY__;
    delete global.__SKULPT_STUB_EXEC__;
    delete global.document;
    delete global.window;
    delete global.parent;
    delete global.top;
    delete global.__XELRA_ENGINE_CACHE__;
  });

  test('detects python live blocks with metadata', () => {
    const dom = new JSDOM(`<!DOCTYPE html><html><head><meta name="xelra-md-live" data-engine="pyodide"></head><body>
      <pre data-info="python live"><code class="language-python">print('hi')</code></pre>
      <pre><code class="language-python">print('skip')</code></pre>
    </body></html>`);
    const liveBlocks = XelraMdLive.detectLiveBlocks(dom.window.document);
    expect(liveBlocks).toHaveLength(1);
    expect(liveBlocks[0].codeEl.textContent).toContain("print('hi')");
  });

  test('runWithTimeout rejects after timeout and interrupts engine', async () => {
    const engine = {
      interrupt: jest.fn(),
    };
    jest.useFakeTimers();
    const promise = __test.runWithTimeout(() => new Promise(() => {}), 10, engine);
    jest.advanceTimersByTime(15);
    await expect(promise).rejects.toThrow('Execution exceeded timeout');
    expect(engine.interrupt).toHaveBeenCalled();
  });

  test('maps syntax and runtime errors to taxonomy', () => {
    expect(XelraMdLive.mapError(new SyntaxError('bad syntax'))).toBe('syntax');
    const runtimeError = new ReferenceError('not defined');
    expect(XelraMdLive.mapError(runtimeError)).toBe('runtime');
    const timeoutErr = new XelraMdLive.TimeoutError();
    expect(XelraMdLive.mapError(timeoutErr)).toBe('timeout');
  });

  test('telemetry client respects consent and payload structure', async () => {
    const config = {
      telemetryConsent: 'granted',
      telemetryBaseUrl: '/v1/telemetry/live',
      itemId: 'item-1',
      learnerId: 'learner-9',
      attemptId: 'attempt-x',
      sessionId: 'session-z',
      engine: 'pyodide',
    };
    const telemetry = __test.createTelemetryClient(config);
    await telemetry.emit('run', { cell_id: 'cell-1', status: 'started' });
    expect(global.fetch).toHaveBeenCalledTimes(1);
    const [url, opts] = global.fetch.mock.calls[0];
    expect(url).toBe('/v1/telemetry/live/run');
    const payload = JSON.parse(opts.body);
    expect(payload.item_id).toBe('item-1');
    expect(payload.learner_id).toBe('learner-9');
    expect(payload.cell_id).toBe('cell-1');

    global.fetch.mockClear();
    const telemetryDenied = __test.createTelemetryClient({ telemetryConsent: 'denied', telemetryBaseUrl: '/v1/telemetry/live' });
    await telemetryDenied.emit('run', { cell_id: 'cell-2' });
    expect(global.fetch).not.toHaveBeenCalled();
  });

  test('bootstrap renders widgets and triggers impression telemetry', async () => {
    global.__PYODIDE_STUB_FACTORY__ = jest.fn(async () => ({
      runPythonAsync: jest.fn(async () => 'ok'),
      globals: { clear: jest.fn() },
    }));
    const dom = new JSDOM(`<!DOCTYPE html><html><head>
      <meta name="xelra-md-live" data-engine="pyodide" data-telemetry-consent="granted"></head><body>
      <pre data-info="python live" data-cell-id="example-1"><code class="language-python" data-timeout-ms="5">print('hi')</code></pre>
    </body></html>`, { runScripts: 'outside-only' });
    global.document = dom.window.document;
    global.window = dom.window;
    global.fetch = jest.fn(() => Promise.resolve({ ok: true }));
    const result = XelraMdLive.bootstrap(dom.window.document);
    expect(result.widgets).toHaveLength(1);
    expect(dom.window.document.querySelector('.xelra-live__editor')).not.toBeNull();
    // impression fired once
    expect(global.fetch).toHaveBeenCalled();
  });

  test('reuses cached pyodide engine across bootstraps', async () => {
    const instance = {
      globals: { get: jest.fn(() => null) },
      runPythonAsync: jest.fn(async () => {}),
      runPython: jest.fn(),
      interrupt: jest.fn(),
    };
    global.loadPyodide = jest.fn(async () => instance);

    const config = {
      engine: 'pyodide',
      pyodideBaseUrl: '/static/js/vendor/pyodide',
      skulptBaseUrl: '/static/js/vendor/skulpt',
    };

    const managerA = __test.createEngineManager(config);
    const engineA = await managerA.ensureEngine();
    expect(global.loadPyodide).toHaveBeenCalledTimes(1);

    delete global.loadPyodide;

    const managerB = __test.createEngineManager(config);
    const engineB = await managerB.ensureEngine();
    expect(engineB).toBe(engineA);
  });

  test('normaliseForComparison strips trailing whitespace and newlines', () => {
    expect(__test.normaliseForComparison('hello  \nworld\n\n')).toBe('hello\nworld');
    expect(__test.normaliseForComparison('  line1  \n  line2  \n')).toBe('  line1\n  line2');
    expect(__test.normaliseForComparison('')).toBe('');
  });

  test('getExpectedOutput reads data attribute from sibling div', () => {
    const dom = new JSDOM(`<!DOCTYPE html><html><body>
      <pre data-info="python live"><code class="language-python">print('hi')</code></pre>
      <div class="xelra-expected-output" hidden data-expected-output="Hello, Python!"></div>
    </body></html>`);
    const pre = dom.window.document.querySelector('pre');
    expect(__test.getExpectedOutput(pre)).toBe('Hello, Python!');
  });

  test('getExpectedOutput returns null when no sibling present', () => {
    const dom = new JSDOM(`<!DOCTYPE html><html><body>
      <pre data-info="python live"><code class="language-python">print('hi')</code></pre>
    </body></html>`);
    const pre = dom.window.document.querySelector('pre');
    expect(__test.getExpectedOutput(pre)).toBeNull();
  });

  test('getExpectedOutput decodes HTML entities', () => {
    const dom = new JSDOM(`<!DOCTYPE html><html><body>
      <pre data-info="python live"><code class="language-python">print('hi')</code></pre>
      <div class="xelra-expected-output" hidden data-expected-output="Line 1&#10;Line 2"></div>
    </body></html>`);
    const pre = dom.window.document.querySelector('pre');
    expect(__test.getExpectedOutput(pre)).toBe('Line 1\nLine 2');
  });

  test('shares pyodide engine cache with accessible parent window', async () => {
    const instance = {
      globals: { get: jest.fn(() => null) },
      runPythonAsync: jest.fn(async () => {}),
      runPython: jest.fn(),
      interrupt: jest.fn(),
    };
    const parentWindow = {};
    global.parent = parentWindow;
    global.top = parentWindow;
    global.loadPyodide = jest.fn(async () => instance);

    const config = {
      engine: 'pyodide',
      pyodideBaseUrl: '/static/js/vendor/pyodide',
      skulptBaseUrl: '/static/js/vendor/skulpt',
    };

    const managerA = __test.createEngineManager(config);
    const engineA = await managerA.ensureEngine();
    expect(global.loadPyodide).toHaveBeenCalledTimes(1);
    expect(parentWindow.__XELRA_ENGINE_CACHE__).toBeDefined();
    expect(global.__XELRA_ENGINE_CACHE__).toBeUndefined();

    delete global.loadPyodide;

    const managerB = __test.createEngineManager(config);
    const engineB = await managerB.ensureEngine();
    expect(engineB).toBe(engineA);
  });
});
