
import re
import sqlite3
import os
import glob
import time
import uuid
import hashlib
import hmac
import secrets
from datetime import datetime
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
    if digits.startswith("0"):
        digits = "972" + digits[1:]
    return digits

# Teacher login comes from environment variables, never from the page source.
TEACHER_USERNAME = (os.environ.get("TEACHER_USERNAME") or "annette").strip().lower()
TEACHER_NAME = (os.environ.get("TEACHER_NAME") or "Annette").strip()
# Stripped because the sign-in form trims spaces, and pasted values often carry a trailing space or newline.
TEACHER_PASSWORD = (os.environ.get("TEACHER_PASSWORD") or "").strip()
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

def check_login_throttle(identifier):
    now = time.time()
    attempts = [t for t in failed_logins.get(identifier, []) if now - t < FAILED_LOGIN_WINDOW]
    failed_logins[identifier] = attempts
    if len(attempts) >= MAX_FAILED_LOGINS:
        raise HTTPException(status_code=429, detail="Too many failed sign-in attempts. Please wait 15 minutes and try again.")

def record_failed_login(identifier):
    failed_logins.setdefault(identifier, []).append(time.time())

def create_session(cursor, role, user_id, name):
    token = secrets.token_urlsafe(32)
    cursor.execute("DELETE FROM sessions WHERE createdAt < ?", (time.time() - SESSION_DAYS * 86400,))
    cursor.execute("INSERT INTO sessions (token, role, userId, name, createdAt) VALUES (?, ?, ?, ?, ?)",
                   (token_key(token), role, user_id, name, time.time()))
    return token

def get_session(authorization: Optional[str] = Header(None)):
    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    if not token:
        raise HTTPException(status_code=401, detail="Please sign in.")
    conn = get_db()
    row = conn.execute("SELECT * FROM sessions WHERE token = ?", (token_key(token),)).fetchone()
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
    conn = get_db()
    teacher_ready = conn.execute("SELECT 1 FROM teachers LIMIT 1").fetchone() is not None
    conn.close()
    return {
        "status": "ok",
        "app": "Annette's Private Lessons Backend",
        "teacherSignIn": "ready" if teacher_ready else "not set up: add TEACHER_PASSWORD in Render",
        "database": "postgres" if USE_POSTGRES else "local file (erased on every Render deploy)",
    }

@app.post("/api/auth/login")
def login(payload: LoginPayload):
    identifier = (payload.usernameOrId or "").strip()
    throttle_key = identifier.lower()
    check_login_throttle(throttle_key)

    conn = get_db()
    cursor = conn.cursor()

    teacher = cursor.execute("SELECT * FROM teachers WHERE LOWER(email) = ? OR LOWER(name) = ?",
                             (identifier.lower(), identifier.lower())).fetchone()
    if teacher:
        matches, needs_rehash = verify_password(teacher["password"], payload.password)
        if not matches:
            conn.close()
            record_failed_login(throttle_key)
            raise HTTPException(status_code=401, detail="Incorrect password. Please try again.")
        if needs_rehash:
            cursor.execute("UPDATE teachers SET password = ? WHERE id = ?", (hash_password(payload.password), teacher["id"]))
        token = create_session(cursor, "teacher", teacher["id"], teacher["name"])
        conn.commit()
        conn.close()
        failed_logins.pop(throttle_key, None)
        return {"role": "teacher", "teacherId": teacher["id"], "name": teacher["name"], "token": token}

    if identifier.lower() == TEACHER_USERNAME and not cursor.execute("SELECT 1 FROM teachers LIMIT 1").fetchone():
        conn.close()
        raise HTTPException(status_code=503, detail="Teacher sign-in is not set up yet. Add TEACHER_PASSWORD in the Render Environment settings, then redeploy.")

    digits = phone_digits(identifier)
    student = None
    for row in cursor.execute("SELECT * FROM students").fetchall():
        phones = {phone_digits(row["phone"]), phone_digits(row["parentPhone"]), phone_digits(row["studentPhone"]), row["wa"] or ""}
        phones.discard("")
        if row["id"] == identifier or (row["name"] or "").strip().lower() == identifier.lower() or (digits and digits in phones):
            student = row
            break

    if not student:
        conn.close()
        record_failed_login(throttle_key)
        raise HTTPException(status_code=404, detail="No account found. Check the spelling or click 'Create an account'.")
    if not student["password"]:
        conn.close()
        raise HTTPException(status_code=403, detail="This account is not set up yet. Please use the invite link from Teacher Annette to sign up.")
    matches, needs_rehash = verify_password(student["password"], payload.password)
    if not matches:
        conn.close()
        record_failed_login(throttle_key)
        raise HTTPException(status_code=401, detail="Incorrect password. Please try again.")
    if needs_rehash:
        cursor.execute("UPDATE students SET password = ? WHERE id = ?", (hash_password(payload.password), student["id"]))
    token = create_session(cursor, "student", student["id"], student["name"])
    conn.commit()
    conn.close()
    failed_logins.pop(throttle_key, None)
    return {"role": "student", "studentId": student["id"], "name": student["name"], "token": token}

