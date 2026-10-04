// GET /api/callback — step 2: GitHub redirects back with ?code; exchange it for a token
// and hand the token to the admin window via postMessage.
import { STATE_COOKIE, query, cookies, send, popupPage, allowedOrigins } from './_oauth.js';

export default async function handler(req, res) {
  const q = query(req);
  const allowed = allowedOrigins(req);
  const html = (status, payload) => send(res, 200, popupPage(status, payload, allowed), {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-store',
    'Set-Cookie': `${STATE_COOKIE}=; Path=/api; Max-Age=0; HttpOnly; Secure; SameSite=Lax`
  });

  if (q.get('error')) return html('error', { error: q.get('error_description') || q.get('error') });
  const code = q.get('code');
  const state = q.get('state');
  if (!code || !state || state !== cookies(req)[STATE_COOKIE]) {
    return html('error', { error: 'Сессия входа устарела. Закройте окно и нажмите «Войти» ещё раз.' });
  }

  try {
    const r = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({
        client_id: process.env.GITHUB_CLIENT_ID,
        client_secret: process.env.GITHUB_CLIENT_SECRET,
        code
      })
    });
    const data = await r.json();
    if (!data.access_token) return html('error', { error: data.error_description || data.error || 'GitHub не выдал токен' });
    return html('success', { token: data.access_token, provider: 'github' });
  } catch (e) {
    return html('error', { error: 'Нет связи с GitHub: ' + e.message });
  }
}
