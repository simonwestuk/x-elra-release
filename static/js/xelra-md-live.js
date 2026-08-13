(function (global, factory) {
  if (typeof module === 'object' && typeof module.exports === 'object') {
    module.exports = factory(global);
  } else {
    global.XelraMdLive = factory(global);
  }
})(typeof globalThis !== 'undefined' ? globalThis : typeof self !== 'undefined' ? self : this, function (global) {
  'use strict';

  const DEFAULT_CONFIG = {
    engine: 'skulpt',  // Changed to skulpt for fast loading on all devices
    pyodideBaseUrl: '/static/js/vendor/pyodide',
    skulptBaseUrl: '/static/js/vendor/skulpt',
    telemetryBaseUrl: '/v1/telemetry/live',
    timeoutMs: 5000,
    allowFallback: true,
  };

  const EVENT_NAMES = {
    impression: 'impression',
    run: 'run',
    success: 'success',
    hint: 'hint',
    reflection: 'reflection',
    arlNudge: 'arl_nudge',
  };

  function toNumber(value, fallback) {
    if (value === undefined || value === null || value === '') return fallback;
    const num = Number(value);
    return Number.isFinite(num) ? num : fallback;
  }

  function normaliseBoolean(value, fallback = false) {
    if (value === undefined || value === null || value === '') return fallback;
    if (typeof value === 'boolean') return value;
    if (typeof value === 'string') {
      const lower = value.trim().toLowerCase();
      if (['1', 'true', 'yes', 'y', 'granted', 'allow', 'allowed'].includes(lower)) return true;
      if (['0', 'false', 'no', 'n', 'denied', 'deny', 'blocked'].includes(lower)) return false;
    }
    return fallback;
  }

  function detectLowEndDevice() {
    // Check CPU cores (most reliable indicator)
    const cores = (typeof navigator !== 'undefined' && navigator.hardwareConcurrency) || 4;

    // Check memory if available (Chrome/Edge only)
    const memory = (typeof navigator !== 'undefined' && navigator.deviceMemory) || 4;

    // Check connection speed if available
    let slowConnection = false;
    if (typeof navigator !== 'undefined' && navigator.connection) {
      const conn = navigator.connection;
      const effectiveType = conn.effectiveType || '';
      slowConnection = effectiveType === 'slow-2g' || effectiveType === '2g';
    }

    // Check if mobile device
    const isMobile = typeof navigator !== 'undefined' &&
                     /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

    // Decision criteria:
    // - Less than 4 CPU cores = low-end
    // - Less than 4GB RAM = low-end
    // - Slow connection = prefer lighter engine
    // - Mobile = prefer lighter engine (battery/heat concerns)
    const isLowEnd = cores < 4 || memory < 4 || slowConnection || isMobile;

    console.debug('[xelra-live] Device detection:', {
      cores,
      memory,
      slowConnection,
      isMobile,
      isLowEnd,
      decision: isLowEnd ? 'skulpt' : 'pyodide'
    });

    return isLowEnd;
  }

  function selectOptimalEngine(requestedEngine, allowAutoSelect) {
    // If auto-selection is disabled, respect the requested engine
    if (!allowAutoSelect) {
      return requestedEngine;
    }

    // If explicitly requested skulpt or pyodide, respect that
    if (requestedEngine === 'skulpt' || requestedEngine === 'pyodide') {
      return requestedEngine;
    }

    // Auto-select based on device capabilities
    const isLowEnd = detectLowEndDevice();
    const selected = isLowEnd ? 'skulpt' : 'pyodide';

    console.info('[xelra-live] Auto-selected engine:', selected, '(requested:', requestedEngine, ')');
    return selected;
  }

  function parseConfig(doc) {
    doc = doc || global.document;
    if (!doc || !doc.querySelector) return null;
    const meta = doc.querySelector('meta[name="xelra-md-live"]');
    const dataset = meta ? meta.dataset : {};
    if (!meta && !Object.keys(dataset).length) {
      return null;
    }

    // Check if auto-selection is enabled (default: true)
    const allowAutoSelect = normaliseBoolean(dataset.autoSelectEngine, true);

    // Get requested engine, applying smart selection if enabled
    const requestedEngine = (dataset.engine || DEFAULT_CONFIG.engine).toLowerCase();
    const selectedEngine = selectOptimalEngine(requestedEngine, allowAutoSelect);

    const config = {
      engine: selectedEngine,
      pyodideBaseUrl: dataset.pyodideBaseUrl || dataset.pyodideBaseurl || DEFAULT_CONFIG.pyodideBaseUrl,
      skulptBaseUrl: dataset.skulptBaseUrl || dataset.skulptBaseurl || DEFAULT_CONFIG.skulptBaseUrl,
      telemetryBaseUrl: dataset.telemetryBaseUrl || dataset.telemetryBaseurl || DEFAULT_CONFIG.telemetryBaseUrl,
      timeoutMs: toNumber(dataset.timeoutMs, DEFAULT_CONFIG.timeoutMs),
      allowFallback: normaliseBoolean(dataset.allowFallback, DEFAULT_CONFIG.allowFallback),
      itemId: dataset.item_id || dataset.itemId || null,
      learnerId: dataset.learner_id || dataset.learnerId || null,
      attemptId: dataset.attempt_id || dataset.attemptId || null,
      sessionId: dataset.session_id || dataset.sessionId || null,
      telemetryConsent: dataset.telemetryConsent || dataset.consent || null,
      reflectionPrompt: dataset.reflectionPrompt || null,
      arlNudgeText: dataset.arlNudge || dataset.arlNudgeText || null,
      lessonUrl: dataset.lessonUrl || dataset.lesson_url || null,
      parentOrigin: dataset.parentOrigin || dataset.parent_origin || null,
    };
    return config;
  }

  function getLiveHint(el) {
    if (!el) return null;
    const attrs = [
      el.getAttribute && el.getAttribute('data-hint'),
      el.dataset && (el.dataset.hint || el.dataset.hints),
    ].filter(Boolean);
    if (attrs.length) return attrs[0];
    if (el.parentElement) return getLiveHint(el.parentElement);
    return null;
  }

  function getLiveReflectionPrompt(el, fallback) {
    if (!el) return fallback;
    const attr = el.getAttribute && el.getAttribute('data-reflection');
    if (attr) return attr;
    if (el.dataset && el.dataset.reflection) return el.dataset.reflection;
    if (el.parentElement) return getLiveReflectionPrompt(el.parentElement, fallback);
    return fallback;
  }

  function getCellId(el, index) {
    if (!el) return `cell-${index + 1}`;
    const attr = el.getAttribute && (el.getAttribute('data-cell-id') || el.getAttribute('data-cellid'));
    if (attr) return attr;
    if (el.dataset && (el.dataset.cellId || el.dataset.cell_id)) return el.dataset.cellId || el.dataset.cell_id;
    if (el.parentElement) return getCellId(el.parentElement, index);
    return `cell-${index + 1}`;
  }

  function isPythonLive(codeEl) {
    if (!codeEl) return false;
    const className = (codeEl.getAttribute('class') || '').toLowerCase();
    const classes = className.split(/\s+/).filter(Boolean);
    const languageMatch = classes.some(cls => cls === 'language-python' || cls === 'lang-python' || cls === 'python');
    if (!languageMatch) return false;
    const metaValues = [];
    const dataInfo = codeEl.getAttribute('data-info') || codeEl.getAttribute('data-meta');
    if (dataInfo) metaValues.push(dataInfo);
    if (codeEl.dataset) {
      if (codeEl.dataset.info) metaValues.push(codeEl.dataset.info);
      if (codeEl.dataset.meta) metaValues.push(codeEl.dataset.meta);
      if (codeEl.dataset.live) metaValues.push(codeEl.dataset.live);
    }
    const parent = codeEl.parentElement;
    if (parent) {
      const parentInfo = parent.getAttribute('data-info') || parent.getAttribute('data-meta');
      if (parentInfo) metaValues.push(parentInfo);
      if (parent.dataset) {
        if (parent.dataset.info) metaValues.push(parent.dataset.info);
        if (parent.dataset.meta) metaValues.push(parent.dataset.meta);
        if (parent.dataset.live) metaValues.push(parent.dataset.live);
      }
      const parentClass = parent.getAttribute('class') || '';
      if (/\blive\b/.test(parentClass)) metaValues.push('live');
    }
    if (/\blive\b/.test(className)) metaValues.push('live');
    const textMatch = metaValues.join(' ').toLowerCase();
    return textMatch.split(/[^a-z0-9_]+/).includes('live');
  }

  function getExpectedOutput(preEl) {
    if (!preEl) return null;
    // Look for a sibling .xelra-expected-output div placed after the <pre> by the build step
    let sibling = preEl.nextElementSibling;
    while (sibling) {
      if (sibling.classList && sibling.classList.contains('xelra-expected-output')) {
        const raw = sibling.getAttribute('data-expected-output');
        if (raw) {
          // Decode HTML entities (&#10; -> newline, &amp; -> &, etc.)
          const tmp = sibling.ownerDocument.createElement('textarea');
          tmp.innerHTML = raw;
          return tmp.value;
        }
        return null;
      }
      // Stop if we hit another <pre> (next code block)
      if (sibling.tagName === 'PRE') break;
      sibling = sibling.nextElementSibling;
    }
    return null;
  }

  function normaliseForComparison(text) {
    if (typeof text !== 'string') return '';
    // Strip trailing whitespace per line and trailing newlines
    return text.replace(/[ \t]+$/gm, '').replace(/\n+$/, '');
  }

  function detectLiveBlocks(doc) {
    doc = doc || global.document;
    if (!doc) return [];
    const candidates = Array.from(doc.querySelectorAll('pre code'));
    const liveCodes = candidates.filter(isPythonLive);
    return liveCodes.map(codeEl => ({
      codeEl,
      preEl: codeEl.closest('pre') || codeEl.parentElement,
    }));
  }

  function loadScriptOnce(url, attrName) {
    return new Promise((resolve, reject) => {
      if (!global.document) {
        reject(new Error('Document is not available to load scripts'));
        return;
      }
      const head = global.document.head || global.document.getElementsByTagName('head')[0];
      if (!head) {
        reject(new Error('Unable to find document head'));
        return;
      }
      const existing = attrName ? head.querySelector(`script[${attrName}]`) : head.querySelector(`script[src="${url}"]`);
      if (existing) {
        if (existing.hasAttribute('data-loaded')) {
          resolve();
          return;
        }
        existing.addEventListener('load', () => resolve());
        existing.addEventListener('error', (err) => reject(err));
        return;
      }
      const script = global.document.createElement('script');
      script.src = url;
      script.async = true;
      if (attrName) {
        script.setAttribute(attrName, 'true');
      }
      script.addEventListener('load', () => {
        script.setAttribute('data-loaded', 'true');
        resolve();
      });
      script.addEventListener('error', (err) => reject(err));
      head.appendChild(script);
    });
  }

  function getSharedEngineCache(globalObj) {
    const cacheKey = '__XELRA_ENGINE_CACHE__';
    const hosts = [];
    const pushHost = (host) => {
      if (!host || typeof host !== 'object') return;
      if (hosts.includes(host)) return;
      hosts.push(host);
    };
    if (globalObj && typeof globalObj === 'object') {
      try {
        const parent = globalObj.parent;
        if (parent && parent !== globalObj) pushHost(parent);
      } catch (_) {}
      try {
        const top = globalObj.top;
        if (top && top !== globalObj) pushHost(top);
      } catch (_) {}
      pushHost(globalObj);
    }
    for (let i = 0; i < hosts.length; i += 1) {
      const host = hosts[i];
      if (!host || typeof host !== 'object') continue;
      try {
        if (!host[cacheKey] || typeof host[cacheKey] !== 'object') {
          host[cacheKey] = {};
        }
        return host[cacheKey];
      } catch (_) {
        try {
          Object.defineProperty(host, cacheKey, { value: {}, configurable: true, writable: true });
          return host[cacheKey];
        } catch (err) {
          console.warn('[xelra-live] Failed to attach shared engine cache', err);
        }
      }
    }
    return {};
  }

  function normaliseBaseUrl(url, fallback) {
    const value = url || fallback || '';
    return String(value).replace(/\/+$/, '');
  }

  function getEngineCacheKey(name, config) {
    if (name === 'pyodide') {
      const base = normaliseBaseUrl(config.pyodideBaseUrl, DEFAULT_CONFIG.pyodideBaseUrl);
      return `pyodide::${base || 'default'}`;
    }
    if (name === 'skulpt') {
      const base = normaliseBaseUrl(config.skulptBaseUrl, DEFAULT_CONFIG.skulptBaseUrl);
      return `skulpt::${base || 'default'}`;
    }
    return name;
  }

  function createPyodideEngine(config) {
    return (async function () {
      if (typeof global.loadPyodide !== 'function') {
        await loadScriptOnce(`${config.pyodideBaseUrl.replace(/\/$/, '')}/pyodide.js`, 'data-xelra-pyodide');
      }
      if (typeof global.loadPyodide !== 'function') {
        throw new Error('Pyodide loader is not available');
      }
      const instance = await global.loadPyodide({ indexURL: config.pyodideBaseUrl });
      const helperState = { ready: false };
      const namespaceKey = '__xelra_namespace';
      const helperSource = [
        'import builtins',
        'import contextlib',
        'import io',
        'import traceback',
        '',
        '__xelra_namespace = {\"__name__\": \"__main__\", \"__builtins__\": builtins.__dict__}',
        '',
        'def __xelra_reset_namespace():',
        "    global __xelra_namespace",
        '    __xelra_namespace = {\"__name__\": \"__main__\", \"__builtins__\": builtins.__dict__}',
        '',
        'def __xelra_exec(source):',
        "    global __xelra_namespace",
        '    stdout_buffer = io.StringIO()',
        '    stderr_buffer = io.StringIO()',
        '    try:',
        "        compiled = compile(source, '<xelra>', 'exec')",
        '    except Exception as exc:',
        '        return {',
        "            'ok': False,",
        "            'stdout': stdout_buffer.getvalue(),",
        "            'stderr': stderr_buffer.getvalue(),",
        "            'error': ''.join(traceback.format_exception_only(type(exc), exc)).strip(),",
        "            'trace': ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)),",
        '        }',
        '    try:',
        '        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):',
        '            exec(compiled, __xelra_namespace, __xelra_namespace)',
        '    except Exception as exc:',
        '        return {',
        "            'ok': False,",
        "            'stdout': stdout_buffer.getvalue(),",
        "            'stderr': stderr_buffer.getvalue(),",
        "            'error': ''.join(traceback.format_exception_only(type(exc), exc)).strip(),",
        "            'trace': ''.join(traceback.format_exception(type(exc), exc, exc.__traceback__)),",
        '        }',
        '    return {',
        "        'ok': True,",
        "        'stdout': stdout_buffer.getvalue(),",
        "        'stderr': stderr_buffer.getvalue(),",
        '    }',
      ].join('\n');

      async function ensureHelpers() {
        if (helperState.ready) {
          const existing = instance.globals.get('__xelra_exec');
          if (existing) {
            return existing;
          }
          helperState.ready = false;
        }
        try {
          await instance.runPythonAsync(helperSource);
        } catch (err) {
          console.error('[xelra-live] helper load failed', err);
          helperState.ready = false;
          return null;
        }
        const created = instance.globals.get('__xelra_exec');
        console.debug('[xelra-live] helper loaded', { hasHelper: Boolean(created) });
        helperState.ready = Boolean(created);
        return created || null;
      }

      function toPlainObject(pyValue) {
        if (!pyValue) return pyValue;
        if (typeof pyValue.toJs === 'function') {
          const converted = pyValue.toJs({
            create_proxies: false,
            dict_converter(items) {
              return Object.fromEntries(items);
            },
          });
          return converted;
        }
        return pyValue;
      }

      return {
        name: 'pyodide',
        instance,
        async run(code) {
          const runner = await ensureHelpers();
          if (!runner) {
            throw new Error('Execution helper is unavailable');
          }
          let resultProxy;
          try {
            resultProxy = runner(code);
            const result = toPlainObject(resultProxy);
            if (!result || typeof result !== 'object') {
              return '';
            }
            if (!result.ok) {
              const err = new Error(result.error || result.stderr || 'Execution failed');
              err.stdout = result.stdout || '';
              err.stderr = result.stderr || '';
              err.trace = result.trace || '';
              throw err;
            }
            const stdout = typeof result.stdout === 'string' ? result.stdout : '';
            const stderr = typeof result.stderr === 'string' ? result.stderr : '';
            return { stdout, stderr };
          } finally {
            if (resultProxy && typeof resultProxy.destroy === 'function') {
              resultProxy.destroy();
            }
            if (runner && typeof runner.destroy === 'function') {
              runner.destroy();
            }
          }
        },
        interrupt() {
          if (instance && typeof instance.interrupt === 'function') {
            try { instance.interrupt(); } catch (_) {}
          }
        },
        reset() {
          try {
            instance.runPython(`
import builtins
globals()['${namespaceKey}'] = {'__name__': '__main__', '__builtins__': builtins.__dict__}
`);
          } catch (_) {
            // ignore reset errors
          }
        }
      };
    })();
  }

  function createSkulptEngine(config) {
    return (async function () {
      const baseUrl = config.skulptBaseUrl.replace(/\/$/, '');

      // Load main Skulpt runtime
      if (!global.Sk) {
        await loadScriptOnce(`${baseUrl}/skulpt.min.js`, 'data-xelra-skulpt');
      }
      if (!global.Sk) {
        throw new Error('Skulpt runtime is not available');
      }

      // Load standard library for better Python compatibility
      if (!global.Sk.builtinFiles || !global.Sk.builtinFiles.files) {
        try {
          await loadScriptOnce(`${baseUrl}/skulpt-stdlib.js`, 'data-xelra-skulpt-stdlib');
          console.debug('[xelra-live] Skulpt stdlib loaded');
        } catch (err) {
          console.warn('[xelra-live] Skulpt stdlib load failed (continuing without it):', err);
        }
      }

      const runtime = global.Sk;
      return {
        name: 'skulpt',
        runtime,
        async run(code) {
          const outputs = [];
          runtime.configure({
            output: (text) => outputs.push(text),
            read: function (filename) {
              if (runtime.builtinFiles === undefined || runtime.builtinFiles.files[filename] === undefined) {
                throw new Error(`File not found: ${filename}`);
              }
              return runtime.builtinFiles.files[filename];
            }
          });
          await runtime.misceval.asyncToPromise(() => runtime.importMainWithBody('<stdin>', false, code, true));
          return outputs.join('');
        },
        interrupt() {
          if (typeof runtime.breakpoint === 'function') {
            try { runtime.breakpoint(); } catch (_) {}
          }
        },
        reset() {
          if (typeof runtime.reset === 'function') {
            runtime.reset();
          }
        }
      };
    })();
  }

  function createEngineManager(config) {
    const cache = getSharedEngineCache(global);
    let activeName = config.engine;
    async function load(name) {
      const cacheKey = getEngineCacheKey(name, config);
      if (!cache[cacheKey]) {
        if (name === 'pyodide') {
          cache[cacheKey] = createPyodideEngine(config).catch((err) => {
            delete cache[cacheKey];
            throw err;
          });
        } else if (name === 'skulpt') {
          cache[cacheKey] = createSkulptEngine(config).catch((err) => {
            delete cache[cacheKey];
            throw err;
          });
        } else {
          throw new Error(`Unsupported engine: ${name}`);
        }
      }
      return cache[cacheKey];
    }
    return {
      async ensureEngine() {
        try {
          const engine = await load(activeName);
          return engine;
        } catch (err) {
          if (config.allowFallback && activeName !== 'skulpt') {
            console.warn('Engine load failed, attempting Skulpt fallback', err);
            activeName = 'skulpt';
            return load(activeName);
          }
          throw err;
        }
      },
      getActiveName() {
        return activeName;
      }
    };
  }

  class TimeoutError extends Error {
    constructor(message) {
      super(message || 'Execution timed out');
      this.name = 'TimeoutError';
    }
  }

  function runWithTimeout(promiseFactory, timeoutMs, engine) {
    const ms = typeof timeoutMs === 'number' && timeoutMs > 0 ? timeoutMs : DEFAULT_CONFIG.timeoutMs;
    let timer;
    let finished = false;
    return new Promise((resolve, reject) => {
      function onTimeout() {
        finished = true;
        if (engine && typeof engine.interrupt === 'function') {
          try { engine.interrupt(); } catch (_) {}
        }
        reject(new TimeoutError('Execution exceeded timeout'));
      }
      timer = setTimeout(onTimeout, ms);
      Promise.resolve()
        .then(() => promiseFactory())
        .then((result) => {
          if (finished) return;
          clearTimeout(timer);
          resolve(result);
        })
        .catch((err) => {
          if (finished) return;
          clearTimeout(timer);
          reject(err);
        });
    });
  }

  function normaliseEngineResult(result) {
    if (result === undefined || result === null) return '';
    if (typeof result === 'string') return result;
    if (typeof result === 'object') {
      const stdout = typeof result.stdout === 'string' ? result.stdout : (Array.isArray(result.stdout) ? result.stdout.join('') : '');
      const stderr = typeof result.stderr === 'string' ? result.stderr : (Array.isArray(result.stderr) ? result.stderr.join('') : '');
      if (stdout || stderr) {
        if (stdout && stderr) {
          const joiner = stdout.endsWith('\n') ? '' : '\n';
          return stdout + joiner + stderr;
        }
        return stdout || stderr;
      }
      if (typeof result.toString === 'function' && result.toString !== Object.prototype.toString) {
        return result.toString();
      }
    }
    return String(result);
  }

  function mapError(err) {
    if (!err) return 'unknown';
    if (err instanceof TimeoutError) return 'timeout';
    const message = (err.message || '').toLowerCase();
    const name = (err.name || '').toLowerCase();
    if (name.includes('syntax') || message.includes('syntaxerror') || message.includes('invalid syntax')) {
      return 'syntax';
    }
    if (name.includes('typeerror') || name.includes('referenceerror') || name.includes('nameerror')) {
      return 'runtime';
    }
    if (message.includes('timeout')) return 'timeout';
    return 'runtime';
  }

  // Extract the Python error type name (e.g., "SyntaxError", "NameError") from raw message
  function extractErrorType(rawMsg) {
    const match = /^(\w*Error)\b/i.exec(rawMsg);
    return match ? match[1] : 'Error';
  }

  // Beginner-friendly error explanations
  const FRIENDLY_ERRORS = [
    // NameError variations
    {
      pattern: /NameError:.*name '(\w+)' is not defined/i,
      friendly: (match) => `"${match[1]}" hasn't been created yet. Check spelling or define it before using it.`,
    },
    {
      pattern: /UnboundLocalError:.*'(\w+)'.*referenced before assignment/i,
      friendly: (match) => `"${match[1]}" is used before it's given a value. Assign it a value first.`,
    },

    // SyntaxError variations
    {
      pattern: /SyntaxError:.*invalid syntax/i,
      friendly: () => 'Something looks wrong with the code structure. Check for missing colons, brackets, or quotes.',
    },
    {
      pattern: /SyntaxError:.*EOL while scanning string/i,
      friendly: () => 'String not closed. Make sure quotes match at start and end.',
    },
    {
      pattern: /SyntaxError:.*unexpected EOF/i,
      friendly: () => 'Code ended unexpectedly. You may be missing a closing bracket or quote.',
    },
    {
      pattern: /SyntaxError:.*'return' outside function/i,
      friendly: () => '"return" can only be used inside a function. Check your indentation.',
    },
    {
      pattern: /SyntaxError:.*'break' outside loop/i,
      friendly: () => '"break" can only be used inside a loop (for/while). Check your indentation.',
    },
    {
      pattern: /SyntaxError:.*'continue' not properly in loop/i,
      friendly: () => '"continue" can only be used inside a loop (for/while). Check your indentation.',
    },
    {
      pattern: /SyntaxError:.*cannot assign to literal/i,
      friendly: () => 'Cannot assign to a value like a number or string. Put the variable name on the left of =.',
    },
    {
      pattern: /SyntaxError:.*cannot assign to operator/i,
      friendly: () => 'Invalid assignment. Make sure the variable name is on the left side of =.',
    },
    {
      pattern: /SyntaxError:.*positional argument follows keyword argument/i,
      friendly: () => 'Regular arguments must come before named arguments. Rearrange your function call.',
    },
    {
      pattern: /SyntaxError:.*non-default argument follows default argument/i,
      friendly: () => 'Parameters without defaults must come before parameters with defaults.',
    },
    {
      pattern: /SyntaxError:.*expected ':'/i,
      friendly: () => 'Missing colon. Add : at the end of if, for, while, def, or class statements.',
    },
    {
      pattern: /SyntaxError:.*unmatched '\)'/i,
      friendly: () => 'Extra closing parenthesis ) without a matching opening one.',
    },
    {
      pattern: /SyntaxError:.*unmatched '\]'/i,
      friendly: () => 'Extra closing bracket ] without a matching opening one.',
    },
    {
      pattern: /SyntaxError:.*unmatched '\}'/i,
      friendly: () => 'Extra closing brace } without a matching opening one.',
    },
    {
      pattern: /SyntaxError:.*'\(' was never closed/i,
      friendly: () => 'Missing closing parenthesis. Add ) to close the opening (.',
    },
    {
      pattern: /SyntaxError:.*'\[' was never closed/i,
      friendly: () => 'Missing closing bracket. Add ] to close the opening [.',
    },
    {
      pattern: /SyntaxError:.*'\{' was never closed/i,
      friendly: () => 'Missing closing brace. Add } to close the opening {.',
    },
    {
      pattern: /SyntaxError:.*f-string.*empty expression/i,
      friendly: () => 'Empty {} in f-string. Put a variable or expression inside the braces.',
    },
    {
      pattern: /SyntaxError:.*EOF in multi-line/i,
      friendly: () => 'Your code ends in the middle of something. Check for unclosed quotes (""" or \'\'\'), brackets, or parentheses.',
    },
    {
      pattern: /SyntaxError:.*bad input/i,
      friendly: () => 'Python doesn\'t understand this code. Check for typos, missing colons after if/for/while/def, or mismatched brackets.',
    },
    {
      pattern: /SyntaxError:.*unexpected character/i,
      friendly: () => 'Unexpected character found. Check for special characters that don\'t belong in Python code.',
    },
    {
      pattern: /SyntaxError:.*invalid token/i,
      friendly: () => 'Invalid character or symbol. Check for typos or characters that Python doesn\'t recognize.',
    },
    {
      pattern: /SyntaxError:.*illegal/i,
      friendly: () => 'Something is not allowed here. Check your code structure and syntax.',
    },
    {
      pattern: /SyntaxError/i,
      friendly: () => 'There\'s a problem with how the code is written. Check for missing colons, brackets, quotes, or typos.',
    },

    // IndentationError / TabError
    {
      pattern: /IndentationError:.*expected an indented block/i,
      friendly: () => 'Expected indented code after this line. Add 4 spaces before the next line.',
    },
    {
      pattern: /IndentationError:.*unexpected indent/i,
      friendly: () => 'This line is indented too much. Remove some spaces from the start.',
    },
    {
      pattern: /IndentationError:.*unindent does not match/i,
      friendly: () => 'Indentation doesn\'t line up. Use the same number of spaces as the matching line above.',
    },
    {
      pattern: /IndentationError/i,
      friendly: () => 'Indentation problem. Use consistent spaces (usually 4) at the start of lines inside blocks.',
    },
    {
      pattern: /TabError/i,
      friendly: () => 'Mixing tabs and spaces. Use only spaces for indentation (4 spaces per level).',
    },

    // TypeError variations
    {
      pattern: /TypeError:.*'(\w+)' object is not callable/i,
      friendly: (match) => `"${match[1]}" is a value, not a function. Remove the parentheses () after it.`,
    },
    {
      pattern: /TypeError:.*'NoneType' object is not iterable/i,
      friendly: () => 'Trying to loop over None. The variable might be empty or a function forgot to return a value.',
    },
    {
      pattern: /TypeError:.*'NoneType' object is not subscriptable/i,
      friendly: () => 'Trying to use [] on None. The variable might be empty or a function forgot to return a value.',
    },
    {
      pattern: /TypeError:.*'(\w+)' object is not iterable/i,
      friendly: (match) => `Cannot loop over a ${match[1]}. Use a list, string, or other sequence.`,
    },
    {
      pattern: /TypeError:.*'(\w+)' object is not subscriptable/i,
      friendly: (match) => `Cannot use [] on a ${match[1]}. This type doesn't support indexing.`,
    },
    {
      pattern: /TypeError:.*can only concatenate str.*to str/i,
      friendly: () => 'Cannot combine text and numbers directly. Use str() to convert numbers to text first.',
    },
    {
      pattern: /TypeError:.*can't multiply sequence by non-int/i,
      friendly: () => 'Can only multiply text/lists by whole numbers. Convert to int if needed.',
    },
    {
      pattern: /TypeError:.*unsupported operand type/i,
      friendly: () => 'These types cannot be used together with that operator. Check your variable types.',
    },
    {
      pattern: /TypeError:.*takes (\d+) positional argument.*but (\d+)/i,
      friendly: (match) => `Function expects ${match[1]} argument(s) but got ${match[2]}. Check the number of values you're passing.`,
    },
    {
      pattern: /TypeError:.*missing (\d+) required positional argument/i,
      friendly: (match) => `Missing ${match[1]} required argument(s). Check the function call has all needed values.`,
    },
    {
      pattern: /TypeError:.*missing.*required.*argument.*'(\w+)'/i,
      friendly: (match) => `Missing required argument "${match[1]}". Add this value to your function call.`,
    },
    {
      pattern: /TypeError:.*got an unexpected keyword argument '(\w+)'/i,
      friendly: (match) => `"${match[1]}" is not a valid argument name for this function. Check spelling.`,
    },
    {
      pattern: /TypeError:.*object cannot be interpreted as an integer/i,
      friendly: () => 'Expected a whole number here. Convert with int() if needed.',
    },
    {
      pattern: /TypeError:.*unhashable type/i,
      friendly: () => 'This type cannot be used as a dictionary key or in a set. Use a string, number, or tuple instead.',
    },
    {
      pattern: /TypeError:.*argument.*must be.*not '(\w+)'/i,
      friendly: (match) => `Wrong type: got ${match[1]} but expected a different type. Check your variable.`,
    },

    // ValueError variations
    {
      pattern: /ValueError:.*invalid literal for int\(\) with base 10/i,
      friendly: () => 'Cannot convert this text to a number. Make sure the text contains only digits.',
    },
    {
      pattern: /ValueError:.*could not convert string to float/i,
      friendly: () => 'Cannot convert this text to a decimal number. Check for non-numeric characters.',
    },
    {
      pattern: /ValueError:.*too many values to unpack/i,
      friendly: () => 'Too many values on the right side. Add more variables on the left to receive them all.',
    },
    {
      pattern: /ValueError:.*not enough values to unpack/i,
      friendly: () => 'Not enough values on the right side. Remove some variables on the left.',
    },
    {
      pattern: /ValueError:.*is not in list/i,
      friendly: () => 'Value not found in the list. Check spelling or if the item exists.',
    },
    {
      pattern: /ValueError:.*substring not found/i,
      friendly: () => 'Text not found in the string. Check spelling or if the text exists.',
    },
    {
      pattern: /ValueError:.*math domain error/i,
      friendly: () => 'Math error: invalid input for this operation (like sqrt of negative number).',
    },
    {
      pattern: /ValueError:.*empty/i,
      friendly: () => 'Cannot perform this operation on an empty sequence.',
    },

    // IndexError variations
    {
      pattern: /IndexError:.*list index out of range/i,
      friendly: () => 'List index too high or low. Remember: a 3-item list uses indices 0, 1, 2 (or -1, -2, -3).',
    },
    {
      pattern: /IndexError:.*string index out of range/i,
      friendly: () => 'String index too high or low. The index must be less than the string length.',
    },
    {
      pattern: /IndexError:.*tuple index out of range/i,
      friendly: () => 'Tuple index too high or low. Remember indices start at 0.',
    },
    {
      pattern: /IndexError:.*index out of range/i,
      friendly: () => 'Index too high or low. Remember indices start at 0 and go up to length-1.',
    },

    // KeyError
    {
      pattern: /KeyError:.*'([^']+)'/i,
      friendly: (match) => `Key "${match[1]}" not found in dictionary. Check spelling or use .get() for safe access.`,
    },
    {
      pattern: /KeyError/i,
      friendly: () => 'Key not found in dictionary. Check if the key exists or use .get() for safe access.',
    },

    // AttributeError
    {
      pattern: /AttributeError:.*'NoneType' object has no attribute '(\w+)'/i,
      friendly: (match) => `Trying to use .${match[1]} on None. A function might have forgotten to return a value.`,
    },
    {
      pattern: /AttributeError:.*'(\w+)' object has no attribute '(\w+)'/i,
      friendly: (match) => `"${match[1]}" doesn't have ".${match[2]}". Check spelling or if this type supports it.`,
    },

    // ZeroDivisionError
    {
      pattern: /ZeroDivisionError:.*division by zero/i,
      friendly: () => 'Cannot divide by zero. Check your divisor isn\'t zero before dividing.',
    },
    {
      pattern: /ZeroDivisionError:.*modulo by zero/i,
      friendly: () => 'Cannot use % (modulo) with zero. Check your divisor isn\'t zero.',
    },
    {
      pattern: /ZeroDivisionError/i,
      friendly: () => 'Cannot divide by zero. Check your divisor value.',
    },

    // RecursionError
    {
      pattern: /RecursionError|maximum recursion depth exceeded/i,
      friendly: () => 'Function calls itself too many times. Add a base case to stop the recursion.',
    },

    // StopIteration
    {
      pattern: /StopIteration/i,
      friendly: () => 'Tried to get next item but sequence is empty. Check if there are items left.',
    },

    // AssertionError
    {
      pattern: /AssertionError/i,
      friendly: () => 'Assertion failed - the condition was False. Check your test condition.',
    },

    // FileNotFoundError
    {
      pattern: /FileNotFoundError/i,
      friendly: () => 'File not found. Check the filename and path are correct.',
    },

    // OverflowError
    {
      pattern: /OverflowError/i,
      friendly: () => 'Number too large to handle. Try using smaller numbers.',
    },

    // MemoryError
    {
      pattern: /MemoryError/i,
      friendly: () => 'Ran out of memory. Your code might be creating too much data.',
    },

    // Import errors (keep at end as catch-all)
    {
      pattern: /ModuleNotFoundError:.*No module named '(\w+)'/i,
      friendly: (match) => `Module "${match[1]}" not available. This browser environment only supports core Python.`,
    },
    {
      pattern: /ImportError:.*cannot import name '(\w+)'/i,
      friendly: (match) => `Cannot import "${match[1]}". Check spelling or if it exists in the module.`,
    },
    {
      pattern: /ModuleNotFoundError|ImportError/i,
      friendly: () => 'Module not available. This browser environment only supports core Python features.',
    },
  ];

  function formatErrorMessage(err) {
    if (!err) return { errorType: 'Error', message: 'Unknown error' };
    if (err instanceof TimeoutError) {
      return { errorType: 'TimeoutError', message: 'Code took too long to run. Check for infinite loops.' };
    }

    // Extract raw message from various error formats
    // Skulpt errors have args array, Pyodide/standard errors have message
    let rawMsg = '';
    if (err && typeof err.message === 'string' && err.message.trim()) {
      rawMsg = err.message.trim();
    } else if (err && err.args && Array.isArray(err.args) && err.args.length > 0) {
      // Skulpt error format: args is an array with the message
      rawMsg = String(err.args[0] || '');
    } else if (err && typeof err.toString === 'function') {
      rawMsg = err.toString();
    } else {
      rawMsg = String(err);
    }

    // Clean up Skulpt's verbose error format if present
    // e.g., "SyntaxError: EOF in multi-line statement on line 2" -> extract just the error
    rawMsg = rawMsg.trim();

    // Extract the Python error type (e.g., "SyntaxError", "NameError")
    const errorType = extractErrorType(rawMsg);

    // Try to find a beginner-friendly explanation
    for (const { pattern, friendly } of FRIENDLY_ERRORS) {
      const match = rawMsg.match(pattern);
      if (match) {
        const friendlyMsg = friendly(match);
        // Lowercase first character since it follows "This error means"
        const lowerFriendly = friendlyMsg.charAt(0).toLowerCase() + friendlyMsg.slice(1);
        return { errorType, message: `${errorType}. This error means ${lowerFriendly}` };
      }
    }

    // Fallback: clean up the raw message
    // Remove "on line X" and technical prefixes
    let cleaned = rawMsg
      .replace(/\s+on line \d+/gi, '')
      .replace(/^(Sk\.builtin\.|sk\.)?/i, '')
      .trim();

    return { errorType, message: cleaned || rawMsg };
  }

  function isConsentGranted(config) {
    if (!config) return false;
    const consent = (config.telemetryConsent || '').toString().trim().toLowerCase();
    if (!consent) return false;
    if (['1', 'true', 'yes', 'y', 'granted', 'allow', 'allowed', 'given'].includes(consent)) {
      return true;
    }
    if (['0', 'false', 'no', 'n', 'denied', 'declined', 'revoked'].includes(consent)) {
      return false;
    }
    return false;
  }

  function createTelemetryClient(config) {
    const consent = isConsentGranted(config);
    const rawBase = config && config.telemetryBaseUrl;
    const normalisedBase = typeof rawBase === 'string' ? rawBase.trim() : rawBase;
    const disabledBase = !normalisedBase
      || ['disabled', 'none', 'off', 'false'].includes(String(normalisedBase).toLowerCase());
    const baseUrl = disabledBase ? null : (normalisedBase || DEFAULT_CONFIG.telemetryBaseUrl);
    if (!consent || !baseUrl || typeof global.fetch !== 'function') {
      return {
        emit: () => false,
        hasConsent: () => consent && Boolean(baseUrl),
      };
    }
    let supportedEvents = null;
    const configuredEvents = config && (config.telemetryEvents || config.telemetryAllowedEvents);
    if (Array.isArray(configuredEvents) && configuredEvents.length) {
      supportedEvents = new Set(configuredEvents.map((name) => String(name || '').trim()).filter(Boolean));
    } else if (typeof configuredEvents === 'string' && configuredEvents.trim()) {
      supportedEvents = new Set(configuredEvents.split(',').map((name) => name.trim()).filter(Boolean));
    } else {
      supportedEvents = new Set();
    }
    if (!supportedEvents.size) {
      Object.values(EVENT_NAMES).forEach((eventName) => supportedEvents.add(eventName));
    }
    function buildPayload(eventName, detail) {
      const payload = {
        event: eventName,
        item_id: config.itemId || null,
        learner_id: config.learnerId || null,
        attempt_id: config.attemptId || null,
        session_id: config.sessionId || null,
        engine: config.engine,
        timestamp: new Date().toISOString(),
      };
      if (detail && typeof detail === 'object') {
        Object.keys(detail).forEach((key) => {
          if (detail[key] !== undefined) payload[key] = detail[key];
        });
      }
      return payload;
    }
    async function emit(eventName, detail) {
      if (!eventName) return false;
      if (!supportedEvents.has(eventName)) return false;
      const url = `${baseUrl.replace(/\/$/, '')}/${eventName}`;
      const body = JSON.stringify(buildPayload(eventName, detail));
      try {
        await global.fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body,
        });
        return true;
      } catch (err) {
        console.warn('Telemetry emit failed', eventName, err);
        return false;
      }
    }
    return {
      emit,
      hasConsent: () => consent,
    };
  }

  function createParentMessenger(config) {
    const canMessage = typeof global !== 'undefined'
      && global.parent
      && global.parent !== global
      && typeof global.parent.postMessage === 'function';
    if (!canMessage) {
      return () => false;
    }
    const originFromConfig = config && (config.parentOrigin || config.parent_origin);
    const fallbackOrigin = global.location && global.location.origin;
    const targetOrigin = originFromConfig || fallbackOrigin || '*';
    const safeOrigin = !targetOrigin || targetOrigin === 'null' ? '*' : targetOrigin;
    return (type, detail) => {
      if (!type) return false;
      const payload = Object.assign({ type }, detail || {});
      try {
        global.parent.postMessage(payload, safeOrigin);
        return true;
      } catch (err) {
        return false;
      }
    };
  }

  function createWidget(doc, block, index, config, telemetry, engineManager, notifyParent) {
    const pre = block.preEl;
    const codeEl = block.codeEl;
    const originalCode = codeEl ? codeEl.textContent : '';
    const cellId = getCellId(codeEl || pre, index);
    const hintText = getLiveHint(codeEl || pre);
    const expectedOutput = getExpectedOutput(pre);
    const reflectionPrompt = getLiveReflectionPrompt(codeEl || pre, config.reflectionPrompt);
    const timeoutMs = toNumber(codeEl && codeEl.getAttribute('data-timeout-ms'), config.timeoutMs);
    const lessonUrl = config.lessonUrl || (doc && doc.location ? doc.location.href : null);
    const postToParent = typeof notifyParent === 'function' ? notifyParent : () => false;

    const wrapper = doc.createElement('section');
    wrapper.className = 'xelra-live';
    wrapper.dataset.cellId = cellId;

    const labelId = `${cellId}-label`;
    const textareaId = `${cellId}-input`;
    const outputId = `${cellId}-output`;

    const label = doc.createElement('label');
    label.className = 'xelra-live__label';
    label.setAttribute('for', textareaId);
    label.id = labelId;
    label.textContent = `Python playground ${index + 1}`;

    const textarea = doc.createElement('textarea');
    textarea.className = 'xelra-live__editor';
    textarea.id = textareaId;
    textarea.setAttribute('aria-labelledby', labelId);
    textarea.value = originalCode ? originalCode.trimEnd() : '';

    const controls = doc.createElement('div');
    controls.className = 'xelra-live__controls';

    const status = doc.createElement('div');
    status.className = 'xelra-live__status';
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');

    const output = doc.createElement('pre');
    output.className = 'xelra-live__output';
    output.id = outputId;
    output.setAttribute('role', 'region');
    output.setAttribute('aria-live', 'polite');
    output.setAttribute('tabindex', '0');

    let validationFeedback = null;
    if (expectedOutput !== null) {
      validationFeedback = doc.createElement('div');
      validationFeedback.className = 'xelra-live__validation';
      validationFeedback.setAttribute('role', 'status');
      validationFeedback.setAttribute('aria-live', 'polite');
      validationFeedback.hidden = true;
    }

    const runBtn = doc.createElement('button');
    runBtn.type = 'button';
    runBtn.className = 'xelra-live__button xelra-live__button--run';
    runBtn.textContent = 'Run (Ctrl+Enter)';
    runBtn.addEventListener('click', () => execute());

    const resetBtn = doc.createElement('button');
    resetBtn.type = 'button';
    resetBtn.className = 'xelra-live__button xelra-live__button--reset';
    resetBtn.textContent = 'Reset (Ctrl+. )';
    resetBtn.addEventListener('click', () => reset());

    controls.appendChild(runBtn);
    controls.appendChild(resetBtn);

    let hintBtn = null;
    let hintRegion = null;
    if (hintText) {
      hintBtn = doc.createElement('button');
      hintBtn.type = 'button';
      hintBtn.className = 'xelra-live__button xelra-live__button--hint';
      hintBtn.textContent = 'Hint';
      hintRegion = doc.createElement('div');
      hintRegion.className = 'xelra-live__hint';
      hintRegion.hidden = true;
      hintRegion.setAttribute('role', 'note');
      hintRegion.textContent = hintText;
      controls.appendChild(hintBtn);
      hintBtn.addEventListener('click', () => {
        const wasHidden = hintRegion.hidden;
        hintRegion.hidden = !hintRegion.hidden;
        hintBtn.setAttribute('aria-expanded', String(!hintRegion.hidden));
        if (!hintRegion.hidden) {
          telemetry.emit(EVENT_NAMES.hint, { cell_id: cellId });
        }
      });
    }

    let reflectionForm = null;
    if (reflectionPrompt) {
      reflectionForm = doc.createElement('form');
      reflectionForm.className = 'xelra-live__reflection';
      reflectionForm.innerHTML = `
        <label class="xelra-live__reflection-label">
          ${reflectionPrompt}
          <textarea class="xelra-live__reflection-input" rows="3"></textarea>
        </label>
        <button type="submit" class="xelra-live__button xelra-live__button--reflection">Submit reflection</button>
      `;
      reflectionForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const reflectionInput = reflectionForm.querySelector('textarea');
        const value = reflectionInput ? reflectionInput.value.trim() : '';
        telemetry.emit(EVENT_NAMES.reflection, { cell_id: cellId, response: value });
        reflectionForm.classList.add('xelra-live__reflection--submitted');
      });
    }

    if (config.arlNudgeText) {
      const nudge = doc.createElement('div');
      nudge.className = 'xelra-live__arl-nudge';
      nudge.textContent = config.arlNudgeText;
      wrapper.appendChild(nudge);
      telemetry.emit(EVENT_NAMES.arlNudge, { cell_id: cellId, message: config.arlNudgeText });
    }

    wrapper.appendChild(label);
    wrapper.appendChild(textarea);
    wrapper.appendChild(controls);
    wrapper.appendChild(status);
    wrapper.appendChild(output);
    if (validationFeedback) {
      wrapper.appendChild(validationFeedback);
    }
    if (hintRegion) {
      wrapper.appendChild(hintRegion);
    }
    if (reflectionForm) {
      wrapper.appendChild(reflectionForm);
    }

    let lastRunCode = textarea.value;

    function reset() {
      textarea.value = originalCode ? originalCode.trimEnd() : '';
      output.textContent = '';
      status.textContent = 'Reset to original example.';
      if (validationFeedback) {
        validationFeedback.hidden = true;
      }
      if (hintBtn && hintRegion) {
        hintRegion.hidden = true;
        hintBtn.setAttribute('aria-expanded', 'false');
      }
      if (reflectionForm) {
        reflectionForm.classList.remove('xelra-live__reflection--submitted');
        const reflectionInput = reflectionForm.querySelector('textarea');
        if (reflectionInput) reflectionInput.value = '';
      }
    }

    function disableButtons(disabled) {
      runBtn.disabled = disabled;
      resetBtn.disabled = disabled;
      if (hintBtn) hintBtn.disabled = disabled;
      if (reflectionForm) {
        const submit = reflectionForm.querySelector('button[type="submit"]');
        if (submit) submit.disabled = disabled;
      }
    }

    async function execute() {
      const code = textarea.value;
      const basePayload = { cell_id: cellId, code_size: code.length, engine: engineManager.getActiveName() };
      telemetry.emit(EVENT_NAMES.run, { ...basePayload, status: 'started' });
      status.textContent = 'Running...';
      disableButtons(true);
      const startTime = (global.performance && typeof global.performance.now === 'function') ? global.performance.now() : Date.now();
      let runOk = false;
      let durationMs = 0;
      try {
        const engine = await engineManager.ensureEngine();
        const result = await runWithTimeout(() => engine.run(code), timeoutMs, engine);
        const text = normaliseEngineResult(result);
        console.debug('[xelra-live] run result', { cellId, result, text });
        output.textContent = text;
        status.textContent = 'Completed successfully.';
        lastRunCode = code;
        if (validationFeedback && expectedOutput !== null) {
          const actual = normaliseForComparison(text);
          const expected = normaliseForComparison(expectedOutput);
          const match = actual === expected;
          validationFeedback.hidden = false;
          validationFeedback.className = match
            ? 'xelra-live__validation xelra-live__validation--correct'
            : 'xelra-live__validation xelra-live__validation--mismatch';
          validationFeedback.textContent = match
            ? 'Correct! Your output matches the expected result.'
            : 'Not quite — your output doesn\'t match the expected result. Keep trying or reveal the answer.';
        }
        const stopTime = ((global.performance && typeof global.performance.now === 'function') ? global.performance.now() : Date.now());
        const duration = stopTime - startTime;
        durationMs = Math.max(0, Math.round(duration));
        telemetry.emit(EVENT_NAMES.run, { ...basePayload, status: 'success', duration_ms: durationMs, output_preview: text.slice(0, 120) });
        telemetry.emit(EVENT_NAMES.success, { ...basePayload, status: 'success', duration_ms: durationMs, output_preview: text.slice(0, 120) });
        runOk = true;
      } catch (err) {
        const taxonomy = mapError(err);
        const { errorType, message } = formatErrorMessage(err);
        console.error('[xelra-live] run error', { cellId, err, taxonomy, errorType, message });
        output.textContent = message;
        status.textContent = errorType;
        if (validationFeedback) {
          validationFeedback.hidden = true;
        }
        telemetry.emit(EVENT_NAMES.run, { ...basePayload, status: 'error', error_type: errorType, error_message: message });
        const stopTime = ((global.performance && typeof global.performance.now === 'function') ? global.performance.now() : Date.now());
        durationMs = Math.max(0, Math.round(stopTime - startTime));
        runOk = false;
      } finally {
        disableButtons(false);
        const elapsed = durationMs || Math.max(0, Math.round(((global.performance && typeof global.performance.now === 'function') ? global.performance.now() : Date.now()) - startTime));
        postToParent('XELRA_CODE_RUN', {
          item_id: config.itemId || null,
          lesson_url: lessonUrl,
          cell_id: cellId,
          ok: runOk,
          ms: elapsed,
        });
      }
    }

    textarea.addEventListener('keydown', (event) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        execute();
      } else if ((event.ctrlKey || event.metaKey) && (event.key === '.' || event.code === 'Period')) {
        event.preventDefault();
        reset();
      }
    });

    telemetry.emit(EVENT_NAMES.impression, { cell_id: cellId, code_size: (originalCode || '').length });

    return { wrapper, pre, execute, reset, cellId, getLastRunCode: () => lastRunCode };
  }

  function bootstrap(doc) {
    doc = doc || global.document;
    if (!doc) return null;
    const config = parseConfig(doc);
    if (!config) return null;
    const blocks = detectLiveBlocks(doc);
    if (!blocks.length) return { config, widgets: [] };
    const telemetry = createTelemetryClient(config);
    const engineManager = createEngineManager(config);
    const notifyParent = createParentMessenger(config);
    const widgets = [];
    blocks.forEach((block, index) => {
      const widget = createWidget(doc, block, index, config, telemetry, engineManager, notifyParent);
      const pre = block.preEl;
      if (pre && pre.parentNode) {
        pre.parentNode.replaceChild(widget.wrapper, pre);
      }
      widgets.push(widget);
    });
    return { config, widgets };
  }

  function autoBootstrap() {
    if (!global.document) return;
    if (global.__XELRA_DISABLE_AUTOBOOT__) return;
    const init = () => bootstrap(global.document);
    if (global.document.readyState === 'loading') {
      global.document.addEventListener('DOMContentLoaded', init, { once: true });
    } else {
      init();
    }
  }

  autoBootstrap();

  const api = {
    bootstrap,
    parseConfig,
    detectLiveBlocks,
    mapError,
    TimeoutError,
    __test: {
      loadScriptOnce,
      createEngineManager,
      runWithTimeout,
      createTelemetryClient,
      createParentMessenger,
      isConsentGranted,
      normaliseEngineResult,
      createWidget,
      normaliseBoolean,
      toNumber,
      normaliseForComparison,
      getExpectedOutput,
    },
  };

  if (global.document && typeof global.document.dispatchEvent === 'function') {
    try {
      const eventName = 'xelra-md-live:ready';
      const detail = api;
      let readyEvent;
      if (typeof global.CustomEvent === 'function') {
        readyEvent = new global.CustomEvent(eventName, { detail });
      } else {
        readyEvent = new global.Event(eventName);
        readyEvent.detail = detail;
      }
      global.document.dispatchEvent(readyEvent);
    } catch (err) {
      // ignore dispatch failures
    }
  }

  return api;
});
