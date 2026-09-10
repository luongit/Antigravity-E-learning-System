/**
 * HyperFrames Subtitle Engine
 * SRT Lockstep subtitle — 48px Be Vietnam Pro ExtraBold
 * Tuyệt đối KHÔNG viền stroke — dùng drop-shadow
 * z-index: 1000 — luôn trên cùng
 */

'use strict';

class SubtitleEngine {
  /**
   * @param {Array}  srtItems  - [{ startSec, endSec, text }]
   * @param {object} config
   * @param {string} [config.containerId='hf-subtitle']   - ID của container element
   * @param {number} [config.fontSize=48]
   * @param {string} [config.color='#FFFFFF']
   * @param {string} [config.fontFamily="'Be Vietnam Pro', sans-serif"]
   * @param {boolean}[config.showBackground=true]         - Gradient background
   * @param {number} [config.sceneOffset=0]               - Offset giây (dùng khi scene không bắt đầu từ 0 trong audio)
   */
  constructor(srtItems = [], config = {}) {
    this.srtItems = srtItems;
    this.containerId = config.containerId ?? 'hf-subtitle';
    this.fontSize = config.fontSize ?? 48;
    this.color = config.color ?? '#FFFFFF';
    this.fontFamily = config.fontFamily ?? "'Be Vietnam Pro', 'Segoe UI', sans-serif";
    this.showBackground = config.showBackground !== false;
    this.sceneOffset = config.sceneOffset ?? 0;
    this._lastText = null;
    this._container = null;
  }

  /**
   * Khởi tạo DOM container nếu chưa tồn tại
   */
  init() {
    let el = document.getElementById(this.containerId);
    if (!el) {
      el = document.createElement('div');
      el.id = this.containerId;
      document.body.appendChild(el);
    }
    el.style.cssText = `
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: auto;
      min-height: 120px;
      padding: 32px 80px 48px;
      display: flex;
      justify-content: center;
      align-items: flex-end;
      z-index: 1000;
      pointer-events: none;
      box-sizing: border-box;
      ${this.showBackground
        ? 'background: linear-gradient(to top, rgba(5,8,17,0.95) 0%, rgba(5,8,17,0.6) 60%, transparent 100%);'
        : ''}
    `;
    this._container = el;
    this._textEl = document.createElement('div');
    this._textEl.style.cssText = `
      font-family: ${this.fontFamily};
      font-weight: 800;
      font-size: ${this.fontSize}px;
      color: ${this.color};
      text-align: center;
      max-width: 85%;
      line-height: 1.35;
      letter-spacing: -0.5px;
      text-shadow: 0 4px 16px rgba(0,0,0,0.95), 0 2px 6px rgba(0,0,0,0.8);
      opacity: 0;
      transition: opacity 0.12s ease;
    `;
    el.appendChild(this._textEl);
    return this;
  }

  /**
   * Tìm câu phụ đề active tại thời điểm timeSec
   * @param {number} timeSec - Thời gian toàn cục (đã cộng sceneOffset)
   */
  findActive(timeSec) {
    const globalTime = timeSec + this.sceneOffset;
    return this.srtItems.find(item =>
      globalTime >= item.startSec && globalTime <= item.endSec + 0.05
    ) ?? null;
  }

  /**
   * Cập nhật hiển thị tại timeSec
   * @param {number} timeSec - Thời gian cục bộ của scene
   */
  seekTo(timeSec) {
    if (!this._container) this.init();
    const active = this.findActive(timeSec);
    const text = active ? active.text : '';

    if (text !== this._lastText) {
      this._lastText = text;
      if (text) {
        this._textEl.textContent = text;
        this._textEl.style.opacity = '1';
      } else {
        this._textEl.style.opacity = '0';
      }
    }
  }

  /**
   * Có thay đổi subtitle tại timeSec không (dùng để smart-skip Puppeteer)
   */
  hasChange(timeSec) {
    const active = this.findActive(timeSec);
    return (active?.text ?? '') !== this._lastText;
  }

  /**
   * Lấy text hiện tại (không đụng DOM)
   */
  getCurrentText(timeSec) {
    const active = this.findActive(timeSec);
    return active?.text ?? '';
  }
}

// ─────────────────────────────────────────────
// SRT Parser — parse string SRT thành array
// ─────────────────────────────────────────────
function parseSRT(srtString) {
  if (!srtString) return [];
  const pattern = /(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*\n([\s\S]*?)(?=\n\d+\s*\n|\n*$)/g;
  const items = [];
  let match;
  while ((match = pattern.exec(srtString)) !== null) {
    const toSec = (t) => {
      const [h, m, s] = t.replace(',', '.').split(':');
      return parseFloat(h) * 3600 + parseFloat(m) * 60 + parseFloat(s);
    };
    items.push({
      id: parseInt(match[1]),
      startSec: toSec(match[2]),
      endSec: toSec(match[3]),
      text: match[4].replace(/\r?\n/g, ' ').trim(),
    });
  }
  return items;
}

// ─────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SubtitleEngine, parseSRT };
} else {
  window.HFSubtitle = { SubtitleEngine, parseSRT };
}
