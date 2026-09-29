// node render.js [land|port|clean] [fps] [query]  →  out/ONEFLOW-motion-16x9.mp4 | …-9x16.mp4 | out/ONEFLOW-clean-16x9.mp4
// Frame-accurate: pauses every CSS animation, seeks to each frame time, screenshots, pipes JPEGs into ffmpeg (H.264 + AAC).
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn, execSync } = require('child_process'); const path = require('path'); const fs = require('fs');
const v = process.argv[2] || 'land', fps = +(process.argv[3] || 30), extra = process.argv[4] || '';
const clean = v === 'clean', T = clean ? 38.5 : 28;
const [w, h] = v === 'port' ? [1080, 1920] : [1920, 1080];
const ff = execSync('python3 -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())"').toString().trim();
const outDir = path.join(__dirname, 'out'); fs.mkdirSync(outDir, { recursive: true });
const out = path.join(outDir, clean ? 'ONEFLOW-clean-16x9.mp4' : `ONEFLOW-motion-${v === 'port' ? '9x16' : '16x9'}${extra ? '-' + extra.replace(/\W+/g, '-') : ''}.mp4`);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.goto('file://' + path.join(__dirname, clean ? 'oneflow-clean.html' : 'oneflow-motion.html') + '?cap=1' + (v === 'port' ? '&v=port' : '') + (extra ? '&' + extra : ''));
  await p.evaluate(async () => { await document.fonts.ready; await Promise.all([...document.images].map((i) => i.decode().catch(() => {}))); });
  await p.waitForTimeout(1500);
  const enc = spawn(ff, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-i', path.join(__dirname, clean ? 'music-clean.wav' : 'music.wav'),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.round(T * fps);
  for (let i = 0; i < n; i++) {
    await p.evaluate((t) => window.seek(t), i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 94 });
    if (!enc.stdin.write(buf)) await new Promise((r) => enc.stdin.once('drain', r));
    if (i % 150 === 0) console.log(`${v} frame ${i}/${n}`);
  }
  enc.stdin.end(); await new Promise((r) => enc.on('close', r)); await b.close();
  console.log(out, (fs.statSync(out).size / 1e6).toFixed(1) + ' MB');
})();
