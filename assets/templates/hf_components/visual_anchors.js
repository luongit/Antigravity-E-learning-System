/**
 * HyperFrames Visual Anchors
 * 7 preset SVG vector + custom image
 * Floating animation: Math.sin(t)
 */

'use strict';

/**
 * Tạo HTML container cho một Visual Anchor
 * @param {object} config
 * @param {string} [config.type='buni-ecosystem'] - Preset type
 * @param {string} [config.imageSrc]              - Custom image path (custom-image type)
 * @param {string} [config.accentColor='#38BDF8']
 * @param {string} [config.label]                 - Label badge text (tùy chọn)
 * @param {number} [config.size=520]              - Kích thước px
 * @returns {HTMLElement}
 */
function createVisualAnchor(config = {}) {
  const type = config.type ?? 'buni-ecosystem';
  const accentColor = config.accentColor ?? '#38BDF8';
  const label = config.label ?? null;
  const size = config.size ?? 520;

  const wrapper = document.createElement('div');
  wrapper.className = 'hf-visual-anchor';
  wrapper.setAttribute('data-anchor-type', type);
  wrapper.style.cssText = `
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: ${size}px;
    position: relative;
  `;

  const svgWrapper = document.createElement('div');
  svgWrapper.className = 'hf-anchor-svg';
  svgWrapper.style.cssText = `
    filter: drop-shadow(0 20px 35px rgba(0,0,0,0.6));
    width: ${size}px;
    height: ${size}px;
  `;

  if (type === 'custom-image' && config.imageSrc) {
    svgWrapper.innerHTML = `
      <div style="position:relative;width:${size}px;height:${size}px;display:flex;align-items:center;justify-content:center;">
        <div style="position:absolute;inset:20px;border-radius:50%;background:radial-gradient(circle,${accentColor}25 0%,transparent 70%);filter:blur(20px);"></div>
        <img src="${config.imageSrc}" style="max-width:100%;max-height:100%;object-fit:contain;position:relative;z-index:1;" />
      </div>
    `;
  } else {
    svgWrapper.innerHTML = getSVGContent(type, accentColor, size);
  }

  wrapper.appendChild(svgWrapper);

  if (label) {
    const badge = document.createElement('div');
    badge.style.cssText = `
      margin-top: 14px;
      font-family: 'Be Vietnam Pro', sans-serif;
      font-size: 14px; font-weight: 800;
      color: ${accentColor};
      letter-spacing: 1.2px;
      text-transform: uppercase;
      background: rgba(15,23,42,0.85);
      padding: 7px 20px;
      border-radius: 20px;
      border: 1px solid ${accentColor}60;
    `;
    badge.textContent = label;
    wrapper.appendChild(badge);
  }

  return wrapper;
}

// ─── Floating Animation ──────────────────────────────────────────
/**
 * Cập nhật floating transform tại timeSec
 * @param {HTMLElement} anchorEl - Element từ createVisualAnchor()
 * @param {number} timeSec
 */
function updateFloating(anchorEl, timeSec) {
  if (!anchorEl) return;
  const floatY = Math.sin(timeSec * 1.5) * 8;
  const pulse = 1 + Math.sin(timeSec * 2.0) * 0.015;
  const svgWrapper = anchorEl.querySelector('.hf-anchor-svg');
  if (svgWrapper) {
    svgWrapper.style.transform = `translateY(${floatY}px) scale(${pulse})`;
  }
}

