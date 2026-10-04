// Shared helpers for the Decap CMS ↔ GitHub OAuth flow (Vercel serverless functions).
// Env vars (Vercel → Project → Settings → Environment Variables):
//   GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET  — from the GitHub OAuth App
//   ALLOWED_ORIGINS (optional)               — extra comma-separated origins allowed to receive the token
import crypto from 'node:crypto';

export const STATE_COOKIE = 'decap_oauth_state';

export function origin(req) {
  const proto = (req.headers['x-forwarded-proto'] || 'https').split(',')[0].trim();
  const host = (req.headers['x-forwarded-host'] || req.headers.host || '').split(',')[0].trim();
  return proto + '://' + host;
}

export function query(req) {
  return new URL(req.url, 'http://localhost').searchParams;
}

export function cookies(req) {
  const out = {};
  String(req.headers.cookie || '').split(';').forEach((c) => {
    const i = c.indexOf('=');
    if (i > 0) out[c.slice(0, i).trim()] = decodeURIComponent(c.slice(i + 1).trim());
  });
  return out;
}

export const randomState = () => crypto.randomBytes(24).toString('hex');

export function allowedOrigins(req) {
  const list = [origin(req)];
  String(process.env.ALLOWED_ORIGINS || '').split(',').map((s) => s.trim()).filter(Boolean).forEach((o) => list.push(o));
  return list;
}

// The popup page. Decap's handshake: popup sends "authorizing:github" to the opener,
// the opener answers, and the popup replies with the result — but only to an allowed origin.
export function popupPage(status, payload, allowed) {
  const msg = 'authorization:github:' + status + ':' + JSON.stringify(payload);
  return `<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>Вход в админку</title></head>
<body style="font-family:system-ui,sans-serif;background:#0F0F0E;color:#ECEBE7;display:grid;place-items:center;min-height:100vh;margin:0">
<p id="t">${status === 'success' ? 'Входим…' : 'Не получилось войти: ' + String(payload.error || '').replace(/[<>&]/g, '')}</p>
<script>
(function () {
  var allowed = ${JSON.stringify(allowed)};
  var msg = ${JSON.stringify(msg)};
  if (!window.opener) { document.getElementById('t').textContent = 'Откройте админку и нажмите «Войти через GitHub».'; return; }
  window.addEventListener('message', function (e) {
    if (allowed.indexOf(e.origin) === -1) return;
    window.opener.postMessage(msg, e.origin);
    ${status === 'success' ? 'setTimeout(function () { window.close(); }, 300);' : ''}
  }, false);
  window.opener.postMessage('authorizing:github', '*');
})();
</script></body></html>`;
}

export function send(res, status, body, headers = {}) {
  res.statusCode = status;
  Object.entries(headers).forEach(([k, v]) => res.setHeader(k, v));
  res.end(body);
}
