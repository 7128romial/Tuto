import re
import math
import sqlite3
import os
import glob
import time
import uuid
import hashlib
import hmac
import secrets
import base64
import json
from datetime import datetime, date, timedelta, timezone
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Annette's Private Lessons API", version="3.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

def find_html_path():
    candidates = [
        os.path.join(os.path.dirname(__file__), "index.html"),
        os.path.join(os.path.dirname(__file__), "english_tutoring_portal.html"),
        "index.html",
        "english_tutoring_portal.html",
    ]
    for c in candidates:
        if os.path.isfile(c):
            return c
    # Scan for any HTML file in the repository or subfolders
    matches = glob.glob(os.path.join(os.path.dirname(__file__), "**", "*.html"), recursive=True)
    if matches:
        return matches[0]
    local_matches = glob.glob("**/*.html", recursive=True)
    if local_matches:
        return local_matches[0]
    return None

def new_id(prefix):
    return f"{prefix}_{int(time.time() * 1000)}_{uuid.uuid4().hex[:6]}"

def phone_digits(value):
    digits = "".join(c for c in (value or "") if c.isdigit())
    if digits.startswith("00"):
        digits = digits[2:]
    if digits.startswith("9720"):
        digits = "972" + digits[4:]
    elif digits.startswith("0"):
        digits = "972" + digits[1:]
    return digits

def utc_now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def min_allowed_date():
    # Allow a 14-hour buffer behind UTC so "today" in any local timezone is never rejected as past.
    return (datetime.now(timezone.utc) - timedelta(hours=14)).date()

def time_to_minutes(value: str) -> int:
    if not value or not isinstance(value, str) or ":" not in value:
        raise HTTPException(status_code=400, detail="Lesson time must be in HH:MM format.")
    parts = value.strip().split(":")
    if len(parts) < 2:
        raise HTTPException(status_code=400, detail="Lesson time must be in HH:MM format.")
    try:
        hours = int(parts[0])
        minutes = int(parts[1])
    except ValueError:
        raise HTTPException(status_code=400, detail="Lesson time must be in HH:MM format.")
    if not (0 <= hours <= 23 and 0 <= minutes <= 59):
        raise HTTPException(status_code=400, detail="Lesson time must be a valid time between 00:00 and 23:59.")
    return hours * 60 + minutes

DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

def day_name_from_date(date_str: str) -> str:
    parsed = datetime.strptime(date_str, "%Y-%m-%d").date()
    return DAY_NAMES[(parsed.weekday() + 1) % 7]

def week_id_from_date(date_str: str) -> str:
    parsed = datetime.strptime(date_str, "%Y-%m-%d").date()
    days_since_sunday = (parsed.weekday() + 1) % 7
    sun = parsed - timedelta(days=days_since_sunday)
    one_jan = date(sun.year, 1, 1)
    one_jan_day = (one_jan.weekday() + 1) % 7
    week_num = math.ceil(((sun - one_jan).days + one_jan_day + 1) / 7)
    return f"{sun.year}-W{week_num}"

def find_lesson_conflict(cursor, date_str: str, start_time: str, end_time: str, ignore_id: Optional[str] = None):
    start_mins = time_to_minutes(start_time)
    end_mins = time_to_minutes(end_time)
    rows = cursor.execute(
        "SELECT id, studentName, startTime, endTime, status FROM lessons WHERE date = ?",
        (date_str,)
    ).fetchall()
    for existing in rows:
        if ignore_id and existing["id"] == ignore_id:
            continue
        if (existing["status"] or "") == "Cancelled":
            continue
        try:
            ex_start = time_to_minutes(existing["startTime"])
            ex_end = time_to_minutes(existing["endTime"])
        except HTTPException:
            continue
        if start_mins < ex_end and end_mins > ex_start:
            return dict(existing)
    return None

# Teacher login comes from environment variables, never from the page source.
TEACHER_USERNAME = (os.environ.get("TEACHER_USERNAME") or "annette").strip().lower()
TEACHER_NAME = (os.environ.get("TEACHER_NAME") or "Annette").strip()
TEACHER_PASSWORD = os.environ.get("TEACHER_PASSWORD") or ""
SESSION_DAYS = 30
MAX_FAILED_LOGINS = 5
FAILED_LOGIN_WINDOW = 15 * 60
failed_logins = {}

def hash_password(password):
    salt = secrets.token_bytes(16)
    iterations = 200_000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2${iterations}${salt.hex()}${digest.hex()}"

def verify_password(stored, password):
    """Returns (matches, needs_rehash). Accepts legacy plain-text passwords."""
    if not stored:
        return False, False
    if stored.startswith("pbkdf2$"):
        try:
            _, iterations, salt_hex, digest_hex = stored.split("$")
            digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations))
            return hmac.compare_digest(digest.hex(), digest_hex), False
        except ValueError:
            return False, False
    matches = hmac.compare_digest(stored.encode(), password.encode())
    return matches, matches

def ensure_hashed(password):
    if not password or password.startswith("pbkdf2$"):
        return password or ""
    return hash_password(password)

def token_key(token):
    return hashlib.sha256(token.encode()).hexdigest()

