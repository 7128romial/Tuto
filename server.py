
import sqlite3
import json
import os
import glob
import time
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Annette's Private Lessons API", version="3.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
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

def get_db():
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
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        createdAt TEXT DEFAULT CURRENT_TIMESTAMP
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
    
    conn.commit()
    conn.close()

init_db()

class LoginPayload(BaseModel):
    role: str
    usernameOrId: str
    password: str

class SignUpPayload(BaseModel):
    name: str
    grade: str
    phone: str
    notes: Optional[str] = ""
    password: str

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
    conn = get_db()
    cursor = conn.cursor()
    
    if payload.role == "teacher":
        identifier = (payload.usernameOrId or "").strip()
        normalized = identifier.lower()
        cursor.execute("SELECT * FROM teachers WHERE email = ? OR name = ?", (normalized, identifier))
        teacher = cursor.fetchone()
        if teacher:
            if teacher["password"] and teacher["password"] != payload.password:
                conn.close()
                raise HTTPException(status_code=401, detail="Incorrect teacher password.")
            conn.close()
            return {"role": "teacher", "teacherId": teacher["id"], "name": teacher["name"]}

        if normalized in ["annette", "annette@lessons.com", "annette@lessons"] and payload.password in ["annette123", "annette", "admin"]:
            conn.close()
            return {"role": "teacher", "teacherId": "t_annette", "name": "Annette"}

        conn.close()
        raise HTTPException(status_code=401, detail="Invalid teacher password or account not found.")
    else:
        cursor.execute("SELECT * FROM students WHERE id = ? OR name = ? OR phone = ?", 
                       (payload.usernameOrId, payload.usernameOrId, payload.usernameOrId))
        student = cursor.fetchone()
        conn.close()
        if not student:
            raise HTTPException(status_code=404, detail="Student account not found. Please click 'Student Sign Up' to register.")
        if student["password"] and student["password"] != payload.password:
            raise HTTPException(status_code=401, detail="Incorrect password. Please verify your password.")
        return {"role": "student", "studentId": student["id"], "name": student["name"]}

@app.post("/api/auth/signup")
def signup(payload: SignUpPayload):
    conn = get_db()
    cursor = conn.cursor()
    clean_digits = "".join([c for c in payload.phone if c.isdigit()])
    if clean_digits.startswith("0"):
        clean_digits = "972" + clean_digits[1:]

    existing = cursor.execute(
        "SELECT * FROM students WHERE LOWER(name) = ? AND (phone = ? OR wa = ?)",
        (payload.name.strip().lower(), payload.phone.strip(), clean_digits)
    ).fetchone()

    if existing:
        cursor.execute(
            "UPDATE students SET grade = ?, phone = ?, wa = ?, notes = ?, password = ? WHERE id = ?",
            (payload.grade, payload.phone, clean_digits, payload.notes or '', payload.password, existing["id"])
        )
        conn.commit()
        conn.close()
        return {"role": "student", "studentId": existing["id"], "name": existing["name"]}

    new_id = f"s_{int(time.time())}"
    cursor.execute("""
    INSERT INTO students (id, name, grade, rate, phone, wa, notes, password)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (new_id, payload.name, payload.grade, 220.0, payload.phone, clean_digits, payload.notes, payload.password))
    conn.commit()
    conn.close()
    
    return {"role": "student", "studentId": new_id, "name": payload.name}

@app.get("/api/students")
def list_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, rate, phone, wa, notes FROM students ORDER BY name ASC")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

@app.post("/api/students")
def add_student_by_teacher(payload: SignUpPayload):
    return signup(payload)

@app.get("/api/lessons")
def list_lessons(weekId: Optional[str] = None, studentId: Optional[str] = None):
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
def save_lesson(lesson: LessonPayload):
    try:
        lesson_date = datetime.strptime(lesson.date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Lesson date is invalid.")

    if lesson_date < datetime.utcnow().date():
        raise HTTPException(status_code=400, detail="You cannot schedule a lesson in the past.")

    conn = get_db()
    cursor = conn.cursor()
    lid = lesson.id or f"l_{int(time.time())}"
    
    cursor.execute("""
    INSERT OR REPLACE INTO lessons (id, studentId, studentName, weekId, day, date, startTime, endTime, rate, payment, method, status, topic, location)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (lid, lesson.studentId, lesson.studentName, lesson.weekId, lesson.day, lesson.date, lesson.startTime, lesson.endTime, lesson.rate, lesson.payment, lesson.method, lesson.status, lesson.topic, lesson.location))
    
    conn.commit()
    conn.close()
    return {"id": lid, "status": "saved"}

@app.delete("/api/lessons/{lesson_id}")
def delete_lesson(lesson_id: str):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM lessons WHERE id = ?", (lesson_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

@app.get("/api/requests")
def list_requests(studentId: Optional[str] = None):
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
def create_request(req: RequestPayload):
    conn = get_db()
    cursor = conn.cursor()
    rid = f"req_{int(time.time())}"
    now_iso = datetime.utcnow().isoformat() + "Z"
    
    cursor.execute("""
    INSERT INTO requests (id, studentId, studentName, lessonId, lessonSummary, requestType, message, dateSubmitted, status, teacherReply, teacherReplyDate)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (rid, req.studentId, req.studentName, req.lessonId, req.lessonSummary, req.requestType, req.message, now_iso, "Pending", "", None))
    conn.commit()
    conn.close()
    return {"id": rid, "status": "submitted"}

@app.post("/api/requests/{request_id}/reply")
def reply_request(request_id: str, payload: ReplyPayload):
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print("==================================================")
    print(f" Annette's Private Lessons Server Running on {host}:{port}")
    print("==================================================")
    uvicorn.run("server:app", host=host, port=port)
