# Instagram AI Content Agent (MVP)

Production-oriented MVP that researches trends, generates drafts with AI, routes review via Telegram, and publishes approved posts via Instagram Graph API.

## Features
- Daily scheduled pipeline with APScheduler.
- Configurable hashtags and competitor accounts via `.env`.
- Trend collection storage with `trend_score`.
- OpenAI-based content generation (3 concepts, prompt, caption, hashtags, rationale).
- 4:5 image generation (MVP placeholder image) + Cloudinary/S3 upload.
- Draft review queue with states: `draft`, `approved`, `rejected`, `published`, `failed`.
- Telegram preview with Approve/Reject/Regenerate actions payload.
- Instagram publish flow (`/media` then `/media_publish`).
- Analytics model scaffold.
- Admin API endpoints.

## Quick start
1. Copy env:
   ```bash
   cp .env.example .env
   ```
2. Fill credentials in `.env`.
3. Start stack:
   ```bash
   docker compose up --build
   ```
4. Open API docs: `http://localhost:8000/docs`

## API
- `GET /drafts`
- `GET /drafts/{id}`
- `POST /drafts/{id}/approve`
- `POST /drafts/{id}/reject`
- `POST /drafts/{id}/regenerate`
- `POST /drafts/{id}/publish`

## Notes
- By default this MVP does **not** use unofficial scraping.
- Trend collection currently uses safe placeholders unless official access scopes are configured.
- Database initialization uses `SQLAlchemy Base.metadata.create_all` on startup (MVP mode).
- Add webhook handling endpoint for Telegram callback queries in a next iteration.
