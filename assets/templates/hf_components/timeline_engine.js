/**
 * HyperFrames Timeline Engine
 * Keyframe-based animation controller với seekTo() frame-accurate
 * Hỗ trợ 15 animation preset + custom keyframes
 * Tích hợp requestAnimationFrame cho preview realtime
 */

'use strict';

// ─────────────────────────────────────────────
// Easing Functions
// ─────────────────────────────────────────────
const Easing = {
  linear:    t => t,
  easeIn:    t => t * t,
  easeOut:   t => t * (2 - t),
  easeInOut: t => t < 0.5 ? 2*t*t : -1 + (4-2*t)*t,
  bounce:    t => {
    const n1 = 7.5625, d1 = 2.75;
    if (t < 1/d1) return n1*t*t;
    if (t < 2/d1) return n1*(t-=1.5/d1)*t + 0.75;
    if (t < 2.5/d1) return n1*(t-=2.25/d1)*t + 0.9375;
    return n1*(t-=2.625/d1)*t + 0.984375;
  },
  elastic: t => {
    if (t === 0 || t === 1) return t;
    return -Math.pow(2, 10*t-10) * Math.sin((t*10-10.75) * (2*Math.PI/3));
  },
  spring: t => {
    // Approximation của spring cho easing context (không cần frame)
    return 1 - Math.pow(2, -8*t) * Math.cos(t * Math.PI * 2.5);
  },
};

// ─────────────────────────────────────────────
// Animation Presets (15 preset)
// ─────────────────────────────────────────────
const AnimPresets = {
  // --- Fade ---
  fadeIn:        { opacity: [0, 1], duration: 0.5, easing: 'easeOut' },
  fadeInDown:    { opacity: [0, 1], translateY: [-24, 0], duration: 0.5, easing: 'easeOut' },
  fadeInUp:      { opacity: [0, 1], translateY: [24, 0], duration: 0.5, easing: 'easeOut' },
  fadeInLeft:    { opacity: [0, 1], translateX: [-32, 0], duration: 0.5, easing: 'easeOut' },
  fadeInRight:   { opacity: [0, 1], translateX: [32, 0], duration: 0.5, easing: 'easeOut' },
  // --- Slide ---
  slideInLeft:   { opacity: [0, 1], translateX: [-60, 0], duration: 0.5, easing: 'easeOut' },
  slideInRight:  { opacity: [0, 1], translateX: [60, 0], duration: 0.5, easing: 'easeOut' },
  slideInUp:     { opacity: [0, 1], translateY: [60, 0], duration: 0.5, easing: 'easeOut' },
  // --- Zoom / Scale ---
  zoomIn:        { opacity: [0, 1], scale: [0.7, 1], duration: 0.5, easing: 'easeOut' },
  scaleUp:       { scale: [0.9, 1], duration: 0.4, easing: 'spring' },
  // --- Spring ---
  springUp:      { opacity: [0, 1], translateY: [20, 0], scale: [0.95, 1], duration: 0.6, easing: 'spring' },
  springLeft:    { opacity: [0, 1], translateX: [-20, 0], scale: [0.97, 1], duration: 0.6, easing: 'spring' },
  // --- Special ---
  highlight:     { opacity: [0.6, 1], scale: [0.98, 1], duration: 0.3, easing: 'easeOut' },
  blurIn:        { opacity: [0, 1], blur: [12, 0], scale: [1.05, 1], duration: 0.6, easing: 'easeOut' },
  // typewriter và kinetic được xử lý bởi component riêng
  typewriter:    { _special: 'typewriter' },
  kinetic:       { _special: 'kinetic' },
  drawSVG:       { _special: 'drawSVG' },
  countUp:       { _special: 'countUp' },
};

// ─────────────────────────────────────────────
// Keyframe Interpolator
// ─────────────────────────────────────────────
function interpolate(t, from, to, easing = 'easeOut') {
  const easeFn = Easing[easing] || Easing.easeOut;
  const progress = Math.min(1, Math.max(0, t));
  const eased = easeFn(progress);
  return from + eased * (to - from);
}

// ─────────────────────────────────────────────
// Animation Track — mỗi element có 1 track
// ─────────────────────────────────────────────
class AnimTrack {
  /**
   * @param {string} elementId
   * @param {object} spec - { preset?, delay, duration, easing?, keyframes? }
   */
  constructor(elementId, spec = {}) {
    this.elementId = elementId;
    this.delay = spec.delay ?? 0;
    this.duration = spec.duration ?? 0.5;
    this.easing = spec.easing ?? 'easeOut';
    this.preset = spec.preset ?? null;
    this.keyframes = spec.keyframes ?? null; // custom keyframes override preset
    this._resolved = this._resolveKeyframes();
  }

  _resolveKeyframes() {
    if (this.keyframes) return this.keyframes;
    if (!this.preset || !AnimPresets[this.preset]) return null;
    const p = AnimPresets[this.preset];
    if (p._special) return { _special: p._special };

    const kf = {};
    if (p.opacity)     kf.opacity     = p.opacity;
    if (p.translateY)  kf.translateY  = p.translateY;
    if (p.translateX)  kf.translateX  = p.translateX;
    if (p.scale)       kf.scale       = p.scale;
    if (p.blur)        kf.blur        = p.blur;
    return kf;
  }

