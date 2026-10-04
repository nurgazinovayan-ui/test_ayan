// GET /api/auth — step 1 of the admin login: redirect to GitHub's consent screen.
import { STATE_COOKIE, origin, randomState, send, popupPage, allowedOrigins } from './_oauth.js';

export default function handler(req, res) {
  const clientId = process.env.GITHUB_CLIENT_ID;
  if (!clientId) {
    send(res, 500, popupPage('error', { error: 'GITHUB_CLIENT_ID не задан в настройках Vercel' }, allowedOrigins(req)),
      { 'Content-Type': 'text/html; charset=utf-8' });
    return;
  }
  const state = randomState();
  const url = new URL('https://github.com/login/oauth/authorize');
  url.searchParams.set('client_id', clientId);
  url.searchParams.set('redirect_uri', origin(req) + '/api/callback');
  url.searchParams.set('scope', 'repo,user');
  url.searchParams.set('state', state);
  send(res, 302, '', {
    Location: url.toString(),
    'Set-Cookie': `${STATE_COOKIE}=${state}; Path=/api; Max-Age=600; HttpOnly; Secure; SameSite=Lax`,
    'Cache-Control': 'no-store'
  });
}
