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
On Render, teacher sign-in stays disabled until `TEACHER_PASSWORD` is set.
When you run the server on your own computer without `TEACHER_PASSWORD`, the password is `annette123`.
