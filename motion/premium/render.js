// node render.js <page.html> <audio.wav> <out.mp4> [width=1280] — frame-accurate capture (seek → screenshot → ffmpeg), length from the page.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn, execSync } = require('child_process'); const path = require('path'); const fs = require('fs');
const [html, wav, out, W = '1280'] = process.argv.slice(2), fps = 30, sf = +W / 1920;
const ff = execSync('python3 -c "import imageio_ffmpeg as f; print(f.get_ffmpeg_exe())"').toString().trim();
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: sf });
  await p.goto('file://' + path.resolve(html) + '?cap=1');
  await p.evaluate(async () => { await document.fonts.ready; });
  await p.waitForTimeout(800);
  const T = await p.evaluate(() => window.DUR), n = Math.round(T * fps);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const enc = spawn(ff, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-', '-i', wav,
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    await p.evaluate((t) => window.seek(t), i / fps);
    const buf = await p.screenshot({ type: 'jpeg', quality: 92 });
    if (!enc.stdin.write(buf)) await new Promise((r) => enc.stdin.once('drain', r));
  }
  enc.stdin.end(); await new Promise((r) => enc.on('close', r)); await b.close();
  console.log(out, (fs.statSync(out).size / 1e6).toFixed(1) + ' MB');
})();
