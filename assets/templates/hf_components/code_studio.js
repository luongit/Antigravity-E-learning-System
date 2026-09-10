/**
 * HyperFrames Code Studio
 * VS Code UI với character-by-character typewriter effect
 * Syntax highlighting: Python, JavaScript, TypeScript, SQL, Bash
 * Blinking cursor █
 */

'use strict';

// ─────────────────────────────────────────────
// Syntax Tokenizer (regex-based, lightweight)
// ─────────────────────────────────────────────
const SyntaxThemes = {
  'one-dark-pro': {
    keyword:    '#C678DD',
    string:     '#98C379',
    comment:    '#5C6370',
    number:     '#D19A66',
    function_:  '#61AFEF',
    operator:   '#56B6C2',
    class_:     '#E5C07B',
    decorator:  '#E06C75',
    default_:   '#ABB2BF',
    builtin:    '#E5C07B',
  },
};

const LanguagePatterns = {
  python: [
    { type: 'comment',   re: /#[^\n]*/g },
    { type: 'string',    re: /"""[\s\S]*?"""|'''[\s\S]*?'''|"[^"\n]*"|'[^'\n]*'/g },
    { type: 'decorator', re: /@\w+/g },
    { type: 'keyword',   re: /\b(def|class|import|from|return|if|else|elif|for|while|in|not|and|or|is|None|True|False|try|except|with|as|pass|lambda|yield|async|await|raise|del|global|nonlocal|assert|break|continue)\b/g },
    { type: 'builtin',   re: /\b(print|len|range|type|int|str|float|list|dict|tuple|set|bool|open|zip|map|filter|enumerate|sorted|reversed|abs|max|min|sum|round|input)\b/g },
    { type: 'function_', re: /\b([a-zA-Z_]\w*)\s*(?=\()/g },
    { type: 'number',    re: /\b\d+(\.\d+)?\b/g },
    { type: 'class_',    re: /\b([A-Z][a-zA-Z_]\w*)\b/g },
    { type: 'operator',  re: /[+\-*\/=<>!&|^~%:]+/g },
  ],
  javascript: [
    { type: 'comment',   re: /\/\/[^\n]*|\/\*[\s\S]*?\*\//g },
    { type: 'string',    re: /`[^`]*`|"[^"\n]*"|'[^'\n]*'/g },
    { type: 'keyword',   re: /\b(const|let|var|function|class|return|if|else|for|while|switch|case|break|continue|import|export|from|new|this|typeof|instanceof|null|undefined|true|false|async|await|try|catch|finally|throw|delete|in|of|do|extends|super|yield|static|get|set)\b/g },
    { type: 'builtin',   re: /\b(console|Math|JSON|Date|Array|Object|Promise|setTimeout|fetch|window|document)\b/g },
    { type: 'function_', re: /\b([a-zA-Z_$]\w*)\s*(?=\()/g },
    { type: 'number',    re: /\b\d+(\.\d+)?\b/g },
    { type: 'class_',    re: /\b([A-Z][a-zA-Z_]\w*)\b/g },
    { type: 'operator',  re: /[+\-*\/=<>!&|^~%:]+/g },
  ],
  typescript: [], // Dùng chung với javascript (thêm type keywords)
  sql: [
    { type: 'keyword',   re: /\b(SELECT|FROM|WHERE|AND|OR|NOT|IN|JOIN|LEFT|RIGHT|INNER|OUTER|ON|GROUP|BY|ORDER|HAVING|LIMIT|INSERT|INTO|VALUES|UPDATE|SET|DELETE|CREATE|TABLE|DROP|ALTER|INDEX|PRIMARY|KEY|FOREIGN|REFERENCES|NULL|IS|AS|DISTINCT|UNION|ALL|EXISTS|BETWEEN|LIKE|COUNT|SUM|AVG|MAX|MIN)\b/gi },
    { type: 'string',    re: /'[^']*'/g },
    { type: 'number',    re: /\b\d+(\.\d+)?\b/g },
    { type: 'comment',   re: /--[^\n]*/g },
  ],
  bash: [
    { type: 'comment',   re: /#[^\n]*/g },
    { type: 'string',    re: /"[^"]*"|'[^']*'/g },
    { type: 'keyword',   re: /\b(if|then|else|elif|fi|for|while|do|done|case|esac|function|in|return|local|export|echo|read|exit|shift|source|alias|unset|declare)\b/g },
    { type: 'operator',  re: /[|&;><$]+/g },
    { type: 'number',    re: /\b\d+\b/g },
  ],
};

// TypeScript inherits JS patterns
LanguagePatterns.typescript = [
  ...LanguagePatterns.javascript,
  { type: 'keyword', re: /\b(interface|type|enum|namespace|declare|abstract|implements|readonly|private|public|protected|override|satisfies|keyof|typeof|infer|never|unknown|any|void|string|number|boolean|object)\b/g },
];

function tokenize(code, language, theme = 'one-dark-pro') {
  const colors = SyntaxThemes[theme] || SyntaxThemes['one-dark-pro'];
  const patterns = LanguagePatterns[language] || [];
  const defaultColor = colors.default_;

  if (!patterns.length) return escapeHtml(code);

  // Build token map: position → { end, color }
  const tokens = new Map();
  for (const { type, re } of patterns) {
    const colorKey = type.endsWith('_') ? type.slice(0, -1) : type;
    const color = colors[colorKey] || colors[type] || defaultColor;
    const regex = new RegExp(re.source, re.flags.includes('g') ? re.flags : re.flags + 'g');
    let m;
    while ((m = regex.exec(code)) !== null) {
      if (!tokens.has(m.index)) {
        tokens.set(m.index, { end: m.index + m[0].length, color, text: m[0] });
      }
    }
  }

  // Rebuild HTML with colorized spans
  let result = '';
  let i = 0;
  const sortedPositions = [...tokens.keys()].sort((a, b) => a - b);
  for (const pos of sortedPositions) {
    if (i > pos) continue;
    if (i < pos) result += escapeHtml(code.slice(i, pos));
    const tok = tokens.get(pos);
    result += `<span style="color:${tok.color}">${escapeHtml(tok.text)}</span>`;
    i = tok.end;
  }
  if (i < code.length) result += escapeHtml(code.slice(i));
  return result;
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

// ─────────────────────────────────────────────
// Code Studio Component
// ─────────────────────────────────────────────
class CodeStudio {
  /**
   * @param {HTMLElement|string} container - Element hoặc ID
   * @param {object} config
   * @param {string} config.language     - python|javascript|typescript|sql|bash
   * @param {string} config.filename     - Tên file hiển thị trên titlebar
   * @param {string} config.code         - Code content
   * @param {number} [config.delay=0.5]  - Giây bắt đầu typewriter
   * @param {number} [config.duration=3] - Giây hoàn thành toàn bộ code
   * @param {string} [config.theme='one-dark-pro']
   * @param {number} [config.fontSize=19]
   * @param {boolean}[config.showLineNumbers=true]
   */
  constructor(container, config = {}) {
    this._container = typeof container === 'string'
      ? document.getElementById(container)
      : container;
    this.language = config.language ?? 'python';
    this.filename = config.filename ?? 'main.py';
    this.code = config.code ?? '';
    this.delay = config.delay ?? 0.5;
    this.duration = config.duration ?? 3.0;
    this.theme = config.theme ?? 'one-dark-pro';
    this.fontSize = config.fontSize ?? 19;
    this.showLineNumbers = config.showLineNumbers !== false;
    this._initialized = false;
    this._lastChars = -1;
    this._coloredCode = '';
  }

  _build() {
    if (this._initialized) return;
    this._initialized = true;

    const bgColors = { 'one-dark-pro': { bg: '#282C34', bar: '#21252B', border: '#181A1F' } };
    const colors = bgColors[this.theme] || bgColors['one-dark-pro'];

    this._container.style.cssText = `
      width: 100%;
      background: ${colors.bg};
      border: 1.5px solid ${colors.border};
      border-radius: 16px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 20px 45px rgba(0,0,0,0.75), 0 0 0 1px rgba(255,255,255,0.05);
    `;

    // Titlebar
    const bar = document.createElement('div');
    bar.style.cssText = `
      height: 44px;
      background: ${colors.bar};
      display: flex;
      align-items: center;
      padding: 0 16px;
      border-bottom: 1px solid ${colors.border};
      flex-shrink: 0;
    `;
    bar.innerHTML = `
      <div style="display:flex;gap:8px;">
        <div style="width:12px;height:12px;border-radius:50%;background:#EF4444;"></div>
        <div style="width:12px;height:12px;border-radius:50%;background:#F59E0B;"></div>
        <div style="width:12px;height:12px;border-radius:50%;background:#22C55E;"></div>
      </div>
      <div style="margin-left:18px;font-family:'Fira Code',monospace;font-size:13px;color:#6B7280;font-weight:600;">
        ${escapeHtml(this.filename)}
      </div>
    `;

    // Code area
    const codeArea = document.createElement('div');
    codeArea.style.cssText = `
      display: flex;
      flex: 1;
      overflow: hidden;
      padding: 20px 0;
    `;

    // Line numbers
    if (this.showLineNumbers) {
      const lines = this.code.split('\n');
      const lineNumEl = document.createElement('div');
      lineNumEl.style.cssText = `
        padding: 0 14px 0 20px;
        font-family: 'Fira Code', monospace;
        font-size: ${this.fontSize}px;
        line-height: 1.65;
        color: #4B5563;
        text-align: right;
        user-select: none;
        flex-shrink: 0;
      `;
      lineNumEl.innerHTML = lines.map((_, i) =>
        `<div>${i + 1}</div>`
      ).join('');
      codeArea.appendChild(lineNumEl);
    }

    // Code content
    this._codeEl = document.createElement('div');
    this._codeEl.style.cssText = `
      flex: 1;
      padding: 0 24px 0 ${this.showLineNumbers ? '0' : '24px'};
      font-family: 'Fira Code', 'Cascadia Code', monospace;
      font-size: ${this.fontSize}px;
      line-height: 1.65;
      color: ${SyntaxThemes[this.theme]?.default_ ?? '#ABB2BF'};
      white-space: pre-wrap;
      word-break: break-all;
      overflow: hidden;
    `;
    codeArea.appendChild(this._codeEl);

    this._container.appendChild(bar);
    this._container.appendChild(codeArea);

    // Pre-tokenize full code
    this._coloredCode = tokenize(this.code, this.language, this.theme);
  }

  /**
   * Render tại timeSec — hiển thị N ký tự theo progress
   */
  seekTo(timeSec) {
    this._build();
    const elapsed = timeSec - this.delay;
    if (elapsed < 0) {
      this._codeEl.innerHTML = '';
      this._lastChars = 0;
      return;
    }

    const progress = Math.min(1, elapsed / this.duration);
    const totalChars = this.code.length;
    const visibleChars = Math.floor(progress * totalChars);

    if (visibleChars === this._lastChars) return; // No change
    this._lastChars = visibleChars;

    const visibleCode = this.code.substring(0, visibleChars);
    const highlighted = tokenize(visibleCode, this.language, this.theme);

    // Thêm blinking cursor
    const cursor = '<span style="display:inline-block;width:10px;height:1em;background:#38BDF8;vertical-align:text-bottom;margin-left:2px;animation:hf-cursor-blink 0.8s step-end infinite;"></span>';
    this._codeEl.innerHTML = highlighted + (progress < 1 ? cursor : '');
  }

  isAnimating(timeSec) {
    const elapsed = timeSec - this.delay;
    return elapsed >= 0 && elapsed <= this.duration + 0.1;
  }

  isDone(timeSec) {
    return timeSec >= this.delay + this.duration;
  }
}

// CSS cho cursor blink (inject 1 lần vào head)
function injectCodeStudioCSS() {
  if (document.getElementById('hf-code-studio-css')) return;
  const style = document.createElement('style');
  style.id = 'hf-code-studio-css';
  style.textContent = `
    @keyframes hf-cursor-blink {
      0%, 100% { opacity: 1; }
      50% { opacity: 0; }
    }
  `;
  document.head.appendChild(style);
}

if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectCodeStudioCSS);
  } else {
    injectCodeStudioCSS();
  }
}

// ─────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { CodeStudio, tokenize, SyntaxThemes };
} else {
  window.HFCodeStudio = { CodeStudio, tokenize, SyntaxThemes };
}