@app.post("/api/auth/logout")
def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.lower().startswith("bearer "):
        conn = get_db()
        conn.execute("DELETE FROM sessions WHERE token = ?", (token_key(authorization[7:].strip()),))
        conn.commit()
        conn.close()
    return {"status": "signed_out"}

@app.post("/api/auth/change-password")
def change_password(payload: ChangePasswordPayload, session: dict = Depends(get_session), authorization: Optional[str] = Header(None)):
    table = "teachers" if session["role"] == "teacher" else "students"
    min_length = 8 if table == "teachers" else 4
    if len(payload.newPassword) < min_length:
        raise HTTPException(status_code=400, detail=f"The new password must be at least {min_length} characters.")

    conn = get_db()
    cursor = conn.cursor()
    row = cursor.execute(f"SELECT password FROM {table} WHERE id = ?", (session["userId"],)).fetchone()
    if not row or not verify_password(row["password"], payload.currentPassword)[0]:
        conn.close()
        raise HTTPException(status_code=400, detail="Your current password is incorrect.")

    cursor.execute(f"UPDATE {table} SET password = ? WHERE id = ?", (hash_password(payload.newPassword), session["userId"]))
    # Sign out every other device that used the old password.
    current_token = token_key(authorization[7:].strip())
    cursor.execute("DELETE FROM sessions WHERE role = ? AND userId = ? AND token != ?", (session["role"], session["userId"], current_token))
    conn.commit()
    conn.close()
    return {"status": "changed"}

@app.get("/api/auth/me")
def me(session: dict = Depends(get_session)):
    if session["role"] == "teacher":
        return {"role": "teacher", "teacherId": session["userId"], "name": session["name"]}
    return {"role": "student", "studentId": session["userId"], "name": session["name"]}

