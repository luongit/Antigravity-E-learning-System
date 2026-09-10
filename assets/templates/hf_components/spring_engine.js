/**
 * HyperFrames Spring Engine — Thuần JavaScript
 * Triển khai spring physics frame-by-frame tự chủ hoàn toàn.
 * Không phụ thuộc bất kỳ thư viện bên ngoài nào.
 *
 * Sử dụng:
 *   const sv = new SpringValue({ stiffness: 150, damping: 15, mass: 1 });
 *   const progress = sv.calculate(frame, fps); // 0.0 → 1.0
 */

'use strict';

// ─────────────────────────────────────────────
// Core Spring Value
// ─────────────────────────────────────────────
class SpringValue {
  /**
   * @param {object} config
   * @param {number} [config.stiffness=150]  - Độ cứng lò xo (k)
   * @param {number} [config.damping=15]     - Hệ số cản (c)
   * @param {number} [config.mass=1]         - Khối lượng (m)
   * @param {number} [config.from=0]         - Giá trị bắt đầu
   * @param {number} [config.to=1]           - Giá trị đích
   * @param {number} [config.initialVelocity=0] - Vận tốc ban đầu
   */
  constructor(config = {}) {
    this.stiffness = config.stiffness ?? 150;
    this.damping = config.damping ?? 15;
    this.mass = config.mass ?? 1;
    this.from = config.from ?? 0;
    this.to = config.to ?? 1;
    this.initialVelocity = config.initialVelocity ?? 0;
    this._cache = new Map();
  }

  /**
   * Tính giá trị spring tại frame cụ thể.
   * @param {number} frame - Frame số (tính từ 0 khi animation bắt đầu)
   * @param {number} fps   - Frames per second (mặc định 30)
   * @returns {number}     - Giá trị trong khoảng [from, to]
   */
  calculate(frame, fps = 30) {
    if (frame <= 0) return this.from;
    const cacheKey = `${frame}:${fps}`;
    if (this._cache.has(cacheKey)) return this._cache.get(cacheKey);

    const timeSec = frame / fps;
    const result = this._solveSpring(timeSec);
    const mapped = this.from + result * (this.to - this.from);
    const clamped = Math.min(Math.max(mapped, Math.min(this.from, this.to)), Math.max(this.from, this.to));
    this._cache.set(cacheKey, clamped);
    return clamped;
  }

  /**
   * Giải phương trình dao động tắt dần.
   * Phương pháp: tích phân Euler cải tiến (Verlet velocity)
   */
  _solveSpring(t) {
    const { stiffness: k, damping: c, mass: m, initialVelocity: v0 } = this;
    const omega_n = Math.sqrt(k / m);
    const zeta = c / (2 * Math.sqrt(k * m));

    if (zeta < 1) {
      // Under-damped — dao động tắt dần (phổ biến nhất)
      const omega_d = omega_n * Math.sqrt(1 - zeta * zeta);
      const A = 1;
      const B = (v0 + zeta * omega_n) / omega_d;
      const decay = Math.exp(-zeta * omega_n * t);
      return 1 - decay * (A * Math.cos(omega_d * t) + B * Math.sin(omega_d * t));
    } else if (zeta === 1) {
      // Critically damped — về đích nhanh nhất không dao động
      const decay = Math.exp(-omega_n * t);
      return 1 - decay * (1 + (v0 + omega_n) * t);
    } else {
      // Over-damped — về đích chậm không dao động
      const r1 = -omega_n * (zeta - Math.sqrt(zeta * zeta - 1));
      const r2 = -omega_n * (zeta + Math.sqrt(zeta * zeta - 1));
      const C1 = (v0 - r2) / (r1 - r2);
      const C2 = 1 - C1;
      return 1 - (C1 * Math.exp(r1 * t) + C2 * Math.exp(r2 * t));
    }
  }

  clearCache() { this._cache.clear(); }
}