def prune_failed_logins(now=None):
    now = now or time.time()
    expired_keys = []
    for key, timestamps in list(failed_logins.items()):
        valid = [t for t in timestamps if now - t < FAILED_LOGIN_WINDOW]
        if valid:
            failed_logins[key] = valid
        else:
            expired_keys.append(key)
    for key in expired_keys:
        failed_logins.pop(key, None)

def check_login_throttle(identifier):
    now = time.time()
    prune_failed_logins(now)
    attempts = failed_logins.get(identifier, [])
    if len(attempts) >= MAX_FAILED_LOGINS:
        raise HTTPException(status_code=429, detail="Too many failed sign-in attempts. Please wait 15 minutes and try again.")

def record_failed_login(identifier):
    now = time.time()
    prune_failed_logins(now)
    failed_logins.setdefault(identifier, []).append(now)

SESSION_SECRET = hashlib.sha256(f"tuto_session:{TEACHER_USERNAME}:{TEACHER_PASSWORD or 'annette123'}".encode()).digest()
revoked_tokens = set()

def create_session(cursor, role, user_id, name):
    now_ts = time.time()
    payload_obj = {"r": role, "u": user_id, "n": name, "t": int(now_ts), "j": secrets.token_hex(6)}
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload_obj, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(SESSION_SECRET, payload_b64.encode(), hashlib.sha256).hexdigest()
    token = f"{payload_b64}.{sig}"
    cursor.execute("DELETE FROM sessions WHERE createdAt < ?", (now_ts - SESSION_DAYS * 86400,))
    cursor.execute("INSERT INTO sessions (token, role, userId, name, createdAt) VALUES (?, ?, ?, ?, ?)",
                   (token_key(token), role, user_id, name, now_ts))
    return token

def verify_signed_token(token: str):
    if "." not in token or token_key(token) in revoked_tokens:
        return None
    payload_b64, sig = token.rsplit(".", 1)
    expected_sig = hmac.new(SESSION_SECRET, payload_b64.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, expected_sig):
        return None
    try:
        padding = "=" * (-len(payload_b64) % 4)
        data = json.loads(base64.urlsafe_b64decode((payload_b64 + padding).encode()).decode())
        created_at = float(data["t"])
        if created_at < time.time() - SESSION_DAYS * 86400:
            return None
        return {
            "token": token_key(token),
            "role": data["r"],
            "userId": data["u"],
            "name": data.get("n") or "",
            "createdAt": created_at,
        }
    except Exception:
        return None

def get_session(authorization: Optional[str] = Header(None)):
    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Please sign in.")
    conn = get_db()
    try:
        row = conn.execute("SELECT * FROM sessions WHERE token = ?", (token_key(token),)).fetchone()
        if not row:
            recovered = verify_signed_token(token)
            if recovered:
                conn.execute(
                    "INSERT OR REPLACE INTO sessions (token, role, userId, name, createdAt) VALUES (?, ?, ?, ?, ?)",
                    (recovered["token"], recovered["role"], recovered["userId"], recovered["name"], recovered["createdAt"])
                )
                conn.commit()
                return recovered
    finally:
        conn.close()
    if not row or row["createdAt"] < time.time() - SESSION_DAYS * 86400:
        raise HTTPException(status_code=401, detail="Your session has expired. Please sign in again.")
    return dict(row)

def require_teacher(session: dict = Depends(get_session)):
    if session["role"] != "teacher":
        raise HTTPException(status_code=403, detail="Only the teacher can do this.")
    return session

# Set DATABASE_URL to a Postgres connection string to keep data across deploys.
# Without it, the server uses a local SQLite file (fine for running on your own computer).
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
USE_POSTGRES = DATABASE_URL.startswith(("postgres://", "postgresql://"))

# Postgres lowercases unquoted names, so map result columns back to the names the page expects.
CAMEL_COLUMNS = {name.lower(): name for name in [
    "studentId", "studentName", "weekId", "startTime", "endTime", "inviteCode", "parentName", "parentPhone",
    "studentPhone", "lessonId", "lessonSummary", "requestType", "dateSubmitted", "teacherReply",
    "teacherReplyDate", "createdAt", "userId", "hasAccount", "envPasswordMark",
]}

def camel_row_factory(cursor):
    names = [CAMEL_COLUMNS.get(col.name, col.name) for col in (cursor.description or [])]
    return lambda values: dict(zip(names, values))

def to_postgres_sql(sql):
    sql = sql.replace("?", "%s")
    if sql.lstrip().upper().startswith("CREATE TABLE"):
        sql = sql.replace(" REAL", " DOUBLE PRECISION")
    match = re.search(r"INSERT OR REPLACE INTO (\w+) \(([^)]*)\)", sql)
    if match:
        columns = [c.strip() for c in match.group(2).split(",")]
        updates = ", ".join(f"{c} = excluded.{c}" for c in columns if c != "id")
        sql = sql.replace("INSERT OR REPLACE", "INSERT").rstrip().rstrip(";") + f" ON CONFLICT (id) DO UPDATE SET {updates}"
    return sql

