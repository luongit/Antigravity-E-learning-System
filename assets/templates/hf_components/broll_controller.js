/**
 * HyperFrames B-roll Controller
 * Multi-clip chaining, auto-loop không freeze, crossfade, label badge
 * Fullscreen 1920×1080, z-index: 500
 */

'use strict';

class BrollController {
  /**
   * @param {Array} cutaways - Danh sách cutaway segments
   *   [{ startSec, endSec, label?, clips: [{ src, duration }] }]
   * @param {object} config
   * @param {string} [config.containerId='hf-broll']
   * @param {number} [config.crossfadeDuration=0.3]  - Thời gian crossfade giây
   * @param {boolean}[config.muted=true]              - Video muted (audio từ narration track)
   */
  constructor(cutaways = [], config = {}) {
    this.cutaways = cutaways;
    this.containerId = config.containerId ?? 'hf-broll';
    this.crossfadeDuration = config.crossfadeDuration ?? 0.3;
    this.muted = config.muted !== false;
    this._container = null;
    this._overlay = null;
    this._label = null;
    this._videoPool = []; // 2 video elements để crossfade
    this._activeIdx = 0;  // index trong pool đang hiển thị
    this._currentCutaway = null;
    this._currentClipIdx = 0;
    this._initialized = false;
  }

  // ─── Init DOM ───────────────────────────────
  init() {
    if (this._initialized) return;
    this._initialized = true;

    // Container fullscreen
    let container = document.getElementById(this.containerId);
    if (!container) {
      container = document.createElement('div');
      container.id = this.containerId;
      document.body.appendChild(container);
    }
    container.style.cssText = `
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      width: 1920px; height: 1080px;
      z-index: 500;
      overflow: hidden;
      display: none;
      background: #000;
    `;
    this._container = container;

    // 2 video elements để crossfade liền mạch
    for (let i = 0; i < 2; i++) {
      const vid = document.createElement('video');
      vid.style.cssText = `
        position: absolute; top: 0; left: 0;
        width: 100%; height: 100%;
        object-fit: cover;
        opacity: ${i === 0 ? 1 : 0};
        transition: opacity ${this.crossfadeDuration}s ease;
      `;
      vid.muted = this.muted;
      vid.playsInline = true;
      vid.loop = false; // loop được xử lý thủ công để tránh delay
      container.appendChild(vid);
      this._videoPool.push(vid);

      // Auto-chain: khi clip kết thúc, load clip tiếp theo
      vid.addEventListener('ended', () => this._onClipEnded(i));
      vid.addEventListener('timeupdate', () => this._onTimeUpdate(vid));
    }

    // Gradient overlay
    this._overlay = document.createElement('div');
    this._overlay.style.cssText = `
      position: absolute; top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(
        180deg,
        rgba(0,0,0,0.45) 0%,
        transparent 22%,
        transparent 68%,
        rgba(0,0,0,0.75) 100%
      );
      pointer-events: none;
      z-index: 10;
    `;
    container.appendChild(this._overlay);

    // Label badge
    this._label = document.createElement('div');
    this._label.style.cssText = `
      position: absolute;
      top: 48px; left: 64px;
      padding: 8px 22px;
      border-radius: 20px;
      background: rgba(15,23,42,0.85);
      border: 1.5px solid rgba(56,189,248,0.6);
      color: #38BDF8;
      font-family: 'Be Vietnam Pro', sans-serif;
      font-size: 15px; font-weight: 800;
      letter-spacing: 0.5px;
      display: none;
      align-items: center;
      gap: 10px;
      z-index: 600;
      backdrop-filter: blur(12px);
    `;
    this._label.innerHTML = `
      <div style="width:8px;height:8px;border-radius:50%;background:#38BDF8;box-shadow:0 0 8px #38BDF8;"></div>
      <span></span>
    `;
    container.appendChild(this._label);
  }

