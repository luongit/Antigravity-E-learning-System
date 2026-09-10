/**
 * HyperFrames Audio Manager
 * Multi-track audio: narration + BGM Lo-Fi
 * Web Audio API GainNode — điều khiển volume từng track
 * Silent mode khi Puppeteer render (không phát âm thanh)
 */

'use strict';

class AudioManager {
  /**
   * @param {object} config
   * @param {string} [config.narrationSrc]    - Đường dẫn file MP3 narration
   * @param {string} [config.bgmSrc]          - Đường dẫn file MP3 BGM
   * @param {number} [config.narrationVolume=1.0]
   * @param {number} [config.bgmVolume=0.12]  - 12% âm lượng BGM
   * @param {boolean}[config.silent=false]    - true khi Puppeteer render
   * @param {number} [config.sceneOffset=0]   - Offset giây narration (nếu scene bắt đầu giữa audio)
   */
  constructor(config = {}) {
    this.narrationSrc = config.narrationSrc ?? null;
    this.bgmSrc = config.bgmSrc ?? null;
    this.narrationVolume = config.narrationVolume ?? 1.0;
    this.bgmVolume = config.bgmVolume ?? 0.12;
    this.silent = config.silent ?? false;
    this.sceneOffset = config.sceneOffset ?? 0;

    this._ctx = null;
    this._narrationEl = null;
    this._bgmEl = null;
    this._narGain = null;
    this._bgmGain = null;
    this._initialized = false;
  }

  /**
   * Khởi tạo Web Audio API và load audio elements
   * Gọi sau user interaction (click/keypress) hoặc trong preview mode
   */
  async init() {
    if (this.silent || this._initialized) return;
    try {
      this._ctx = new (window.AudioContext || window.webkitAudioContext)();
      await this._ctx.resume();
    } catch (e) {
      console.warn('[AudioManager] AudioContext init failed:', e.message);
      this.silent = true;
      return;
    }

    // Track 1: Narration
    if (this.narrationSrc) {
      this._narrationEl = this._createAudio(this.narrationSrc, false);
      const narSource = this._ctx.createMediaElementSource(this._narrationEl);
      this._narGain = this._ctx.createGain();
      this._narGain.gain.value = this.narrationVolume;
      narSource.connect(this._narGain).connect(this._ctx.destination);
    }

    // Track 2: BGM
    if (this.bgmSrc) {
      this._bgmEl = this._createAudio(this.bgmSrc, true); // loop = true
      const bgmSource = this._ctx.createMediaElementSource(this._bgmEl);
      this._bgmGain = this._ctx.createGain();
      this._bgmGain.gain.value = this.bgmVolume;
      bgmSource.connect(this._bgmGain).connect(this._ctx.destination);
    }

    this._initialized = true;
  }

  _createAudio(src, loop = false) {
    const el = new Audio(src);
    el.loop = loop;
    el.preload = 'auto';
    el.crossOrigin = 'anonymous';
    return el;
  }

  /**
   * Bắt đầu phát từ đầu (preview mode)
   */
  async play() {
    if (this.silent || !this._initialized) return;
    try {
      if (this._narrationEl) {
        this._narrationEl.currentTime = this.sceneOffset;
        await this._narrationEl.play();
      }
      if (this._bgmEl) {
        this._bgmEl.currentTime = 0;
        await this._bgmEl.play();
      }
    } catch (e) {
      console.warn('[AudioManager] Play failed:', e.message);
    }
  }

  /**
   * Dừng phát
   */
  pause() {
    if (this.silent || !this._initialized) return;
    if (this._narrationEl) this._narrationEl.pause();
    if (this._bgmEl) this._bgmEl.pause();
  }

  /**
   * Seek đến vị trí trong audio (dùng khi scrub timeline)
   * @param {number} timeSec - Thời gian cục bộ của scene
   */
  seekTo(timeSec) {
    if (this.silent || !this._initialized) return;
    const globalTime = timeSec + this.sceneOffset;
    if (this._narrationEl && isFinite(globalTime)) {
      this._narrationEl.currentTime = Math.max(0, globalTime);
    }
  }

  /**
   * Điều chỉnh volume narration (0.0 → 1.0)
   */
  setNarrationVolume(vol) {
    this.narrationVolume = vol;
    if (this._narGain) this._narGain.gain.value = vol;
  }

  /**
   * Điều chỉnh volume BGM (0.0 → 1.0)
   */
  setBGMVolume(vol) {
    this.bgmVolume = vol;
    if (this._bgmGain) this._bgmGain.gain.value = vol;
  }

  /**
   * Fade in BGM trong fadeDuration giây
   */
  bgmFadeIn(fadeDuration = 1.5) {
    if (!this._bgmGain || !this._ctx) return;
    this._bgmGain.gain.setValueAtTime(0, this._ctx.currentTime);
    this._bgmGain.gain.linearRampToValueAtTime(this.bgmVolume, this._ctx.currentTime + fadeDuration);
    if (this._bgmEl) this._bgmEl.play().catch(() => {});
  }

  /**
   * Fade out BGM trong fadeDuration giây rồi dừng
   */
  bgmFadeOut(fadeDuration = 1.5) {
    if (!this._bgmGain || !this._ctx) return;
    this._bgmGain.gain.setValueAtTime(this.bgmVolume, this._ctx.currentTime);
    this._bgmGain.gain.linearRampToValueAtTime(0, this._ctx.currentTime + fadeDuration);
    setTimeout(() => {
      if (this._bgmEl) this._bgmEl.pause();
    }, fadeDuration * 1000 + 100);
  }

  destroy() {
    this.pause();
    if (this._ctx) this._ctx.close().catch(() => {});
  }
}

// ─────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { AudioManager };
} else {
  window.HFAudio = { AudioManager };
}