// ─────────────────────────────────────────────
// Presets
// ─────────────────────────────────────────────
const SpringPresets = {
  gentle:   { stiffness: 100, damping: 15, mass: 0.8 },
  bouncy:   { stiffness: 180, damping: 10, mass: 1.0 },
  stiff:    { stiffness: 200, damping: 26, mass: 1.0 },
  wobbly:   { stiffness: 180, damping: 8,  mass: 1.0 },
  slow:     { stiffness: 60,  damping: 14, mass: 1.0 },
  card:     { stiffness: 140, damping: 15, mass: 0.8 }, // dùng cho card reveal
  anchor:   { stiffness: 80,  damping: 14, mass: 1.0 }, // dùng cho visual anchor
};

/**
 * Hàm tiện ích tính toán spring animation
 * @param {object} opts
 * @param {number} opts.frame          - Frame hiện tại (tính từ khi animation bắt đầu)
 * @param {number} [opts.fps=30]       - FPS
 * @param {object} [opts.config]       - { stiffness, damping, mass }
 * @param {string} [opts.preset]       - Tên preset (gentle, bouncy, stiff, wobbly, slow, card, anchor)
 * @param {number} [opts.from=0]
 * @param {number} [opts.to=1]
 * @returns {number} Giá trị 0→1 (hoặc from→to)
 */
function spring({ frame, fps = 30, config = {}, preset = null, from = 0, to = 1 } = {}) {
  const baseConfig = preset ? { ...SpringPresets[preset], ...config } : config;
  const sv = new SpringValue({ ...baseConfig, from, to });
  return sv.calculate(frame, fps);
}

// ─────────────────────────────────────────────
// Spring Timeline — quản lý nhiều spring cùng lúc
// ─────────────────────────────────────────────
class SpringTimeline {
  constructor(fps = 30) {
    this.fps = fps;
    this._springs = new Map(); // id → { startSec, springValue, props }
  }

  /**
   * Thêm spring animation cho một phần tử
   * @param {string} id          - ID element hoặc animation
   * @param {number} startSec    - Thời điểm bắt đầu (giây)
   * @param {object} config      - SpringValue config hoặc preset
   * @param {object} [props]     - { opacity, translateY, scale, translateX, ... }
   */
  add(id, startSec, config = {}, props = {}) {
    const preset = config.preset || null;
    const baseConf = preset ? { ...SpringPresets[preset], ...config } : config;
    this._springs.set(id, {
      startSec,
      springValue: new SpringValue({ ...baseConf }),
      props: {
        opacity:     { from: 0, to: 1, ...props.opacity },
        translateY:  { from: 20, to: 0, ...props.translateY },
        scale:       { from: 0.95, to: 1, ...props.scale },
        translateX:  { from: 0, to: 0, ...props.translateX },
      },
    });
    return this;
  }

  /**
   * Lấy CSS style cho phần tử tại thời điểm timeSec
   * @param {string} id
   * @param {number} timeSec
   * @returns {object} { opacity, transform, visibility }
   */
  getStyle(id, timeSec) {
    const entry = this._springs.get(id);
    if (!entry) return {};

    const elapsed = timeSec - entry.startSec;
    if (elapsed < 0) {
      return { opacity: 0, transform: 'translateY(20px) scale(0.95)', visibility: 'hidden' };
    }

    const frame = Math.round(elapsed * this.fps);
    const sp = entry.springValue.calculate(frame, this.fps);

    const p = entry.props;
    const opacity = p.opacity.from + sp * (p.opacity.to - p.opacity.from);
    const ty = p.translateY.from + sp * (p.translateY.to - p.translateY.from);
    const scale = p.scale.from + sp * (p.scale.to - p.scale.from);
    const tx = p.translateX.from + sp * (p.translateX.to - p.translateX.from);

    return {
      opacity,
      transform: `translateX(${tx}px) translateY(${ty}px) scale(${scale})`,
      visibility: opacity > 0.01 ? 'visible' : 'hidden',
    };
  }

  /**
   * Kiểm tra có phần tử nào đang animate tại timeSec không
   */
  isAnimating(timeSec, settleDuration = 1.2) {
    for (const [, entry] of this._springs) {
      const elapsed = timeSec - entry.startSec;
      if (elapsed >= 0 && elapsed <= settleDuration) return true;
    }
    return false;
  }
}

// ─────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SpringValue, SpringPresets, SpringTimeline, spring };
} else {
  window.HFSpring = { SpringValue, SpringPresets, SpringTimeline, spring };
}
