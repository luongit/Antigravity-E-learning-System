/**
 * engines/hyperframes/renderer/renderer.mjs
 * HyperFrames v2 Renderer — Puppeteer + FFmpeg stdin frame-pipe
 *
 * Tính năng chính:
 * - Smart-skip: chỉ chụp frame khi animation đang chạy hoặc subtitle thay đổi
 * - Multi-audio: FFmpeg amix narration + BGM
 * - Progress logging mỗi 30 frames
 */

import puppeteer from 'puppeteer';
import { execFile, spawn } from 'child_process';
import { promisify } from 'util';
import { readFileSync, mkdirSync, existsSync } from 'fs';
import { resolve, join, dirname, isAbsolute } from 'path';
import { parseArgs } from 'util';
import { fileURLToPath, pathToFileURL } from 'url';

const execFileAsync = promisify(execFile);
const __dirname = dirname(fileURLToPath(import.meta.url));
const WORKSPACE_ROOT = resolve(__dirname, '..', '..', '..');

// ─────────────────────────────────────────────
// Parse CLI Args
// ─────────────────────────────────────────────
const { values: args } = parseArgs({
  options: {
    spec:        { type: 'string'  },   // Path to HF Scene Spec JSON
    html:        { type: 'string'  },   // Path to rendered HTML file
    output:      { type: 'string', default: 'output.mp4' },
    slides:      { type: 'boolean', default: false },
    'slides-dir':{ type: 'string'  },
    fps:         { type: 'string', default: '30' },
    width:       { type: 'string', default: '1920' },
    height:      { type: 'string', default: '1080' },
    narration:   { type: 'string'  },   // MP3 narration path
    bgm:         { type: 'string'  },   // BGM path
    'bgm-volume':{ type: 'string', default: '0.12' },
    duration:    { type: 'string'  },   // Override duration (seconds)
    'smart-skip':{ type: 'boolean', default: true },
    debug:       { type: 'boolean', default: false },
  },
  strict: false,
});

const FPS        = parseInt(args.fps || '30');
const WIDTH      = parseInt(args.width || '1920');
const HEIGHT     = parseInt(args.height || '1080');
const BGM_VOL    = parseFloat(args['bgm-volume'] || '0.12');
const SMART_SKIP = args['smart-skip'] !== false;
const DEBUG      = !!args.debug;

// ─────────────────────────────────────────────
// Load spec + audio info
// ─────────────────────────────────────────────
function loadSpec() {
  if (!args.spec) return null;
  try {
    return JSON.parse(readFileSync(args.spec, 'utf-8'));
  } catch (e) {
    console.error('[renderer] Không thể đọc spec:', e.message);
    return null;
  }
}

function resolveAudio(spec, htmlPath) {
  const baseDir = htmlPath ? dirname(resolve(htmlPath)) : process.cwd();
  const globalAudio = spec?.globalAudio || [];
  let narration = args.narration
    || globalAudio.find(a => a.id === 'narration')?.src
    || null;
  let bgm = args.bgm
    || globalAudio.find(a => a.id === 'bgm')?.src
    || null;
  if (narration && !isAbsolute(narration)) narration = resolve(baseDir, narration);
  if (bgm && !isAbsolute(bgm)) bgm = resolve(baseDir, bgm);
  return { narration, bgm };
}

function getDuration(spec) {
  if (args.duration) return parseFloat(args.duration);
  const scene = spec?.scenes?.[0];
  if (scene?.duration) return scene.duration;
  return 30.0;
}

// ─────────────────────────────────────────────
// Get audio duration via ffprobe
// ─────────────────────────────────────────────
async function getAudioDuration(audioPath) {
  if (!audioPath || !existsSync(audioPath)) return null;
  try {
    const { stdout } = await execFileAsync('ffprobe', [
      '-v', 'error', '-show_entries', 'format=duration',
      '-of', 'default=noprint_wrappers=1:nokey=1', audioPath,
    ]);
    return parseFloat(stdout.trim());
  } catch {
    return null;
  }
}