  /**
   * Trả về CSS style object tại thời điểm timeSec
   * @param {number} timeSec - Thời gian cục bộ trong scene
   * @returns {object}
   */
  getStyle(timeSec) {
    const elapsed = timeSec - this.delay;
    if (elapsed < 0) {
      return { opacity: 0, transform: 'translateY(20px) scale(0.95)', visibility: 'hidden' };
    }
    if (!this._resolved || this._resolved._special) {
      // Special animations xử lý bởi component riêng
      return { opacity: elapsed >= 0 ? 1 : 0 };
    }

    const progress = Math.min(1, elapsed / this.duration);
    const kf = this._resolved;
    const easing = this.preset && AnimPresets[this.preset]?.easing
      ? AnimPresets[this.preset].easing
      : this.easing;

    const style = { visibility: 'visible' };
    const transforms = [];

    if (kf.opacity !== undefined) {
      style.opacity = interpolate(progress, kf.opacity[0], kf.opacity[1], easing);
    } else {
      style.opacity = 1;
    }
    if (kf.translateX !== undefined) {
      transforms.push(`translateX(${interpolate(progress, kf.translateX[0], kf.translateX[1], easing)}px)`);
    }
    if (kf.translateY !== undefined) {
      transforms.push(`translateY(${interpolate(progress, kf.translateY[0], kf.translateY[1], easing)}px)`);
    }
    if (kf.scale !== undefined) {
      transforms.push(`scale(${interpolate(progress, kf.scale[0], kf.scale[1], easing)})`);
    }
    if (kf.blur !== undefined) {
      style.filter = `blur(${interpolate(progress, kf.blur[0], kf.blur[1], easing)}px)`;
    }
    if (transforms.length) style.transform = transforms.join(' ');

    if (style.opacity < 0.01) style.visibility = 'hidden';
    return style;
  }

  /**
   * Kiểm tra có đang animate tại timeSec
   */
  isAnimating(timeSec) {
    if (!this._resolved || this._resolved._special) return false;
    const elapsed = timeSec - this.delay;
    return elapsed >= 0 && elapsed <= this.duration;
  }

  /**
   * Kiểm tra có đã hoàn thành
   */
  isDone(timeSec) {
    return timeSec >= this.delay + this.duration;
  }
}

// ─────────────────────────────────────────────
// HFTimeline — Controller chính
// ─────────────────────────────────────────────
class HFTimeline {
  constructor(fps = 30) {
    this.fps = fps;
    this._tracks = new Map();        // elementId → AnimTrack
    this._rafId = null;
    this._startTime = null;
    this._currentTime = 0;
    this._playing = false;
    this._onTick = null;             // callback(timeSec) mỗi frame
  }

  /**
   * Thêm animation track cho element
   * @param {string} elementId
   * @param {object} spec - { preset, delay, duration, easing, keyframes }
   * @returns {HFTimeline} - for chaining
   */
  add(elementId, spec = {}) {
    this._tracks.set(elementId, new AnimTrack(elementId, spec));
    return this;
  }

  /**
   * Áp dụng style lên DOM elements tại timeSec
   * Puppeteer gọi hàm này để render frame
   * @param {number} timeSec
   */
  seekTo(timeSec) {
    this._currentTime = timeSec;
    this._applyStyles(timeSec);
  }

  _applyStyles(timeSec) {
    for (const [elementId, track] of this._tracks) {
      const el = document.getElementById(elementId);
      if (!el) continue;
      const style = track.getStyle(timeSec);
      Object.assign(el.style, style);
    }
  }

  /**
   * Lấy CSS style cho một element mà không apply vào DOM
   */
  getStyle(elementId, timeSec) {
    const track = this._tracks.get(elementId);
    if (!track) return {};
    return track.getStyle(timeSec);
  }

  /**
   * Kiểm tra có element nào đang animate tại timeSec
   */
  isAnimating(timeSec) {
    for (const [, track] of this._tracks) {
      if (track.isAnimating(timeSec)) return true;
    }
    return false;
  }

  /**
   * Danh sách elements đang animate (để smart-skip trong Puppeteer render)
   */
  getAnimatingElements(timeSec) {
    const result = [];
    for (const [id, track] of this._tracks) {
      if (track.isAnimating(timeSec)) result.push(id);
    }
    return result;
  }

  /**
   * Preview realtime với requestAnimationFrame
   * @param {function} [onTick] - callback(timeSec) gọi mỗi frame
   */
  play(onTick = null) {
    if (this._playing) return;
    this._playing = true;
    this._onTick = onTick;
    this._startTime = performance.now() - this._currentTime * 1000;
    this._rafLoop();
  }

  pause() {
    this._playing = false;
    if (this._rafId) cancelAnimationFrame(this._rafId);
    this._rafId = null;
  }

  _rafLoop() {
    if (!this._playing) return;
    const now = performance.now();
    const timeSec = (now - this._startTime) / 1000;
    this._currentTime = timeSec;
    this._applyStyles(timeSec);
    if (this._onTick) this._onTick(timeSec);
    this._rafId = requestAnimationFrame(() => this._rafLoop());
  }

  reset() {
    this.pause();
    this._currentTime = 0;
    this._applyStyles(0);
  }

  /** Trả về thời gian scene kết thúc animation cuối cùng */
  getTotalDuration() {
    let max = 0;
    for (const [, track] of this._tracks) {
      max = Math.max(max, track.delay + track.duration);
    }
    return max;
  }
}

// ─────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { HFTimeline, AnimTrack, AnimPresets, Easing, interpolate };
} else {
  window.HFTimeline = HFTimeline;
  window.AnimPresets = AnimPresets;
  window.HFEasing = Easing;
}