class PostgresCursor:
    def __init__(self, conn):
        self._cur = conn.cursor(row_factory=camel_row_factory)

    def execute(self, sql, params=()):
        self._cur.execute(to_postgres_sql(sql), tuple(params))
        return self

    def fetchone(self):
        return self._cur.fetchone()

    def fetchall(self):
        return self._cur.fetchall()

class PostgresConnection:
    """Gives a psycopg connection the small part of the sqlite3 API this server uses."""

    def __init__(self, conn):
        self._conn = conn

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def cursor(self):
        return PostgresCursor(self._conn)

    def execute(self, sql, params=()):
        return self.cursor().execute(sql, params)

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()

def get_db():
    if USE_POSTGRES:
        import psycopg
        return PostgresConnection(psycopg.connect(DATABASE_URL, connect_timeout=10))

    candidates = [
        os.path.join(os.path.dirname(__file__), "tutoring.db"),
        "/tmp/tutoring.db",
        "tutoring.db"
    ]
    for path in candidates:
        try:
            conn = sqlite3.connect(path, timeout=5.0)
            conn.row_factory = sqlite3.Row
            conn.execute("CREATE TABLE IF NOT EXISTS _test_probe (id INT)")
            return conn
        except Exception:
            continue
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT,
            rate REAL DEFAULT 220.0,
            phone TEXT,
            wa TEXT,
            notes TEXT,
            password TEXT NOT NULL,
            inviteCode TEXT,
            parentName TEXT,
            parentPhone TEXT,
            studentPhone TEXT
        )
        """)

        if not USE_POSTGRES:
            # Add columns that older SQLite databases are missing.
            student_columns = [row[1] for row in cursor.execute("PRAGMA table_info(students)").fetchall()]
            for column in ["inviteCode", "parentName", "parentPhone", "studentPhone"]:
                if column not in student_columns:
                    cursor.execute(f"ALTER TABLE students ADD COLUMN {column} TEXT")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS teachers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            createdAt TEXT
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id TEXT PRIMARY KEY,
            studentId TEXT NOT NULL,
            studentName TEXT NOT NULL,
            weekId TEXT NOT NULL,
            day TEXT NOT NULL,
            date TEXT NOT NULL,
            startTime TEXT NOT NULL,
            endTime TEXT NOT NULL,
            rate REAL DEFAULT 220.0,
            payment TEXT DEFAULT 'Unpaid',
            method TEXT DEFAULT 'Bit',
            status TEXT DEFAULT 'Confirmed',
            topic TEXT,
            location TEXT DEFAULT 'Studio (In-Person)',
            FOREIGN KEY (studentId) REFERENCES students (id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id TEXT PRIMARY KEY,
            studentId TEXT NOT NULL,
            studentName TEXT NOT NULL,
            lessonId TEXT,
            lessonSummary TEXT,
            requestType TEXT NOT NULL,
            message TEXT NOT NULL,
            dateSubmitted TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            teacherReply TEXT,
            teacherReplyDate TEXT,
            FOREIGN KEY (studentId) REFERENCES students (id)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            role TEXT NOT NULL,
            userId TEXT NOT NULL,
            name TEXT,
            createdAt REAL NOT NULL
        )
        """)

        # envPasswordMark remembers which TEACHER_PASSWORD was last applied. A password changed
        # in the app survives restarts, while a new TEACHER_PASSWORD value still overrides it
        # (the way to recover a forgotten password).
        if USE_POSTGRES:
            cursor.execute("ALTER TABLE teachers ADD COLUMN IF NOT EXISTS envPasswordMark TEXT")
        elif "envPasswordMark" not in [row[1] for row in cursor.execute("PRAGMA table_info(teachers)").fetchall()]:
            cursor.execute("ALTER TABLE teachers ADD COLUMN envPasswordMark TEXT")

        if TEACHER_PASSWORD:
            teacher = cursor.execute("SELECT envPasswordMark FROM teachers WHERE id = 't_annette'").fetchone()
            env_changed = not teacher or not verify_password(teacher["envPasswordMark"] or "", TEACHER_PASSWORD)[0]
            if env_changed:
                cursor.execute("""
                INSERT INTO teachers (id, name, email, password, envPasswordMark) VALUES ('t_annette', ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET name = excluded.name, email = excluded.email,
                    password = excluded.password, envPasswordMark = excluded.envPasswordMark
                """, (TEACHER_NAME, TEACHER_USERNAME, hash_password(TEACHER_PASSWORD), hash_password(TEACHER_PASSWORD)))
            else:
                cursor.execute("UPDATE teachers SET name = ?, email = ? WHERE id = 't_annette'", (TEACHER_NAME, TEACHER_USERNAME))
        elif os.environ.get("RENDER") and not cursor.execute("SELECT 1 FROM teachers LIMIT 1").fetchone():
            # Never use a known default password on the live site.
            print("ERROR: TEACHER_PASSWORD is not set. Teacher sign-in is disabled until you set it in the Render dashboard.")
        elif not cursor.execute("SELECT 1 FROM teachers LIMIT 1").fetchone():
            print("WARNING: TEACHER_PASSWORD is not set. Using the default teacher password 'annette123'. "
                  "Set TEACHER_PASSWORD in your hosting environment.")
            cursor.execute("INSERT INTO teachers (id, name, email, password) VALUES ('t_annette', ?, ?, ?)",
                           (TEACHER_NAME, TEACHER_USERNAME, hash_password("annette123")))

        conn.commit()
    finally:
        conn.close()