// ─────────────────────────────────────────────
// Render Video — Puppeteer + FFmpeg stdin pipe
// ─────────────────────────────────────────────
async function renderVideo(htmlPath, spec) {
  const { narration, bgm } = resolveAudio(spec, htmlPath);
  let duration = getDuration(spec);

  // Override với audio duration nếu có
  if (narration) {
    const audioDur = await getAudioDuration(narration);
    if (audioDur && audioDur > 0) {
      duration = audioDur + 1.0; // 1s tail
      console.log(`[renderer] Audio duration: ${audioDur.toFixed(2)}s → duration: ${duration.toFixed(2)}s`);
    }
  }

  const totalFrames = Math.ceil(duration * FPS);
  const outputPath = resolve(args.output);

  console.log(`[renderer] Bắt đầu render: ${totalFrames} frames @ ${FPS}fps → ${outputPath}`);

  // ── Build FFmpeg command ─────────────────────────────────────────
  const ffmpegArgs = ['-y'];

  // Video từ stdin (pipe)
  ffmpegArgs.push(
    '-f', 'image2pipe',
    '-vcodec', 'png',
    '-r', String(FPS),
    '-i', 'pipe:0',
  );

  // Audio tracks
  const audioInputs = [];
  if (narration && existsSync(narration)) {
    ffmpegArgs.push('-i', narration);
    audioInputs.push('narration');
  }
  if (bgm && existsSync(bgm)) {
    ffmpegArgs.push('-i', bgm);
    audioInputs.push('bgm');
  }

  // Audio filter — amix nếu có BGM
  if (audioInputs.length === 2) {
    const narIdx = 1, bgmIdx = 2;
    ffmpegArgs.push(
      '-filter_complex',
      `[${narIdx}:a]volume=1.0[vocal];[${bgmIdx}:a]volume=${BGM_VOL}[bgm];[vocal][bgm]amix=inputs=2:duration=first:dropout_transition=2[aout]`,
      '-map', '0:v',
      '-map', '[aout]',
    );
  } else if (audioInputs.length === 1) {
    ffmpegArgs.push('-map', '0:v', '-map', '1:a');
  } else {
    ffmpegArgs.push('-map', '0:v');
  }

  // Video encoding
  ffmpegArgs.push(
    '-vcodec', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'medium',
    '-crf', '18',
    '-movflags', '+faststart',
  );

  if (audioInputs.length > 0) {
    ffmpegArgs.push('-acodec', 'aac', '-b:a', '192k');
  }

  ffmpegArgs.push('-t', String(duration), outputPath);

  // ── Launch FFmpeg ────────────────────────────────────────────────
  const ffmpeg = spawn('ffmpeg', ffmpegArgs, { stdio: ['pipe', 'pipe', 'pipe'] });
  ffmpeg.stderr.on('data', d => {
    if (DEBUG) process.stderr.write(`[ffmpeg] ${d}`);
  });

  // ── Launch Puppeteer ─────────────────────────────────────────────
  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox', '--disable-setuid-sandbox',
      '--disable-dev-shm-usage', '--disable-web-security',
      '--allow-file-access-from-files',
      `--window-size=${WIDTH},${HEIGHT}`,
    ],
    defaultViewport: { width: WIDTH, height: HEIGHT },
  });

  const page = await browser.newPage();
  const fileUrl = pathToFileURL(htmlPath).href;
  await page.goto(fileUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });

  // Chờ HFRenderer khởi tạo
  await page.waitForFunction(() => typeof window.HFRenderer !== 'undefined', {
    timeout: 15000,
  });

  console.log('[renderer] Puppeteer sẵn sàng. Bắt đầu frame-pipe...');

  // ── Frame loop ───────────────────────────────────────────────────
  let lastSubtitleText = '';
  let skippedFrames = 0;
  let renderedFrames = 0;
  let lastRenderedBuf = null;

  for (let frame = 0; frame <= totalFrames; frame++) {
    const timeSec = frame / FPS;

    // Seek đến thời điểm hiện tại
    await page.evaluate((t) => window.HFRenderer.seekTo(t), timeSec);

    // Smart-skip: bỏ qua frame nếu không có gì thay đổi
    let shouldCapture = true;
    if (SMART_SKIP && frame > 0) {
      const [isAnimating, subtitleText] = await page.evaluate((t) => [
        window.HFRenderer.isAnimating(t),
        window.HFRenderer.getSubtitleText(t),
      ], timeSec);

      if (!isAnimating && subtitleText === lastSubtitleText && lastRenderedBuf) {
        // Tái sử dụng frame trước — gửi lại cho FFmpeg
        await new Promise((resolve, reject) => {
          ffmpeg.stdin.write(lastRenderedBuf, err => err ? reject(err) : resolve());
        });
        skippedFrames++;
        shouldCapture = false;
      } else {
        lastSubtitleText = subtitleText;
      }
    }

    if (shouldCapture) {
      const buf = await page.screenshot({ type: 'png' });
      lastRenderedBuf = buf;
      await new Promise((resolve, reject) => {
        ffmpeg.stdin.write(buf, err => err ? reject(err) : resolve());
      });
      renderedFrames++;
    }

    // Progress log mỗi 30 frames
    if (frame % 30 === 0) {
      const pct = ((frame / totalFrames) * 100).toFixed(1);
      process.stdout.write(`\r[renderer] ${pct}% (${frame}/${totalFrames} frames | render:${renderedFrames} skip:${skippedFrames})`);
    }
  }

  process.stdout.write('\n');
  ffmpeg.stdin.end();

  await new Promise((resolve, reject) => {
    ffmpeg.on('close', code => {
      if (code === 0) resolve();
      else reject(new Error(`FFmpeg exited with code ${code}`));
    });
    ffmpeg.on('error', reject);
  });

  await browser.close();
  console.log(`[renderer] ✅ Video xuất thành công: ${outputPath}`);
  console.log(`[renderer] Frames: render=${renderedFrames}, skip=${skippedFrames} (${((skippedFrames/totalFrames)*100).toFixed(1)}% saved)`);
}

