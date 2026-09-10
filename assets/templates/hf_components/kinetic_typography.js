/**
 * HyperFrames Kinetic Typography Engine
 * Word-by-word reveal, character split, gradient sweep, counter animation
 */

'use strict';

// ─────────────────────────────────────────────
// Word-by-Word Reveal (theo SRT timestamp)
// ─────────────────────────────────────────────
class WordReveal {
  /**
   * @param {HTMLElement} container
   * @param {string} text - Toàn bộ text cần hiển thị
   * @param {object} config
   * @param {number} config.startSec    - Giây bắt đầu reveal
   * @param {number} config.duration    - Tổng thời gian reveal toàn bộ text
   * @param {string} [config.color='#F8FAFC']
   * @param {string} [config.accentColor='#38BDF8'] - Màu từ đầu tiên
   */
  constructor(container, text, config = {}) {
    this.container = container;
    this.text = text;
    this.words = text.split(/\s+/).filter(Boolean);
    this.startSec = config.startSec ?? 0;
    this.duration = config.duration ?? 3.0;
    this.color = config.color ?? '#F8FAFC';
    this.accentColor = config.accentColor ?? '#38BDF8';
    this._rendered = false;
  }

  _render() {
    if (this._rendered) return;
    this._rendered = true;
    this.container.innerHTML = '';
    this.words.forEach((word, i) => {
      const span = document.createElement('span');
      span.setAttribute('data-word-idx', i);
      span.textContent = word + ' ';
      span.style.cssText = `
        display: inline;
        opacity: 0;
        transition: opacity 0.2s ease, color 0.3s ease;
        color: ${i === 0 ? this.accentColor : this.color};
      `;
      this.container.appendChild(span);
    });
  }

  seekTo(timeSec) {
    this._render();
    const elapsed = timeSec - this.startSec;
    if (elapsed < 0) return;
    const perWord = this.duration / Math.max(1, this.words.length);
    const spans = this.container.querySelectorAll('[data-word-idx]');
    spans.forEach((span, i) => {
      const wordElapsed = elapsed - i * perWord;
      span.style.opacity = Math.min(1, Math.max(0, wordElapsed / (perWord * 0.6)));
    });
  }

  isAnimating(timeSec) {
    const elapsed = timeSec - this.startSec;
    return elapsed >= 0 && elapsed <= this.duration + 0.3;
  }
}

// ─────────────────────────────────────────────
// Character Split Animation
// ─────────────────────────────────────────────
class CharSplit {
  /**
   * @param {HTMLElement} container
   * @param {string} text
   * @param {object} config
   * @param {number} config.startSec
   * @param {number} config.duration
   * @param {string} [config.preset='fadeInUp'] - fadeInUp | fadeInDown | scaleIn | slideLeft
   */
  constructor(container, text, config = {}) {
    this.container = container;
    this.text = text;
    this.chars = [...text]; // Split unicode-safe
    this.startSec = config.startSec ?? 0;
    this.duration = config.duration ?? 1.5;
    this.preset = config.preset ?? 'fadeInUp';
    this._rendered = false;
  }

  _render() {
    if (this._rendered) return;
    this._rendered = true;
    this.container.innerHTML = '';
    this.chars.forEach((ch, i) => {
      const span = document.createElement('span');
      span.setAttribute('data-char-idx', i);
      span.textContent = ch;
      span.style.cssText = `
        display: inline-block;
        opacity: 0;
        transition: none;
      `;
      this.container.appendChild(span);
    });
  }

  seekTo(timeSec) {
    this._render();
    const elapsed = timeSec - this.startSec;
    if (elapsed < 0) return;
    const perChar = this.duration / Math.max(1, this.chars.length);
    const spans = this.container.querySelectorAll('[data-char-idx]');
    spans.forEach((span, i) => {
      const charElapsed = elapsed - i * perChar;
      const progress = Math.min(1, Math.max(0, charElapsed / (perChar * 1.5)));
      span.style.opacity = progress;
      switch (this.preset) {
        case 'fadeInUp':
          span.style.transform = `translateY(${(1 - progress) * 10}px)`;
          break;
        case 'fadeInDown':
          span.style.transform = `translateY(${-(1 - progress) * 10}px)`;
          break;
        case 'scaleIn':
          span.style.transform = `scale(${0.7 + progress * 0.3})`;
          break;
        case 'slideLeft':
          span.style.transform = `translateX(${-(1 - progress) * 8}px)`;
          break;
      }
    });
  }

  isAnimating(timeSec) {
    const elapsed = timeSec - this.startSec;
    return elapsed >= 0 && elapsed <= this.duration + 0.3;
  }
}