init_db()

class LoginPayload(BaseModel):
    role: Optional[str] = None
    usernameOrId: str
    password: str

class SignUpPayload(BaseModel):
    name: str
    grade: str
    phone: str
    parentName: Optional[str] = ""
    parentPhone: Optional[str] = ""
    studentPhone: Optional[str] = ""
    notes: Optional[str] = ""
    password: str
    inviteCode: Optional[str] = ""

class StudentPayload(BaseModel):
    id: Optional[str] = None
    name: str
    grade: Optional[str] = ""
    rate: Optional[float] = 220.0
    phone: Optional[str] = ""
    parentName: Optional[str] = ""
    parentPhone: Optional[str] = ""
    studentPhone: Optional[str] = ""
    notes: Optional[str] = ""
    inviteCode: Optional[str] = ""

class BackupPayload(BaseModel):
    students: list = []
    lessons: list = []
    requests: list = []

class LessonPayload(BaseModel):
    id: Optional[str] = None
    studentId: str
    studentName: str
    weekId: str
    day: str
    date: str
    startTime: str
    endTime: str
    rate: float
    payment: Optional[str] = "Unpaid"
    method: Optional[str] = "Bit"
    status: Optional[str] = "Confirmed"
    topic: Optional[str] = ""
    location: Optional[str] = "Studio (In-Person)"

class RequestPayload(BaseModel):
    studentId: str
    studentName: str
    lessonId: Optional[str] = None
    lessonSummary: Optional[str] = None
    requestType: str
    message: str

class ChangePasswordPayload(BaseModel):
    currentPassword: str
    newPassword: str

class ReplyPayload(BaseModel):
    reply: str
    newStatus: Optional[str] = "Answered"
    lessonId: Optional[str] = None
    newDay: Optional[str] = None
    newDate: Optional[str] = None
    newStartTime: Optional[str] = None
    newEndTime: Optional[str] = None
    updateLesson: bool = False

@app.get("/")
def serve_frontend():
    path = find_html_path()
    if path:
        return FileResponse(path)
    return HTMLResponse("<h1>Annette's Private Lessons</h1><p>Please ensure index.html or english_tutoring_portal.html is uploaded to your repository.</p>")

@app.get("/index.html")
def serve_index():
    return serve_frontend()

@app.get("/english_tutoring_portal.html")
def serve_portal():
    return serve_frontend()

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Annette's Private Lessons Backend"}

@app.post("/api/auth/login")
def login(payload: LoginPayload):
    identifier = (payload.usernameOrId or "").strip()
    throttle_key = identifier.lower()
    check_login_throttle(throttle_key)

    conn = get_db()
    try:
        cursor = conn.cursor()

        teacher = cursor.execute("SELECT * FROM teachers WHERE LOWER(email) = ? OR LOWER(name) = ?",
                                 (identifier.lower(), identifier.lower())).fetchone()
        if teacher:
            matches, needs_rehash = verify_password(teacher["password"], payload.password)
            if not matches:
                record_failed_login(throttle_key)
                raise HTTPException(status_code=401, detail="Incorrect password. Please try again.")
            if needs_rehash:
                cursor.execute("UPDATE teachers SET password = ? WHERE id = ?", (hash_password(payload.password), teacher["id"]))
            token = create_session(cursor, "teacher", teacher["id"], teacher["name"])
            conn.commit()
            failed_logins.pop(throttle_key, None)
            return {"role": "teacher", "teacherId": teacher["id"], "name": teacher["name"], "token": token}

        digits = phone_digits(identifier)
        candidates = []
        for row in cursor.execute("SELECT * FROM students").fetchall():
            phones = {phone_digits(row["phone"]), phone_digits(row["parentPhone"]), phone_digits(row["studentPhone"]), row["wa"] or ""}
            phones.discard("")
            if row["id"] == identifier or (row["name"] or "").strip().lower() == identifier.lower() or (digits and digits in phones):
                candidates.append(row)

        if not candidates:
            record_failed_login(throttle_key)
            raise HTTPException(status_code=404, detail="No account found. Check the spelling or click 'Create an account'.")

        active_candidates = [c for c in candidates if c["password"]]
        if not active_candidates:
            raise HTTPException(status_code=403, detail="This account is not set up yet. Please use the invite link from Teacher Annette to sign up.")

        matched_student = None
        matched_rehash = False
        for candidate in active_candidates:
            matches, needs_rehash = verify_password(candidate["password"], payload.password)
            if matches:
                matched_student = candidate
                matched_rehash = needs_rehash
                break

        if not matched_student:
            record_failed_login(throttle_key)
            raise HTTPException(status_code=401, detail="Incorrect password. Please try again.")

        if matched_rehash:
            cursor.execute("UPDATE students SET password = ? WHERE id = ?", (hash_password(payload.password), matched_student["id"]))
        token = create_session(cursor, "student", matched_student["id"], matched_student["name"])
        conn.commit()
        failed_logins.pop(throttle_key, None)
        return {"role": "student", "studentId": matched_student["id"], "name": matched_student["name"], "token": token}
    finally:
        conn.close()