// ─── SVG Content Library ──────────────────────────────────────────
function getSVGContent(type, accent, size) {
  const v = size;
  const cx = v / 2, cy = v / 2;

  switch (type) {

    // ── 1. buni-student ─────────────────────────────────────────────
    case 'buni-student':
      return `<svg width="${v}" height="${v}" viewBox="0 0 540 540" fill="none">
        <defs>
          <linearGradient id="orbitG" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="${accent}" stop-opacity="0.8"/>
            <stop offset="50%" stop-color="#818CF8" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="${accent}" stop-opacity="0.1"/>
          </linearGradient>
          <linearGradient id="bodyG" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#1E293B"/>
            <stop offset="100%" stop-color="#0F172A"/>
          </linearGradient>
          <radialGradient id="aura1" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="${accent}" stop-opacity="0.25"/>
            <stop offset="100%" stop-color="transparent"/>
          </radialGradient>
        </defs>
        <circle cx="270" cy="270" r="240" fill="url(#aura1)"/>
        <circle cx="270" cy="270" r="190" stroke="url(#orbitG)" stroke-width="2.5" stroke-dasharray="12 8" opacity="0.6"/>
        <circle cx="270" cy="200" r="60" fill="url(#bodyG)" stroke="${accent}" stroke-width="3"/>
        <circle cx="270" cy="190" r="28" fill="${accent}" opacity="0.9"/>
        <path d="M190 380 C190 300 350 300 350 380 Z" fill="url(#bodyG)" stroke="${accent}" stroke-width="3"/>
        <circle cx="270" cy="120" r="14" fill="#10B981"/>
        <circle cx="410" cy="220" r="12" fill="#F59E0B"/>
        <circle cx="130" cy="280" r="10" fill="#3B82F6"/>
        <circle cx="390" cy="350" r="14" fill="#8B5CF6"/>
        <rect x="70" y="70" width="130" height="42" rx="10" fill="${accent}30" stroke="${accent}" stroke-width="1.5"/>
        <text x="135" y="96" fill="${accent}" font-size="12" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">BẢN QUYỀN BUNI</text>
        <rect x="340" y="420" width="140" height="42" rx="10" fill="#10B98130" stroke="#10B981" stroke-width="1.5"/>
        <text x="410" y="446" fill="#34D399" font-size="12" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">LÀM TRƯỚC HỌC SAU</text>
      </svg>`;

    // ── 2. ai-robotics ──────────────────────────────────────────────
    case 'ai-robotics':
      return `<svg width="${v}" height="${v}" viewBox="0 0 540 540" fill="none">
        <radialGradient id="aiAura" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#10B981" stop-opacity="0.2"/>
          <stop offset="100%" stop-color="transparent"/>
        </radialGradient>
        <circle cx="270" cy="270" r="240" fill="url(#aiAura)"/>
        <polygon points="270,110 400,185 400,335 270,410 140,335 140,185" stroke="#10B981" stroke-width="2.5" fill="#0F172A"/>
        <polygon points="270,150 360,202 360,308 270,360 180,308 180,202" stroke="#34D399" stroke-width="1.5" fill="none" opacity="0.5"/>
        <rect x="215" y="205" width="110" height="110" rx="16" fill="#064E3B" stroke="#10B981" stroke-width="2.5"/>
        <text x="270" y="270" fill="#6EE7B7" font-size="28" font-weight="800" text-anchor="middle" dominant-baseline="middle" font-family="'Be Vietnam Pro',sans-serif">AI</text>
        <line x1="270" y1="150" x2="270" y2="205" stroke="#10B981" stroke-width="3"/>
        <line x1="270" y1="315" x2="270" y2="360" stroke="#10B981" stroke-width="3"/>
        <line x1="180" y1="260" x2="215" y2="260" stroke="#10B981" stroke-width="3"/>
        <line x1="325" y1="260" x2="360" y2="260" stroke="#10B981" stroke-width="3"/>
        <circle cx="270" cy="145" r="8" fill="#10B981" opacity="0.8"/>
        <circle cx="270" cy="365" r="8" fill="#10B981" opacity="0.8"/>
        <circle cx="175" cy="260" r="8" fill="#10B981" opacity="0.8"/>
        <circle cx="365" cy="260" r="8" fill="#10B981" opacity="0.8"/>
      </svg>`;

    // ── 3. tech-orbit ───────────────────────────────────────────────
    case 'tech-orbit':
      return `<svg width="${v}" height="${v}" viewBox="0 0 540 540" fill="none">
        <radialGradient id="orbitAura" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.22"/>
          <stop offset="100%" stop-color="transparent"/>
        </radialGradient>
        <circle cx="270" cy="270" r="240" fill="url(#orbitAura)"/>
        <circle cx="270" cy="270" r="180" stroke="#F59E0B" stroke-width="3" stroke-dasharray="16 10" opacity="0.7"/>
        <circle cx="270" cy="270" r="90" fill="#1E293B" stroke="#F59E0B" stroke-width="2"/>
        <text x="270" y="265" fill="#FCD34D" font-size="16" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">CHU TRÌNH</text>
        <text x="270" y="286" fill="#FCD34D" font-size="16" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">3 BƯỚC</text>
        <circle cx="270" cy="90" r="36" fill="#FF7043" stroke="#fff" stroke-width="2.5"/>
        <text x="270" y="97" fill="#fff" font-size="20" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">01</text>
        <circle cx="426" cy="360" r="36" fill="#3B82F6" stroke="#fff" stroke-width="2.5"/>
        <text x="426" y="367" fill="#fff" font-size="20" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">02</text>
        <circle cx="114" cy="360" r="36" fill="#10B981" stroke="#fff" stroke-width="2.5"/>
        <text x="114" y="367" fill="#fff" font-size="20" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">03</text>
        <path d="M270 126 L414 332" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6 4" opacity="0.5"/>
        <path d="M414 332 L126 332" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6 4" opacity="0.5"/>
        <path d="M126 332 L270 126" stroke="#F59E0B" stroke-width="2" stroke-dasharray="6 4" opacity="0.5"/>
      </svg>`;

    // ── 4. enterprise-network ───────────────────────────────────────
    case 'enterprise-network':
      return `<svg width="${v}" height="${v}" viewBox="0 0 540 540" fill="none">
        <radialGradient id="entAura" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="${accent}" stop-opacity="0.22"/>
          <stop offset="100%" stop-color="transparent"/>
        </radialGradient>
        <circle cx="270" cy="270" r="240" fill="url(#entAura)"/>
        <rect x="180" y="150" width="180" height="260" rx="8" fill="#1E293B" stroke="${accent}" stroke-width="2"/>
        <rect x="110" y="240" width="80" height="170" rx="6" fill="#0F172A" stroke="${accent}" stroke-width="1.5"/>
        <rect x="350" y="220" width="90" height="190" rx="6" fill="#0F172A" stroke="${accent}" stroke-width="1.5"/>
        <rect x="210" y="190" width="30" height="24" rx="3" fill="${accent}" opacity="0.8"/>
        <rect x="260" y="190" width="30" height="24" rx="3" fill="${accent}" opacity="0.8"/>
        <rect x="300" y="190" width="30" height="24" rx="3" fill="${accent}" opacity="0.8"/>
        <rect x="210" y="240" width="30" height="24" rx="3" fill="#F59E0B" opacity="0.8"/>
        <rect x="260" y="240" width="30" height="24" rx="3" fill="#10B981" opacity="0.8"/>
        <rect x="300" y="240" width="30" height="24" rx="3" fill="${accent}" opacity="0.8"/>
        <circle cx="270" cy="350" r="42" fill="#3B82F6" stroke="#fff" stroke-width="2.5"/>
        <text x="270" y="357" fill="#fff" font-size="20" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">BUNI</text>
        <line x1="150" y1="350" x2="228" y2="350" stroke="${accent}" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.6"/>
        <line x1="312" y1="350" x2="395" y2="350" stroke="${accent}" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.6"/>
      </svg>`;

    // ── 5. four-stages ─────────────────────────────────────────────
    case 'four-stages':
      return `<svg width="${v}" height="${v}" viewBox="0 0 440 440" fill="none">
        <defs>
          <linearGradient id="trackG" x1="120" y1="50" x2="120" y2="390" gradientUnits="userSpaceOnUse">
            <stop stop-color="#38BDF8"/>
            <stop offset="0.33" stop-color="#818CF8"/>
            <stop offset="0.66" stop-color="#F59E0B"/>
            <stop offset="1" stop-color="#10B981"/>
          </linearGradient>
        </defs>
        <circle cx="220" cy="220" r="190" fill="#1E293B" fill-opacity="0.4" stroke="#334155" stroke-width="1.5"/>
        <circle cx="220" cy="220" r="150" stroke="${accent}" stroke-width="1" stroke-dasharray="6 6" stroke-opacity="0.3"/>
        <line x1="120" y1="70" x2="120" y2="370" stroke="url(#trackG)" stroke-width="4" stroke-linecap="round"/>
        ${[
          { cy: 90,  color: '#0284C7', border: '#38BDF8', label: 'NỀN TẢNG KỸ THUẬT', num: 'O1' },
          { cy: 180, color: '#4F46E5', border: '#818CF8', label: 'CHUYÊN SÂU PHÂN HỆ', num: 'O2' },
          { cy: 270, color: '#D97706', border: '#F59E0B', label: 'DỰ ÁN DOANH NGHIỆP', num: 'O3' },
          { cy: 360, color: '#059669', border: '#10B981', label: 'THỰC CHIẾN ĐỐI TÁC', num: 'O4' },
        ].map(s => `
          <circle cx="120" cy="${s.cy}" r="22" fill="${s.color}" stroke="${s.border}" stroke-width="3"/>
          <text x="120" y="${s.cy + 5}" fill="#fff" font-size="14" font-weight="900" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">${s.num}</text>
          <rect x="160" y="${s.cy - 16}" width="230" height="32" rx="8" fill="#0F172A" stroke="${s.border}" stroke-width="1.5"/>
          <text x="175" y="${s.cy + 5}" fill="${s.border}" font-size="12" font-weight="800" font-family="'Be Vietnam Pro',sans-serif">${s.label}</text>
        `).join('')}
      </svg>`;

    // ── 6. career-passport ─────────────────────────────────────────
    case 'career-passport':
      return `<svg width="${v}" height="${v}" viewBox="0 0 440 440" fill="none">
        <defs>
          <linearGradient id="cpCard" x1="60" y1="60" x2="380" y2="380" gradientUnits="userSpaceOnUse">
            <stop stop-color="#1E3A8A"/>
            <stop offset="1" stop-color="#0F172A"/>
          </linearGradient>
          <linearGradient id="cpGold" x1="100" y1="100" x2="340" y2="340" gradientUnits="userSpaceOnUse">
            <stop stop-color="#FDE68A"/>
            <stop offset="0.5" stop-color="#F59E0B"/>
            <stop offset="1" stop-color="#B45309"/>
          </linearGradient>
        </defs>
        <rect x="50" y="50" width="340" height="340" rx="28" fill="url(#cpCard)" stroke="url(#cpGold)" stroke-width="2.5"/>
        <rect x="65" y="65" width="310" height="310" rx="20" fill="none" stroke="#38BDF8" stroke-width="1" stroke-opacity="0.2" stroke-dasharray="4 4"/>
        <circle cx="220" cy="130" r="45" fill="#0F172A" stroke="url(#cpGold)" stroke-width="2.5"/>
        <path d="M220 100 L228 122 L252 122 L232 136 L240 158 L220 144 L200 158 L208 136 L188 122 L212 122 Z" fill="#F59E0B"/>
        <text x="220" y="205" fill="#fff" font-size="17" font-weight="900" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif" letter-spacing="1">CAREER PASSPORT</text>
        <text x="220" y="228" fill="#94A3B8" font-size="12" font-weight="700" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">HỘ CHIẾU NGHỀ NGHIỆP SỐ</text>
        <rect x="85" y="250" width="75" height="26" rx="6" fill="#1E293B" stroke="#38BDF8" stroke-width="1"/>
        <text x="122" y="267" fill="#38BDF8" font-size="11" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">PYTHON</text>
        <rect x="170" y="250" width="100" height="26" rx="6" fill="#1E293B" stroke="#10B981" stroke-width="1"/>
        <text x="220" y="267" fill="#10B981" font-size="11" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">AI AGENT</text>
        <rect x="280" y="250" width="75" height="26" rx="6" fill="#1E293B" stroke="#F59E0B" stroke-width="1"/>
        <text x="317" y="267" fill="#F59E0B" font-size="11" font-weight="800" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">DOCKER</text>
        <rect x="85" y="298" width="270" height="40" rx="10" fill="#064E3B" stroke="#10B981" stroke-width="1.5"/>
        <text x="220" y="323" fill="#6EE7B7" font-size="12" font-weight="900" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">100% CAM KẾT VIỆC LÀM</text>
      </svg>`;

    // ── 7. buni-ecosystem (default) ────────────────────────────────
    default:
    case 'buni-ecosystem':

      return `<svg width="${v}" height="${v}" viewBox="0 0 440 440" fill="none">
        <defs>
          <radialGradient id="ecoAura" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#1E3A8A" stop-opacity="0.85"/>
            <stop offset="100%" stop-color="#0F172A" stop-opacity="0.2"/>
          </radialGradient>
          <linearGradient id="ecoShield" x1="140" y1="100" x2="300" y2="320" gradientUnits="userSpaceOnUse">
            <stop stop-color="#1E40AF"/>
            <stop offset="1" stop-color="#0F172A"/>
          </linearGradient>
          <linearGradient id="ecoSeal" x1="160" y1="160" x2="280" y2="280" gradientUnits="userSpaceOnUse">
            <stop stop-color="#FDE68A"/>
            <stop offset="0.5" stop-color="#F59E0B"/>
            <stop offset="1" stop-color="#B45309"/>
          </linearGradient>
        </defs>
        <circle cx="220" cy="220" r="190" fill="url(#ecoAura)" stroke="#1E293B" stroke-width="2"/>
        <circle cx="220" cy="220" r="170" stroke="${accent}" stroke-width="1.5" stroke-dasharray="8 6" stroke-opacity="0.5"/>
        <ellipse cx="220" cy="220" rx="190" ry="75" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="10 6" transform="rotate(-28 220 220)" stroke-opacity="0.5"/>
        <path d="M220 85 L305 130 C305 240 220 290 220 290 C220 290 135 240 135 130 Z" fill="url(#ecoShield)" stroke="${accent}" stroke-width="3"/>
        <polygon points="220,130 265,155 220,175 175,155" fill="${accent}"/>
        <polygon points="190,165 190,195 220,210 250,195 250,165 220,180" fill="#0284C7"/>
        <circle cx="220" cy="235" r="16" fill="#F59E0B" stroke="#fff" stroke-width="2"/>
        <circle cx="85" cy="180" r="30" fill="#0F172A" stroke="#EF4444" stroke-width="2"/>
        <text x="85" y="185" fill="#fff" font-size="11" font-weight="900" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">PTIT</text>
        <circle cx="355" cy="180" r="30" fill="#0F172A" stroke="${accent}" stroke-width="2"/>
        <text x="355" y="185" fill="#fff" font-size="10" font-weight="900" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif">BK-APTECH</text>
        <line x1="115" y1="180" x2="145" y2="180" stroke="#EF4444" stroke-width="2" stroke-dasharray="4 4"/>
        <line x1="295" y1="180" x2="325" y2="180" stroke="${accent}" stroke-width="2" stroke-dasharray="4 4"/>
        <rect x="75" y="325" width="290" height="40" rx="10" fill="url(#ecoSeal)" stroke="#fff" stroke-width="1.5"/>
        <text x="220" y="350" fill="#0F172A" font-size="13" font-weight="900" text-anchor="middle" font-family="'Be Vietnam Pro',sans-serif" letter-spacing="1">BẢN QUYỀN 7190/2021/QTG</text>
      </svg>`;
  }
}

// ─────────────────────────────────────────────
// Manager — tự động tạo và animate tất cả anchors
// ─────────────────────────────────────────────
class VisualAnchorManager {
  constructor() {
    this._anchors = new Map(); // id → { element, config }
  }

  /**
   * Mount visual anchor vào DOM container
   * @param {string} containerId
   * @param {object} config
   * @returns {HTMLElement}
   */
  mount(containerId, config = {}) {
    const container = document.getElementById(containerId);
    if (!container) return null;
    const el = createVisualAnchor(config);
    container.appendChild(el);
    this._anchors.set(containerId, { element: el, config });
    return el;
  }

  /**
   * Cập nhật tất cả floating animations tại timeSec
   */
  updateFloating(timeSec) {
    for (const [, { element }] of this._anchors) {
      updateFloating(element, timeSec);
    }
  }
}

// ─────────────────────────────────────────────
// Export
// ─────────────────────────────────────────────
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { createVisualAnchor, updateFloating, VisualAnchorManager, getSVGContent };
} else {
  window.HFVisualAnchor = { createVisualAnchor, updateFloating, VisualAnchorManager };
}