@app.get("/api/invite/{invite_code}")
def get_invite(invite_code: str):
    conn = get_db()
    row = conn.execute("SELECT name, grade, notes, parentName, parentPhone, phone, studentPhone, password FROM students WHERE inviteCode = ? AND inviteCode != ''",
                       (invite_code,)).fetchone()
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
    cursor = conn.cursor()
    parent_phone_value = (payload.parentPhone or payload.phone or "").strip()
    student_phone_value = (payload.studentPhone or "").strip()
    clean_digits = phone_digits(parent_phone_value)
    student_digits = phone_digits(student_phone_value)
    invite_code = (payload.inviteCode or "").strip()

    existing = None
    if invite_code:
        existing = cursor.execute("SELECT * FROM students WHERE inviteCode = ?", (invite_code,)).fetchone()
    if not existing:
        for row in cursor.execute("SELECT * FROM students WHERE LOWER(TRIM(name)) = ?", (payload.name.strip().lower(),)).fetchall():
            phones = {phone_digits(row["phone"]), phone_digits(row["parentPhone"]), phone_digits(row["studentPhone"]), row["wa"] or ""}
            phones.discard("")
            if (clean_digits and clean_digits in phones) or (student_digits and student_digits in phones):
                existing = row
                break

    if existing:
        joined_by_invite = invite_code and existing["inviteCode"] == invite_code
        if existing["password"] and not joined_by_invite:
            conn.close()
            raise HTTPException(status_code=409, detail="An account with this name and phone already exists. Please sign in instead.")
        cursor.execute(
            "UPDATE students SET grade = ?, phone = ?, wa = ?, notes = ?, password = ?, parentName = ?, parentPhone = ?, studentPhone = ? WHERE id = ?",
            (payload.grade or existing["grade"], parent_phone_value or existing["phone"], clean_digits or existing["wa"],
             payload.notes or existing["notes"] or "", hash_password(payload.password),
             payload.parentName or existing["parentName"], parent_phone_value or existing["parentPhone"],
             student_phone_value or existing["studentPhone"], existing["id"])
        )
        token = create_session(cursor, "student", existing["id"], existing["name"])
        conn.commit()
        conn.close()
        return {"role": "student", "studentId": existing["id"], "name": existing["name"], "token": token}

    student_id = new_id("s")
    cursor.execute("""
    INSERT INTO students (id, name, grade, rate, phone, wa, notes, password, inviteCode, parentName, parentPhone, studentPhone)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (student_id, payload.name.strip(), payload.grade, 220.0, parent_phone_value, clean_digits, payload.notes, hash_password(payload.password), invite_code, payload.parentName or "", parent_phone_value, student_phone_value))
    token = create_session(cursor, "student", student_id, payload.name.strip())
    conn.commit()
    conn.close()

    return {"role": "student", "studentId": student_id, "name": payload.name.strip(), "token": token}

@app.get("/api/students")
def list_students(session: dict = Depends(get_session)):
    conn = get_db()
    cursor = conn.cursor()
    only_own = " WHERE id = ?" if session["role"] == "student" else ""
    params = (session["userId"],) if only_own else ()
    cursor.execute("SELECT id, name, grade, rate, phone, wa, notes, inviteCode, parentName, parentPhone, studentPhone, CASE WHEN COALESCE(password, '') != '' THEN 1 ELSE 0 END AS hasAccount FROM students" + only_own + " ORDER BY name ASC", params)
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

@app.post("/api/students")
def save_student(payload: StudentPayload, session: dict = Depends(require_teacher)):
    conn = get_db()
    cursor = conn.cursor()
    parent_phone_value = (payload.parentPhone or payload.phone or "").strip()
    student_id = payload.id or new_id("s")
    existing = cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    values = (payload.name.strip(), payload.grade or "", payload.rate if payload.rate is not None else 220.0,
              parent_phone_value, phone_digits(parent_phone_value), payload.notes or "",
              payload.parentName or "", parent_phone_value, (payload.studentPhone or "").strip())

    if existing:
        cursor.execute(
            "UPDATE students SET name = ?, grade = ?, rate = ?, phone = ?, wa = ?, notes = ?, parentName = ?, parentPhone = ?, studentPhone = ?, inviteCode = ? WHERE id = ?",
            values + (payload.inviteCode or existing["inviteCode"] or "", student_id)
        )
        cursor.execute("UPDATE lessons SET studentName = ? WHERE studentId = ?", (payload.name.strip(), student_id))
        cursor.execute("UPDATE requests SET studentName = ? WHERE studentId = ?", (payload.name.strip(), student_id))
    else:
        cursor.execute(
            "INSERT INTO students (name, grade, rate, phone, wa, notes, parentName, parentPhone, studentPhone, inviteCode, id, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, '')",
            values + (payload.inviteCode or "", student_id)
        )
    conn.commit()
    conn.close()
    return {"id": student_id, "status": "saved"}

@app.delete("/api/students/{student_id}")
def delete_student(student_id: str, session: dict = Depends(require_teacher)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE role = 'student' AND userId = ?", (student_id,))
    cursor.execute("DELETE FROM requests WHERE studentId = ?", (student_id,))
    cursor.execute("DELETE FROM lessons WHERE studentId = ?", (student_id,))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

@app.post("/api/students/{student_id}/reset-password")
def reset_student_password(student_id: str, session: dict = Depends(require_teacher)):
    """Clears the password and issues a new invite link so the student can choose a new one."""
    conn = get_db()
    cursor = conn.cursor()
    if not cursor.execute("SELECT 1 FROM students WHERE id = ?", (student_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Student not found.")
    invite_code = f"inv_{secrets.token_urlsafe(12)}"
    cursor.execute("UPDATE students SET password = '', inviteCode = ? WHERE id = ?", (invite_code, student_id))
    cursor.execute("DELETE FROM sessions WHERE role = 'student' AND userId = ?", (student_id,))
    conn.commit()
    conn.close()
    return {"status": "reset", "inviteCode": invite_code}

@app.get("/api/lessons")
def list_lessons(weekId: Optional[str] = None, studentId: Optional[str] = None, session: dict = Depends(get_session)):
    if session["role"] == "student":
        studentId = session["userId"]
    conn = get_db()
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
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

@app.post("/api/lessons")
def save_lesson(lesson: LessonPayload, session: dict = Depends(require_teacher)):
    try:
        lesson_date = datetime.strptime(lesson.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Lesson date is invalid.")

    if lesson.startTime >= lesson.endTime:
        raise HTTPException(status_code=400, detail="End time must be after start time.")

    conn = get_db()
    cursor = conn.cursor()
    lid = lesson.id or new_id("l")

    # Past dates are allowed only when an existing lesson keeps its date (e.g. marking it paid).
    existing = cursor.execute("SELECT date FROM lessons WHERE id = ?", (lid,)).fetchone()
    date_unchanged = existing is not None and existing["date"] == lesson.date
    if lesson_date < datetime.utcnow().date() and not date_unchanged:
        conn.close()
        raise HTTPException(status_code=400, detail="You cannot schedule a lesson in the past.")
    
    cursor.execute("""
    INSERT OR REPLACE INTO lessons (id, studentId, studentName, weekId, day, date, startTime, endTime, rate, payment, method, status, topic, location)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (lid, lesson.studentId, lesson.studentName, lesson.weekId, lesson.day, lesson.date, lesson.startTime, lesson.endTime, lesson.rate, lesson.payment, lesson.method, lesson.status, lesson.topic, lesson.location))
    
    conn.commit()
    conn.close()
    return {"id": lid, "status": "saved"}