@app.post("/api/auth/logout")
def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.lower().startswith("bearer "):
        t_hash = token_key(authorization[7:].strip())
        revoked_tokens.add(t_hash)
        conn = get_db()
        try:
            conn.execute("DELETE FROM sessions WHERE token = ?", (t_hash,))
            conn.commit()
        finally:
            conn.close()
    return {"status": "signed_out"}

@app.post("/api/auth/change-password")
def change_password(payload: ChangePasswordPayload, session: dict = Depends(get_session), authorization: Optional[str] = Header(None)):
    table = "teachers" if session["role"] == "teacher" else "students"
    min_length = 8 if table == "teachers" else 4
    if len(payload.newPassword) < min_length:
        raise HTTPException(status_code=400, detail=f"The new password must be at least {min_length} characters.")

    conn = get_db()
    try:
        cursor = conn.cursor()
        row = cursor.execute(f"SELECT password FROM {table} WHERE id = ?", (session["userId"],)).fetchone()
        if not row or not verify_password(row["password"], payload.currentPassword)[0]:
            raise HTTPException(status_code=400, detail="Your current password is incorrect.")

        cursor.execute(f"UPDATE {table} SET password = ? WHERE id = ?", (hash_password(payload.newPassword), session["userId"]))
        # Sign out every other device that used the old password.
        current_token = session.get("token") or (token_key(authorization[7:].strip()) if authorization else "")
        cursor.execute("DELETE FROM sessions WHERE role = ? AND userId = ? AND token != ?", (session["role"], session["userId"], current_token))
        conn.commit()
        return {"status": "changed"}
    finally:
        conn.close()

@app.get("/api/auth/me")
def me(session: dict = Depends(get_session)):
    if session["role"] == "teacher":
        return {"role": "teacher", "teacherId": session["userId"], "name": session["name"]}
    return {"role": "student", "studentId": session["userId"], "name": session["name"]}

@app.get("/api/invite/{invite_code}")
def get_invite(invite_code: str):
    conn = get_db()
    try:
        row = conn.execute("SELECT name, grade, notes, parentName, parentPhone, phone, studentPhone, password FROM students WHERE inviteCode = ? AND inviteCode != ''",
                           (invite_code,)).fetchone()
    finally:
        conn.close()
    if not row or row["password"]:
        raise HTTPException(status_code=404, detail="This invite link is not valid or was already used.")
    return {"name": row["name"], "grade": row["grade"] or "", "notes": row["notes"] or "", "parentName": row["parentName"] or "",
            "parentPhone": row["parentPhone"] or row["phone"] or "", "studentPhone": row["studentPhone"] or ""}

@app.post("/api/auth/signup")
def signup(payload: SignUpPayload):
    if len(payload.password or "") < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters.")

    conn = get_db()
    try:
        cursor = conn.cursor()
        clean_name = (payload.name or "").strip()
        if not clean_name:
            raise HTTPException(status_code=400, detail="Please enter the student name.")
        parent_phone_value = (payload.parentPhone or payload.phone or "").strip()
        student_phone_value = (payload.studentPhone or "").strip()
        clean_digits = phone_digits(parent_phone_value)
        student_digits = phone_digits(student_phone_value)
        invite_code = (payload.inviteCode or "").strip()

        existing = None
        if invite_code:
            existing = cursor.execute("SELECT * FROM students WHERE inviteCode = ? AND inviteCode != ''", (invite_code,)).fetchone()
            if existing and existing["password"]:
                raise HTTPException(status_code=409, detail="This invite link was already used. Please sign in instead.")
        if not existing:
            for row in cursor.execute("SELECT * FROM students WHERE LOWER(TRIM(name)) = ?", (clean_name.lower(),)).fetchall():
                phones = {phone_digits(row["phone"]), phone_digits(row["parentPhone"]), phone_digits(row["studentPhone"]), row["wa"] or ""}
                phones.discard("")
                if (clean_digits and clean_digits in phones) or (student_digits and student_digits in phones):
                    existing = row
                    break

        if existing:
            if existing["password"]:
                raise HTTPException(status_code=409, detail="An account with this name and phone already exists. Please sign in instead.")
            updated_name = clean_name or existing["name"]
            cursor.execute(
                "UPDATE students SET name = ?, grade = ?, phone = ?, wa = ?, notes = ?, password = ?, inviteCode = '', parentName = ?, parentPhone = ?, studentPhone = ? WHERE id = ?",
                (updated_name, payload.grade or existing["grade"], parent_phone_value or existing["phone"], clean_digits or existing["wa"],
                 payload.notes or existing["notes"] or "", hash_password(payload.password),
                 payload.parentName or existing["parentName"], parent_phone_value or existing["parentPhone"],
                 student_phone_value or existing["studentPhone"], existing["id"])
            )
            if updated_name != existing["name"]:
                cursor.execute("UPDATE lessons SET studentName = ? WHERE studentId = ?", (updated_name, existing["id"]))
                cursor.execute("UPDATE requests SET studentName = ? WHERE studentId = ?", (updated_name, existing["id"]))
            token = create_session(cursor, "student", existing["id"], updated_name)
            conn.commit()
            return {"role": "student", "studentId": existing["id"], "name": updated_name, "token": token}

        student_id = new_id("s")
        cursor.execute("""
        INSERT INTO students (id, name, grade, rate, phone, wa, notes, password, inviteCode, parentName, parentPhone, studentPhone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, '', ?, ?, ?)
        """, (student_id, clean_name, payload.grade, 220.0, parent_phone_value, clean_digits, payload.notes, hash_password(payload.password), payload.parentName or "", parent_phone_value, student_phone_value))
        token = create_session(cursor, "student", student_id, clean_name)
        conn.commit()

        return {"role": "student", "studentId": student_id, "name": clean_name, "token": token}
    finally:
        conn.close()

