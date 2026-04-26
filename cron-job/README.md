# cron-job — daily knowledge email

GitHub Actions workflow that picks a random concept from `monorepo/` once a day and emails it.

## How selection works

- Notes that have never been sent get top priority (score 1000)
- Otherwise: `score = days_since_last_sent * 10 - review_count * 5`
- Random weighted choice across all notes

Recently-sent notes can still surface — just less often. Notes you've reviewed many times get gradually deprioritized.

## Files

- `.github/workflows/daily-email.yml` — runs at 07:00 IST daily
- `scripts/send_daily.py` — picks a note, renders it as HTML email, sends, updates metadata
- `requirements.txt` — Python deps

## Required GitHub secrets

| Secret | Value |
|--------|-------|
| `SMTP_USER` | your Gmail address |
| `SMTP_PASS` | Gmail app password (NOT your account password) |
| `RECIPIENT` | optional — where to send (defaults to SMTP_USER) |

## Deployment options

**Option A (recommended):** merge this folder's contents into the monorepo repo. Move `.github/workflows/daily-email.yml` to the repo root's `.github/workflows/` and keep `scripts/` and `requirements.txt` under `cron-job/` (or move them to the repo root — adjust the workflow paths accordingly).

**Option B:** keep this as a separate repo. The workflow then needs an extra step to `git clone` the monorepo before running the script. Slightly more setup.