@app.delete("/api/lessons/{lesson_id}")
def delete_lesson(lesson_id: str, session: dict = Depends(require_teacher)):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

@app.get("/api/requests")
def list_requests(studentId: Optional[str] = None, session: dict = Depends(get_session)):
    if session["role"] == "student":
        studentId = session["userId"]
    conn = get_db()
    cursor = conn.cursor()
    if studentId:
        cursor.execute("SELECT * FROM requests WHERE studentId = ? ORDER BY dateSubmitted DESC", (studentId,))
    else:
        cursor.execute("SELECT * FROM requests ORDER BY dateSubmitted DESC")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

@app.post("/api/requests")
def create_request(req: RequestPayload, session: dict = Depends(get_session)):
    conn = get_db()
    cursor = conn.cursor()
    if session["role"] == "student":
        # Students can only send messages as themselves, about their own lessons.
        student = cursor.execute("SELECT id, name FROM students WHERE id = ?", (session["userId"],)).fetchone()
        if not student:
            conn.close()
            raise HTTPException(status_code=401, detail="Please sign in again.")
        if req.lessonId and not cursor.execute("SELECT 1 FROM lessons WHERE id = ? AND studentId = ?", (req.lessonId, student["id"])).fetchone():
            conn.close()
            raise HTTPException(status_code=403, detail="You can only send messages about your own lessons.")
        req.studentId = student["id"]
        req.studentName = student["name"]
    rid = new_id("req")
    now_iso = datetime.utcnow().isoformat() + "Z"
    
    cursor.execute("""
    INSERT INTO requests (id, studentId, studentName, lessonId, lessonSummary, requestType, message, dateSubmitted, status, teacherReply, teacherReplyDate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (rid, req.studentId, req.studentName, req.lessonId, req.lessonSummary, req.requestType, req.message, now_iso, "Pending", "", None))
    conn.commit()
    conn.close()
    return {"id": rid, "status": "submitted"}

@app.post("/api/requests/{request_id}/reply")
def reply_request(request_id: str, payload: ReplyPayload, session: dict = Depends(require_teacher)):
    conn = get_db()
    cursor = conn.cursor()
    now_iso = datetime.utcnow().isoformat() + "Z"

    if payload.updateLesson and payload.lessonId:
        updated_day = payload.newDay or "Monday"
        updated_date = payload.newDate or datetime.utcnow().strftime("%Y-%m-%d")
        try:
            parsed_date = datetime.strptime(updated_date, "%Y-%m-%d").date()
        except ValueError:
            conn.close()
            raise HTTPException(status_code=400, detail="Approved lesson date is invalid.")

        if parsed_date < datetime.utcnow().date():
            conn.close()
            raise HTTPException(status_code=400, detail="You cannot approve a lesson in the past.")

        updated_start = payload.newStartTime or "09:00"
        updated_end = payload.newEndTime or "10:00"
        updated_week = datetime.strptime(updated_date, "%Y-%m-%d").strftime("%Y-W%W")

        cursor.execute("""
        UPDATE lessons
        SET day = ?, date = ?, startTime = ?, endTime = ?, weekId = ?
        WHERE id = ?
        """, (updated_day, updated_date, updated_start, updated_end, updated_week, payload.lessonId))

    cursor.execute("""
    UPDATE requests SET teacherReply = ?, teacherReplyDate = ?, status = ? WHERE id = ?
    """, (payload.reply, now_iso, payload.newStatus, request_id))
    conn.commit()
    conn.close()
    return {"status": "replied"}

@app.post("/api/backup/import")
def import_backup(payload: BackupPayload, session: dict = Depends(require_teacher)):
    conn = get_db()
    cursor = conn.cursor()
    for s in payload.students:
        if not s.get("id") or not s.get("name"):
            continue
        cursor.execute("""
        INSERT INTO students (id, name, grade, rate, phone, wa, notes, password, inviteCode, parentName, parentPhone, studentPhone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET name = excluded.name, grade = excluded.grade, rate = excluded.rate, phone = excluded.phone,
            wa = excluded.wa, notes = excluded.notes, inviteCode = excluded.inviteCode, parentName = excluded.parentName,
            parentPhone = excluded.parentPhone, studentPhone = excluded.studentPhone,
            password = COALESCE(NULLIF(excluded.password, ''), students.password)
        """, (s["id"], s["name"], s.get("grade") or "", s.get("rate") or 220.0, s.get("phone") or "", s.get("wa") or "",
              s.get("notes") or "", ensure_hashed(s.get("password") or ""), s.get("inviteCode") or "", s.get("parentName") or "",
              s.get("parentPhone") or "", s.get("studentPhone") or ""))
    lesson_cols = ["id", "studentId", "studentName", "weekId", "day", "date", "startTime", "endTime", "rate", "payment", "method", "status", "topic", "location"]
    for l in payload.lessons:
        if not all(l.get(k) for k in ["id", "studentId", "date", "startTime", "endTime"]):
            continue
        cursor.execute(f"INSERT OR REPLACE INTO lessons ({', '.join(lesson_cols)}) VALUES ({', '.join('?' * len(lesson_cols))})",
                       [l.get(k) if l.get(k) is not None else "" for k in lesson_cols])
    request_cols = ["id", "studentId", "studentName", "lessonId", "lessonSummary", "requestType", "message", "dateSubmitted", "status", "teacherReply", "teacherReplyDate"]
    for r in payload.requests:
        if not all(r.get(k) for k in ["id", "studentId", "requestType", "dateSubmitted"]):
            continue
        cursor.execute(f"INSERT OR REPLACE INTO requests ({', '.join(request_cols)}) VALUES ({', '.join('?' * len(request_cols))})",
                       [r.get(k) if r.get(k) is not None or k in ("lessonId", "teacherReplyDate") else "" for k in request_cols])
    conn.commit()
    conn.close()
    return {"status": "imported"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print("==================================================")
    print(f" Annette's Private Lessons Server Running on {host}:{port}")
    print("==================================================")
    uvicorn.run("server:app", host=host, port=port)