@app.get("/api/students")
def list_students(session: dict = Depends(get_session)):
    conn = get_db()
    try:
        cursor = conn.cursor()
        only_own = " WHERE id = ?" if session["role"] == "student" else ""
        params = (session["userId"],) if only_own else ()
        cursor.execute("SELECT id, name, grade, rate, phone, wa, notes, inviteCode, parentName, parentPhone, studentPhone, CASE WHEN COALESCE(password, '') != '' THEN 1 ELSE 0 END AS hasAccount FROM students" + only_own + " ORDER BY name ASC", params)
        items = [dict(row) for row in cursor.fetchall()]
        updated_any = False
        for item in items:
            if not item.get("hasAccount") and not item.get("inviteCode"):
                code = f"inv_{secrets.token_urlsafe(12)}"
                item["inviteCode"] = code
                cursor.execute("UPDATE students SET inviteCode = ? WHERE id = ?", (code, item["id"]))
                updated_any = True
        if updated_any:
            conn.commit()
        return items
    finally:
        conn.close()

@app.post("/api/students")
def save_student(payload: StudentPayload, session: dict = Depends(require_teacher)):
    conn = get_db()
    try:
        cursor = conn.cursor()
        parent_phone_value = (payload.parentPhone or payload.phone or "").strip()
        student_id = payload.id or new_id("s")
        existing = cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        values = (payload.name.strip(), payload.grade or "", payload.rate if payload.rate is not None else 220.0,
                  parent_phone_value, phone_digits(parent_phone_value), payload.notes or "",
                  payload.parentName or "", parent_phone_value, (payload.studentPhone or "").strip())

        if existing:
            invite_code = payload.inviteCode or existing["inviteCode"] or ("" if existing["password"] else f"inv_{secrets.token_urlsafe(12)}")
            cursor.execute(
                "UPDATE students SET name = ?, grade = ?, rate = ?, phone = ?, wa = ?, notes = ?, parentName = ?, parentPhone = ?, studentPhone = ?, inviteCode = ? WHERE id = ?",
                values + (invite_code, student_id)
            )
            cursor.execute("UPDATE lessons SET studentName = ? WHERE studentId = ?", (payload.name.strip(), student_id))
            cursor.execute("UPDATE requests SET studentName = ? WHERE studentId = ?", (payload.name.strip(), student_id))
        else:
            invite_code = payload.inviteCode or f"inv_{secrets.token_urlsafe(12)}"
            cursor.execute(
                "INSERT INTO students (name, grade, rate, phone, wa, notes, parentName, parentPhone, studentPhone, inviteCode, id, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '')",
                values + (invite_code, student_id)
            )
        conn.commit()
        return {"id": student_id, "inviteCode": invite_code, "status": "saved"}
    finally:
        conn.close()

@app.delete("/api/students/{student_id}")
def delete_student(student_id: str, session: dict = Depends(require_teacher)):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE role = 'student' AND userId = ?", (student_id,))
        cursor.execute("DELETE FROM requests WHERE studentId = ?", (student_id,))
        cursor.execute("DELETE FROM lessons WHERE studentId = ?", (student_id,))
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        return {"status": "deleted"}
    finally:
        conn.close()

@app.post("/api/students/{student_id}/reset-password")
def reset_student_password(student_id: str, session: dict = Depends(require_teacher)):
    """Clears the password and issues a new invite link so the student can choose a new one."""
    conn = get_db()
    try:
        cursor = conn.cursor()
        if not cursor.execute("SELECT 1 FROM students WHERE id = ?", (student_id,)).fetchone():
            raise HTTPException(status_code=404, detail="Student not found.")
        invite_code = f"inv_{secrets.token_urlsafe(12)}"
        cursor.execute("UPDATE students SET password = '', inviteCode = ? WHERE id = ?", (invite_code, student_id))
        cursor.execute("DELETE FROM sessions WHERE role = 'student' AND userId = ?", (student_id,))
        conn.commit()
        return {"status": "reset", "inviteCode": invite_code}
    finally:
        conn.close()

