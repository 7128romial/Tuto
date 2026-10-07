# Tuto

Annette's Private Lessons: a student and teacher portal for scheduling, requests and payments.

## Run locally

```
pip install -r requirements.txt
python server.py
```

Open http://127.0.0.1:8000 in your browser.

## Teacher login

The teacher login comes from environment variables:

- `TEACHER_USERNAME` (default `annette`)
- `TEACHER_PASSWORD` (required in production)
- `TEACHER_NAME` (default `Annette`)

On Render, set `TEACHER_PASSWORD` under the service's Environment tab.
Annette can then change her password in the app under Settings. That change survives restarts.
If she forgets it, set a new `TEACHER_PASSWORD` value in Render. The new value replaces the password on the next start.
On Render, teacher sign-in stays disabled until `TEACHER_PASSWORD` is set.
When you run the server on your own computer without `TEACHER_PASSWORD`, the password is `annette123`.

## Database

Without `DATABASE_URL`, the server saves data to a local `tutoring.db` file.
Render's free plan erases that file on every deploy and restart, so the live site needs a hosted Postgres database.

1. Create a free Postgres database at https://neon.tech (pick the Frankfurt region, close to the Render server).
2. Copy its connection string. It starts with `postgresql://`.
3. In the Render dashboard, open the service, go to Environment, and add `DATABASE_URL` with that connection string.
4. Save. Render redeploys, and the server creates the tables on first start.

Data in the old `tutoring.db` file is not moved. To keep it, download a backup from the Backup tab before you switch, then restore it after.