// ─────────────────────────────────────────────
// Render Slides — chụp PNG tại thời điểm hoàn thiện
// ─────────────────────────────────────────────
async function renderSlides(htmlPath, spec) {
  const slidesDir = args['slides-dir'] || join(dirname(htmlPath), 'slides');
  mkdirSync(slidesDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: 'new',
    args: [
      '--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage',
      '--disable-web-security', '--allow-file-access-from-files',
      `--window-size=${WIDTH},${HEIGHT}`,
    ],
    defaultViewport: { width: WIDTH, height: HEIGHT },
  });

  const scenes = spec?.scenes || [];
  const outputPaths = [];

  for (let i = 0; i < Math.max(scenes.length, 1); i++) {
    const scene = scenes[i];
    const page = await browser.newPage();
    const fileUrl = pathToFileURL(htmlPath).href;
    await page.goto(fileUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForFunction(() => typeof window.HFRenderer !== 'undefined', { timeout: 15000 });

    // Seek đến thời điểm nội dung hoàn thiện (80% duration)
    const duration = scene?.duration || 40;
    const seekTime = duration * 0.8;
    await page.evaluate((t) => window.HFRenderer.seekTo(t), seekTime);
    await new Promise(r => setTimeout(r, 300));

    let outPath;
    if (args.output && (args.output.endsWith('.png') || args.output.endsWith('.jpg'))) {
      outPath = args.output;
    } else {
      const slideNum = scene?.slideNumber || (i + 1);
      outPath = join(slidesDir, `slide_${slideNum}.png`);
    }
    await page.screenshot({ path: outPath, fullPage: false });
    console.log(`[renderer] Slide ${scene?.slideNumber || (i + 1)}: ${outPath}`);
    outputPaths.push(outPath);
    await page.close();
  }

  await browser.close();
  console.log(`[renderer] ✅ Xuất ${outputPaths.length} slide PNG → ${slidesDir}`);
  return outputPaths;
}

// ─────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────
async function main() {
  if (!args.html) {
    console.error('[renderer] Thiếu --html argument');
    process.exit(1);
  }

  const htmlPath = resolve(args.html);
  if (!existsSync(htmlPath)) {
    console.error(`[renderer] HTML file không tồn tại: ${htmlPath}`);
    process.exit(1);
  }

  const spec = loadSpec();

  try {
    if (args.slides) {
      await renderSlides(htmlPath, spec);
    } else {
      await renderVideo(htmlPath, spec);
    }
  } catch (err) {
    console.error('[renderer] Lỗi render:', err.message);
    process.exit(1);
  }
}

main();