@app.get("/api/lessons")
def list_lessons(weekId: Optional[str] = None, studentId: Optional[str] = None, session: dict = Depends(get_session)):
    if session["role"] == "student":
        studentId = session["userId"]
    conn = get_db()
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM lessons WHERE 1=1"
        params = []
        if weekId:
            query += " AND weekId = ?"
            params.append(weekId)
        if studentId:
            query += " AND studentId = ?"
            params.append(studentId)
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

@app.post("/api/lessons")
def save_lesson(lesson: LessonPayload, session: dict = Depends(require_teacher)):
    try:
        lesson_date = datetime.strptime(lesson.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Lesson date is invalid.")

    if time_to_minutes(lesson.startTime) >= time_to_minutes(lesson.endTime):
        raise HTTPException(status_code=400, detail="End time must be after start time.")

    conn = get_db()
    try:
        cursor = conn.cursor()
        lid = lesson.id or new_id("l")

        # Past dates are allowed only when an existing lesson keeps its date (e.g. marking it paid).
        existing = cursor.execute("SELECT date FROM lessons WHERE id = ?", (lid,)).fetchone()
        date_unchanged = existing is not None and existing["date"] == lesson.date
        if lesson_date < min_allowed_date() and not date_unchanged:
            raise HTTPException(status_code=400, detail="You cannot schedule a lesson in the past.")

        if (lesson.status or "Confirmed") != "Cancelled":
            conflict = find_lesson_conflict(cursor, lesson.date, lesson.startTime, lesson.endTime, ignore_id=lid)
            if conflict:
                raise HTTPException(
                    status_code=409,
                    detail=f"Time conflict: {conflict['studentName']} already has a lesson on {lesson.date} at {conflict['startTime']}–{conflict['endTime']}."
                )

        computed_week_id = week_id_from_date(lesson.date)
        computed_day = day_name_from_date(lesson.date)

        cursor.execute("""
        INSERT OR REPLACE INTO lessons (id, studentId, studentName, weekId, day, date, startTime, endTime, rate, payment, method, status, topic, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (lid, lesson.studentId, lesson.studentName, computed_week_id, computed_day, lesson.date, lesson.startTime, lesson.endTime, lesson.rate, lesson.payment, lesson.method, lesson.status, lesson.topic, lesson.location))
        
        conn.commit()
        return {"id": lid, "status": "saved"}
    finally:
        conn.close()

@app.delete("/api/lessons/{lesson_id}")
def delete_lesson(lesson_id: str, session: dict = Depends(require_teacher)):
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
        conn.commit()
        return {"status": "deleted"}
    finally:
        conn.close()

@app.get("/api/requests")
def list_requests(studentId: Optional[str] = None, session: dict = Depends(get_session)):
    if session["role"] == "student":
        studentId = session["userId"]
    conn = get_db()
    try:
        cursor = conn.cursor()
        if studentId:
            cursor.execute("SELECT * FROM requests WHERE studentId = ? ORDER BY dateSubmitted DESC", (studentId,))
        else:
            cursor.execute("SELECT * FROM requests ORDER BY dateSubmitted DESC")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

@app.post("/api/requests")
def create_request(req: RequestPayload, session: dict = Depends(get_session)):
    conn = get_db()
    try:
        cursor = conn.cursor()
        if session["role"] == "student":
            # Students can only send messages as themselves, about their own lessons.
            student = cursor.execute("SELECT id, name FROM students WHERE id = ?", (session["userId"],)).fetchone()
            if not student:
                raise HTTPException(status_code=401, detail="Please sign in again.")
            if req.lessonId and not cursor.execute("SELECT 1 FROM lessons WHERE id = ? AND studentId = ?", (req.lessonId, student["id"])).fetchone():
                raise HTTPException(status_code=403, detail="You can only send messages about your own lessons.")
            req.studentId = student["id"]
            req.studentName = student["name"]
        rid = new_id("req")
        now_iso = utc_now_iso()
        
        cursor.execute("""
        INSERT INTO requests (id, studentId, studentName, lessonId, lessonSummary, requestType, message, dateSubmitted, status, teacherReply, teacherReplyDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (rid, req.studentId, req.studentName, req.lessonId, req.lessonSummary, req.requestType, req.message, now_iso, "Pending", "", None))
        conn.commit()
        return {"id": rid, "status": "submitted"}
    finally:
        conn.close()

@app.post("/api/requests/{request_id}/reply")
def reply_request(request_id: str, payload: ReplyPayload, session: dict = Depends(require_teacher)):
    conn = get_db()
    try:
        cursor = conn.cursor()
        now_iso = utc_now_iso()

        if payload.updateLesson and payload.lessonId:
            updated_date = payload.newDate or datetime.now(timezone.utc).strftime("%Y-%m-%d")
            try:
                parsed_date = datetime.strptime(updated_date, "%Y-%m-%d").date()
            except ValueError:
                raise HTTPException(status_code=400, detail="Approved lesson date is invalid.")

            if parsed_date < min_allowed_date():
                raise HTTPException(status_code=400, detail="You cannot approve a lesson in the past.")

            updated_start = payload.newStartTime or "09:00"
            updated_end = payload.newEndTime or "10:00"
            if time_to_minutes(updated_start) >= time_to_minutes(updated_end):
                raise HTTPException(status_code=400, detail="End time must be after start time.")

            conflict = find_lesson_conflict(cursor, updated_date, updated_start, updated_end, ignore_id=payload.lessonId)
            if conflict:
                raise HTTPException(
                    status_code=409,
                    detail=f"Time conflict: {conflict['studentName']} already has a lesson on {updated_date} at {conflict['startTime']}–{conflict['endTime']}."
                )

            updated_day = day_name_from_date(updated_date)
            updated_week = week_id_from_date(updated_date)

            cursor.execute("""
            UPDATE lessons
            SET day = ?, date = ?, startTime = ?, endTime = ?, weekId = ?, status = 'Confirmed'
            WHERE id = ?
            """, (updated_day, updated_date, updated_start, updated_end, updated_week, payload.lessonId))

        cursor.execute("""
        UPDATE requests SET teacherReply = ?, teacherReplyDate = ?, status = ? WHERE id = ?
        """, (payload.reply, now_iso, payload.newStatus, request_id))
        conn.commit()
        return {"status": "replied"}
    finally:
        conn.close()

@app.post("/api/backup/import")
def import_backup(payload: BackupPayload, session: dict = Depends(require_teacher)):
    conn = get_db()
    try:
        cursor = conn.cursor()
        for s in payload.students:
            if not s.get("id") or not s.get("name"):
                continue
            try:
                s_rate = float(s["rate"]) if s.get("rate") not in (None, "") else 220.0
            except (TypeError, ValueError):
                s_rate = 220.0
            cursor.execute("""
            INSERT INTO students (id, name, grade, rate, phone, wa, notes, password, inviteCode, parentName, parentPhone, studentPhone)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET name = excluded.name, grade = excluded.grade, rate = excluded.rate, phone = excluded.phone,
                wa = excluded.wa, notes = excluded.notes, inviteCode = excluded.inviteCode, parentName = excluded.parentName,
                parentPhone = excluded.parentPhone, studentPhone = excluded.studentPhone,
                password = COALESCE(NULLIF(excluded.password, ''), students.password)
            """, (s["id"], s["name"], s.get("grade") or "", s_rate, s.get("phone") or "", s.get("wa") or "",
                  s.get("notes") or "", ensure_hashed(s.get("password") or ""), s.get("inviteCode") or "", s.get("parentName") or "",
                  s.get("parentPhone") or "", s.get("studentPhone") or ""))

        known_students = {row["id"] for row in cursor.execute("SELECT id FROM students").fetchall()}

        lesson_cols = ["id", "studentId", "studentName", "weekId", "day", "date", "startTime", "endTime", "rate", "payment", "method", "status", "topic", "location"]
        for l in payload.lessons:
            if not all(l.get(k) for k in ["id", "studentId", "date", "startTime", "endTime"]):
                continue
            if l["studentId"] not in known_students:
                continue
            try:
                l_rate = float(l["rate"]) if l.get("rate") not in (None, "") else 220.0
            except (TypeError, ValueError):
                l_rate = 220.0
            try:
                l_week = l.get("weekId") or week_id_from_date(l["date"])
                l_day = l.get("day") or day_name_from_date(l["date"])
            except ValueError:
                continue
            values = [
                l["id"],
                l["studentId"],
                l.get("studentName") or "Student",
                l_week,
                l_day,
                l["date"],
                l["startTime"],
                l["endTime"],
                l_rate,
                l.get("payment") or "Unpaid",
                l.get("method") or "Bit",
                l.get("status") or "Confirmed",
                l.get("topic") or "",
                l.get("location") or "Studio (In-Person)",
            ]
            cursor.execute(f"INSERT OR REPLACE INTO lessons ({', '.join(lesson_cols)}) VALUES ({', '.join('?' * len(lesson_cols))})", values)

        request_cols = ["id", "studentId", "studentName", "lessonId", "lessonSummary", "requestType", "message", "dateSubmitted", "status", "teacherReply", "teacherReplyDate"]
        for r in payload.requests:
            if not all(r.get(k) for k in ["id", "studentId", "requestType", "dateSubmitted"]):
                continue
            if r["studentId"] not in known_students:
                continue
            values = [
                r["id"],
                r["studentId"],
                r.get("studentName") or "Student",
                r.get("lessonId") or None,
                r.get("lessonSummary") or "",
                r["requestType"],
                r.get("message") or "",
                r["dateSubmitted"],
                r.get("status") or "Pending",
                r.get("teacherReply") or "",
                r.get("teacherReplyDate") or None,
            ]
            cursor.execute(f"INSERT OR REPLACE INTO requests ({', '.join(request_cols)}) VALUES ({', '.join('?' * len(request_cols))})", values)
        conn.commit()
        return {"status": "imported"}
    finally:
        conn.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print("==================================================")
    print(f" Annette's Private Lessons Server Running on {host}:{port}")
    print("==================================================")
    uvicorn.run("server:app", host=host, port=port)
