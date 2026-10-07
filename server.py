"""
Helen's English Studio — Python FastAPI + SQLite Application Server
Runs on: http://127.0.0.1:8000
"""

import sqlite3
import json
import os
import time
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Helen's English Studio API", version="2.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HTML_FILE = os.path.join(os.path.dirname(__file__), "english_tutoring_portal.html")

def get_db():
    # Attempt local dir first, then fallback to /tmp if filesystem lacks lock support
    candidates = [
        os.path.join(os.path.dirname(__file__), "tutoring.db"),
        "/tmp/tutoring.db",
        "tutoring.db"
    ]
    for path in candidates:
        try:
            conn = sqlite3.connect(path, timeout=5.0)
            conn.row_factory = sqlite3.Row
            # test write
            conn.execute("CREATE TABLE IF NOT EXISTS _test_probe (id INT)")
            return conn
        except Exception:
            continue
    # In-memory fallback if disk writes are restricted
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
        rate REAL DEFAULT 45.0,
        phone TEXT,
        wa TEXT,
        notes TEXT,
        password TEXT DEFAULT 'student123'
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
        rate REAL DEFAULT 45.0,
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
    
    # Check if empty, seed defaults
    cursor.execute("SELECT COUNT(*) as cnt FROM students")
    if cursor.fetchone()["cnt"] == 0:
        cursor.executemany("""
        INSERT INTO students (id, name, grade, rate, phone, wa, notes, password)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            ('s1', 'Maya Ronen', '9th Grade', 45.0, 'Sarah (Mom) 054-234-5678', '972542345678', 'Grammar tenses and speaking confidence.', 'student123'),
            ('s2', 'Daniel Klein', '11th Grade (5 Units)', 50.0, 'David (Dad) 050-987-6543', '972509876543', 'Bagrut Module E practice and unseen texts.', 'student123'),
            ('s3', 'Liam Shahar', '7th Grade', 40.0, 'Rachel 052-333-8899', '972523338899', 'Reading comprehension and school homework.', 'student123'),
            ('s4', 'Emma Tal', '10th Grade', 45.0, 'Noa 053-444-1122', '972534441122', 'Essay writing structure and rich vocabulary.', 'student123'),
            ('s5', 'Noah Ben-David', '8th Grade', 40.0, 'Itai 050-555-7788', '972505557788', 'Irregular verbs drill and conversational fluency.', 'student123')
        ])
        
        cursor.executemany("""
        INSERT INTO lessons (id, studentId, studentName, weekId, day, date, startTime, endTime, rate, payment, method, status, topic, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            ('l1', 's1', 'Maya Ronen', '2026-W41', 'Sunday', '2026-10-04', '16:00', '17:00', 45.0, 'Paid', 'Bit', 'Completed', 'Present Perfect & Vocabulary', 'Studio (In-Person)'),
            ('l2', 's3', 'Liam Shahar', '2026-W41', 'Sunday', '2026-10-04', '17:15', '18:15', 40.0, 'Paid', 'Cash', 'Completed', 'School Book Chapter 4', 'Studio (In-Person)'),
            ('l3', 's2', 'Daniel Klein', '2026-W41', 'Monday', '2026-10-05', '16:30', '17:30', 50.0, 'Unpaid', 'Bank Transfer', 'Completed', '5-Unit Module E Practice', 'Online (Zoom / Meet)'),
            ('l4', 's4', 'Emma Tal', '2026-W41', 'Tuesday', '2026-10-06', '15:30', '16:30', 45.0, 'Paid', 'PayBox', 'Completed', 'Opinion Essay Writing', 'Studio (In-Person)'),
            ('l5', 's5', 'Noah Ben-David', '2026-W41', 'Wednesday', '2026-10-07', '16:00', '17:00', 40.0, 'Unpaid', 'Bit', 'Confirmed', 'Irregular Verbs Drill', 'Studio (In-Person)'),
            ('l6', 's1', 'Maya Ronen', '2026-W41', 'Thursday', '2026-10-08', '16:30', '17:30', 45.0, 'Unpaid', 'Bit', 'Confirmed', 'Conversation & Speech', 'Online (Zoom / Meet)'),
            ('l7', 's2', 'Daniel Klein', '2026-W41', 'Friday', '2026-10-09', '11:00', '12:00', 50.0, 'Unpaid', 'Bank Transfer', 'Confirmed', 'Literature Analysis', 'Studio (In-Person)')
        ])
        
        cursor.executemany("""
        INSERT INTO requests (id, studentId, studentName, lessonId, lessonSummary, requestType, message, dateSubmitted, status, teacherReply, teacherReplyDate)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, [
            ('r1', 's1', 'Maya Ronen', 'l6', 'Thursday (Oct 8) @ 16:30', 'Reschedule', 'Hi Teacher Helen! I have a school biology exam on Thursday afternoon. Could we please move our lesson to Thursday at 18:00 or Friday morning?', '2026-10-06T18:30:00Z', 'Answered', 'Hi Maya! Yes, Thursday at 18:00 works well for me. I updated the schedule for you.', '2026-10-06T19:15:00Z'),
            ('r2', 's5', 'Noah Ben-David', 'l5', 'Wednesday (Oct 7) @ 16:00', 'Cancel', 'Hello Helen, Noah is not feeling well with a fever today and cannot attend. Can we make it up next week?', '2026-10-07T08:15:00Z', 'Pending', '', None)
        ])
    
    conn.commit()
    conn.close()

init_db()

# Models
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

# Routes
@app.get("/")
def serve_frontend():
    if os.path.exists(HTML_FILE):
        return FileResponse(HTML_FILE)
    return HTMLResponse("<h1>Helen's English Studio</h1><p>english_tutoring_portal.html not found</p>")

@app.get("/api/health")
def health():
    return {"status": "ok", "app": "Helen's English Studio Python Backend"}

@app.post("/api/auth/login")
def login(payload: LoginPayload):
    conn = get_db()
    cursor = conn.cursor()
    
    if payload.role == "teacher":
        conn.close()
        if payload.password in ["helen123", "admin"]:
            return {"role": "teacher", "name": "Helen"}
        raise HTTPException(status_code=401, detail="Invalid teacher password (default: helen123)")
    else:
        cursor.execute("SELECT * FROM students WHERE id = ? OR name = ?", (payload.usernameOrId, payload.usernameOrId))
        student = cursor.fetchone()
        conn.close()
        if not student:
            raise HTTPException(status_code=404, detail="Student account not found")
        if student["password"] and student["password"] != payload.password:
            raise HTTPException(status_code=401, detail="Incorrect password (default: student123)")
        return {"role": "student", "studentId": student["id"], "name": student["name"]}

@app.post("/api/auth/signup")
def signup(payload: SignUpPayload):
    conn = get_db()
    cursor = conn.cursor()
    new_id = f"s_{int(time.time())}"
    
    clean_digits = "".join([c for c in payload.phone if c.isdigit()])
    if clean_digits.startswith("0"):
        clean_digits = "972" + clean_digits[1:]
        
    cursor.execute("""
    INSERT INTO students (id, name, grade, rate, phone, wa, notes, password)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (new_id, payload.name, payload.grade, 45.0, payload.phone, clean_digits, payload.notes, payload.password))
    conn.commit()
    conn.close()
    
    return {"role": "student", "studentId": new_id, "name": payload.name}

@app.get("/api/students")
def list_students():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, grade, rate, phone, wa, notes FROM students")
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items

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
    cursor.execute("""
    UPDATE requests SET teacherReply = ?, teacherReplyDate = ?, status = ? WHERE id = ?
    """, (payload.reply, now_iso, payload.newStatus, request_id))
    conn.commit()
    conn.close()
    return {"status": "replied"}

if __name__ == "__main__":
    print("==================================================")
    print(" Helen's English Studio Server Running!")
    print(" Open in your browser: http://127.0.0.1:8000")
    print("==================================================")
    uvicorn.run(app, host="127.0.0.1", port=8000)