  // ─── Clip management ────────────────────────
  _onClipEnded(poolIdx) {
    if (!this._currentCutaway) return;
    const clips = this._currentCutaway.clips || [];
    if (clips.length <= 1) {
      // Loop lại clip duy nhất — không dùng video.loop để tránh freeze delay
      const vid = this._videoPool[poolIdx];
      vid.currentTime = 0;
      vid.play().catch(() => {});
      return;
    }
    // Chuyển sang clip tiếp theo trong danh sách
    this._currentClipIdx = (this._currentClipIdx + 1) % clips.length;
    this._loadClip(this._currentClipIdx, true);
  }

  _onTimeUpdate(vid) {
    if (!this._currentCutaway) return;
    const clips = this._currentCutaway.clips || [];
    const clipSpec = clips[this._currentClipIdx];
    // Nếu clip có maxDuration được chỉ định, reset về đầu khi đến giới hạn
    if (clipSpec?.duration && vid.currentTime >= clipSpec.duration) {
      vid.currentTime = 0;
    }
  }

  /**
   * Load và phát clip với index trong cutaway.clips
   * @param {number} clipIdx
   * @param {boolean} crossfade - Dùng crossfade hay show ngay
   */
  _loadClip(clipIdx, crossfade = false) {
    const clips = this._currentCutaway?.clips;
    if (!clips || !clips[clipIdx]) return;

    const clip = clips[clipIdx];
    const nextIdx = crossfade ? 1 - this._activeIdx : this._activeIdx;
    const nextVid = this._videoPool[nextIdx];

    nextVid.src = clip.src;
    nextVid.currentTime = 0;
    nextVid.load();
    nextVid.play().catch(() => {});

    if (crossfade) {
      // Fade in next, fade out current
      nextVid.style.opacity = '1';
      this._videoPool[this._activeIdx].style.opacity = '0';
      this._activeIdx = nextIdx;
    } else {
      nextVid.style.opacity = '1';
    }
  }

  // ─── Public API ─────────────────────────────

  /**
   * Tìm cutaway đang active tại timeSec
   */
  _findActive(timeSec) {
    return this.cutaways.find(c => timeSec >= c.startSec && timeSec < c.endSec) ?? null;
  }

  /**
   * Seek toàn bộ controller đến timeSec
   * Gọi từ HFRenderer.seekTo()
   */
  seekTo(timeSec) {
    if (!this._initialized) this.init();
    const cutaway = this._findActive(timeSec);

    if (cutaway) {
      // Hiển thị B-roll
      if (this._container) this._container.style.display = 'block';

      // Nếu đây là cutaway mới
      if (cutaway !== this._currentCutaway) {
        this._currentCutaway = cutaway;
        this._currentClipIdx = 0;
        this._loadClip(0, false);
      }

      // Label
      if (cutaway.label) {
        this._label.style.display = 'flex';
        this._label.querySelector('span').textContent = cutaway.label;
      } else {
        this._label.style.display = 'none';
      }

    } else {
      // Ẩn B-roll, hiện slide
      if (this._container) this._container.style.display = 'none';
      this._currentCutaway = null;

      // Dừng tất cả video để tiết kiệm tài nguyên
      this._videoPool.forEach(v => { try { v.pause(); } catch {} });
    }
  }

  /**
   * Kiểm tra có đang hiển thị B-roll tại timeSec
   */
  isActive(timeSec) {
    return !!this._findActive(timeSec);
  }

  /**
   * Kiểm tra có chuyển trạng thái tại timeSec không
   * (dùng để smart-skip trong Puppeteer render)
   */
  hasChange(timeSec, prevTimeSec) {
    const cur = this._findActive(timeSec);
    const prev = this._findActive(prevTimeSec);
    return (!!cur) !== (!!prev) ||
      (cur && prev && cur !== prev) ||
      (cur && (
        Math.abs(timeSec - cur.startSec) < 0.2 ||
        Math.abs(timeSec - cur.endSec) < 0.2
      ));
  }
}

// ─────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { BrollController };
} else {
  window.HFBroll = { BrollController };
}
