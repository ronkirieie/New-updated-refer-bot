# Refer Bot Next

Refer Bot Next is the upgraded, Telegram-only version of the referral and reward
bot. It is intentionally separate from the legacy bot: the legacy repository is
kept in `../legacy-reference` for audit and comparison, and this bot must use a
separate PostgreSQL database.

There is no website, React app, or browser admin dashboard. Users and
administrators work entirely inside Telegram through messages, inline buttons,
media uploads, confirmations, message editing, and Mini App device verification.

## What is improved

- More useful user menu: referrals, stock rewards, reward history, progress,
  profile, how-it-works guide, and support.
- Referral sharing button with live stats, pending count, next milestone, and
  refresh action.
- Expiring admin input sessions so an old message cannot accidentally trigger a
  later operation.
- Owner-controlled admin permissions for dashboard, users, rewards, referrals,
  force-subscribe, content, broadcasts, settings, and security.
- Audit logging for sensitive administrator changes.
- Transactional reward and stock claims with row locks and `SKIP LOCKED`.
- Persistent, confirmation-first broadcasts to all registered non-banned users,
  with per-user delivery tracking, retry handling, rate limiting, progress, and
  exact sent/not-sent totals.
- Telegram Mini App verification with signed init data, device/install and
  fingerprint correlation, IP/network reputation signals, rate limits, risk
  scoring, referral-cycle detection, and security alerts.
- In-place spinner and progress animations without fake delays.

## Architecture

- Python 3.12+
- `aiogram` 3 for Telegram updates and keyboards
- PostgreSQL with `asyncpg`
- `aiohttp` for the secure Telegram Mini App endpoint
- One long-polling worker process

The root `db.py` is the only active database layer. The duplicate legacy
`telegram-bot/db.py` module was intentionally not carried into the upgrade.

## Run locally

Use a fresh database for this upgraded bot. Do not point it at the database used
by the old production bot until a deliberate migration plan has been reviewed.

```bash
cd telegram-bot-next
cp .env.example .env
python -m pip install -r requirements.txt
python bot.py
```

Required values:

- `TELEGRAM_BOT_TOKEN`
- `DATABASE_URL`
- `OWNER_TELEGRAM_ID=713914937`

The owner ID enables the Telegram-native admin panel and full owner access.

For device verification, configure `PUBLIC_BASE_URL` or `MINIAPP_URL`. The bot
can run without a Mini App URL, but users will not pass the device-verification
gate until it is configured.

The bot must be an administrator in every mandatory force-subscribe channel so
Telegram can verify membership.

## Railway

Use `python bot.py` as the start command and keep exactly one polling replica.
Set the required environment variables from `.env.example`. Railway supplies
`PORT` automatically for the Mini App health server.

## Safety rules

- The legacy reference is never modified by this project.
- Use a separate `DATABASE_URL` for Refer Bot Next.
- Telegram IDs are stored as PostgreSQL `BIGINT`.
- Referral attribution is one-time and only completes after subscription,
  disclaimer, device verification, and security checks.
- Claims are reserved before delivery; failed delivery stays visible for admin
  retry instead of silently returning to inventory.
- Never commit `.env`, bot tokens, database URLs, or verification secrets.