// ─────────────────────────────────────────────
// Gradient Text Sweep Animation
// ─────────────────────────────────────────────
class GradientSweep {
  /**
   * Màu chạy ngang theo thời gian
   * @param {HTMLElement} el
   * @param {object} config
   * @param {string[]} config.colors  - Mảng màu cho gradient
   * @param {number} config.cycleSec  - Thời gian 1 chu kỳ (giây)
   * @param {number} [config.startSec=0]
   */
  constructor(el, config = {}) {
    this.el = el;
    this.colors = config.colors ?? ['#38BDF8', '#818CF8', '#10B981', '#38BDF8'];
    this.cycleSec = config.cycleSec ?? 4.0;
    this.startSec = config.startSec ?? 0;
    this._init();
  }

  _init() {
    this.el.style.backgroundClip = 'text';
    this.el.style.webkitBackgroundClip = 'text';
    this.el.style.color = 'transparent';
    this.el.style.backgroundSize = '200% 100%';
  }

  seekTo(timeSec) {
    const elapsed = timeSec - this.startSec;
    if (elapsed < 0) return;
    const cycle = (elapsed % this.cycleSec) / this.cycleSec;
    const pos = Math.round(cycle * 200);
    const gradient = `linear-gradient(90deg, ${this.colors.join(', ')})`;
    this.el.style.backgroundImage = gradient;
    this.el.style.backgroundPosition = `${pos}% 0`;
  }
}

// ─────────────────────────────────────────────
// Counter Animation (0 → N)
// ─────────────────────────────────────────────
class CounterAnim {
  /**
   * @param {HTMLElement} el
   * @param {object} config
   * @param {number} config.from       - Giá trị bắt đầu
   * @param {number} config.to         - Giá trị đích
   * @param {number} config.startSec
   * @param {number} config.duration
   * @param {string} [config.prefix='']
   * @param {string} [config.suffix='']
   * @param {number} [config.decimals=0]
   * @param {string} [config.easing='easeOut']
   */
  constructor(el, config = {}) {
    this.el = el;
    this.from = config.from ?? 0;
    this.to = config.to ?? 100;
    this.startSec = config.startSec ?? 0;
    this.duration = config.duration ?? 2.0;
    this.prefix = config.prefix ?? '';
    this.suffix = config.suffix ?? '';
    this.decimals = config.decimals ?? 0;
    this.easing = config.easing ?? 'easeOut';
  }

  _easeOut(t) { return t * (2 - t); }

  seekTo(timeSec) {
    const elapsed = timeSec - this.startSec;
    if (elapsed < 0) {
      this.el.textContent = `${this.prefix}${this.from.toFixed(this.decimals)}${this.suffix}`;
      return;
    }
    const progress = this.easing === 'easeOut'
      ? this._easeOut(Math.min(1, elapsed / this.duration))
      : Math.min(1, elapsed / this.duration);
    const value = this.from + progress * (this.to - this.from);
    this.el.textContent = `${this.prefix}${value.toFixed(this.decimals)}${this.suffix}`;
  }

  isAnimating(timeSec) {
    const elapsed = timeSec - this.startSec;
    return elapsed >= 0 && elapsed <= this.duration + 0.1;
  }
}

// ─────────────────────────────────────────────
// SVG Path Draw Animation
// ─────────────────────────────────────────────
class SVGDrawPath {
  /**
   * @param {SVGPathElement} pathEl
   * @param {object} config
   * @param {number} config.startSec
   * @param {number} config.duration
   * @param {string} [config.easing='easeInOut']
   */
  constructor(pathEl, config = {}) {
    this.pathEl = pathEl;
    this.startSec = config.startSec ?? 0;
    this.duration = config.duration ?? 1.5;
    this.easing = config.easing ?? 'easeInOut';
    this._totalLen = null;
  }

  _getTotalLength() {
    if (this._totalLen === null) {
      try {
        this._totalLen = this.pathEl.getTotalLength();
        this.pathEl.style.strokeDasharray = this._totalLen;
        this.pathEl.style.strokeDashoffset = this._totalLen;
      } catch {
        this._totalLen = 1000;
      }
    }
    return this._totalLen;
  }

  _easeInOut(t) { return t < 0.5 ? 2*t*t : -1+(4-2*t)*t; }

  seekTo(timeSec) {
    const len = this._getTotalLength();
    const elapsed = timeSec - this.startSec;
    if (elapsed < 0) {
      this.pathEl.style.strokeDashoffset = len;
      return;
    }
    const rawProgress = Math.min(1, elapsed / this.duration);
    const progress = this.easing === 'easeInOut' ? this._easeInOut(rawProgress) : rawProgress;
    this.pathEl.style.strokeDashoffset = len * (1 - progress);
  }

  isAnimating(timeSec) {
    const elapsed = timeSec - this.startSec;
    return elapsed >= 0 && elapsed <= this.duration;
  }
}

// ─────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { WordReveal, CharSplit, GradientSweep, CounterAnim, SVGDrawPath };
} else {
  window.HFKinetic = { WordReveal, CharSplit, GradientSweep, CounterAnim, SVGDrawPath };
}
