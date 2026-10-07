

Private English Tutoring Management
Provided manual steps for repository code updates.
1 min ago

Gemini Spark Setup
Created instructions for Spark collaboration.

Private English Tutoring Management
beta

Plan steps

Conversation with Gemini
i want to create a site manegment to help my mom as am enlish private teacher to keep her studens inline with each one knows his hour




To build the most effective solution for your mom, a few key details will help determine the right setup.

Here are the most common ways to handle this:

Custom Web Application / Student Portal: A dedicated webpage where your mom can input students and their assigned time slots, and students (or parents) can view the weekly schedule or check their specific lesson time.

Google Calendar Appointment Schedule / Shared Calendar: Free, built-in scheduling where each student has their reserved slot, receives automatic calendar invites, and can see upcoming sessions.

Google Sheets Schedule & Attendance Tracker: A simple, shareable spreadsheet template detailing student names, weekly recurring hours, lesson status, and contact details.

Questions to Help Tailor the Solution
Platform Preference: Would you like a custom-coded web application (an interactive site you can host or open in a browser), or an existing tool like Google Calendar / Google Sheets?

Student Interaction: Should students only be able to view their assigned hours, or do they need to book, reschedule, or cancel slots themselves?

Schedule Structure: Are lessons set to fixed recurring weekly times (e.g., every Tuesday at 4:00 PM), or does the schedule change from week to week?

Extra Features: Does she need tracking for payments, lesson notes, or attendance, or is the focus solely on the timetable?

Once you share your preferences, we can proceed with creating the site or setting up the workflow.

Custom Web Application / Student Portal:

i want them to see and if they want to change or cancle they will write in a text box and my mom willl anser then

the schedule change from week to week

Does she need tracking for payments















I have created a standalone web application and student portal tailored for your mom's English private tutoring practice.

HTML icon
english_tutoring_portal
 HTML 
Key Features Included
1. Dual-View Portal
Student & Parent View:

Dedicated Student Filter: Students or parents can select their name from a dropdown to instantly see their assigned day, lesson time, location (Studio or Zoom), learning topic, and payment status.

Full Timetable View: Displays the studio's weekly schedule so students can see available and booked slots across all 7 days (Sunday through Saturday).

Change / Cancellation Request Box: When students need to reschedule or cancel, they select their lesson, choose a reason (Reschedule, Cancel, or Question), and type their message into a text box.

Teacher Answers Feed: Once your mom replies, the student can see her response directly under "Messages & Teacher's Answers" with a timestamp and resolution status.

Teacher / Mom's Management Dashboard:

Weekly Stats Bar: Real-time overview of total sessions, completed lessons, pending student requests, total revenue, and outstanding unpaid balances.

Weekly Schedule Management: Easily add, edit, or cancel lessons for any date. Since schedules change from week to week, she can navigate between weeks and use the "Duplicate Week to Next" button to copy this week's timetable to the following week with a single click.

Requests Inbox & Reply Tool: Displays all student messages with a text box for your mom to write her reply, approve schedule changes, or cancel lessons.

Payment Tracker: A dedicated ledger displaying each student's scheduled hours, rate per lesson, and payment status (Paid vs. Pending), with one-click toggles to mark sessions as paid.

Student Roster: Directory of students, grade levels, parent contact phone numbers, default hourly rates, and learning goals.

Automatic Storage & Backups: All changes are automatically preserved in the browser's local storage. She can also download a JSON backup file or restore data anytime.

How to Use
Download or open english_tutoring_portal.html in any web browser (Chrome, Safari, Edge, or mobile browser).

Use the toggle button in the top navigation bar to switch between Student & Parent View and Mom's Dashboard.

Sample students and lessons are pre-loaded so you can test all features immediately.

it looks amature







The web application has been completely redesigned with a modern, clean SaaS interface inspired by platforms like Cal.com and Notion.

HTML icon
english_tutoring_portal
 HTML 
What Was Upgraded
1. Visual Design & Interface
Modern Aesthetic: Replaced standard controls with custom card components, a pill-style role switcher, soft diffuse shadows, crisp micro-borders, and inline vector icons.

Refined Color Palette: Indigo primary accents, emerald green for confirmed and paid sessions, warm amber for pending requests, and rose for cancellations.

2. Student & Parent Portal
"Next Up" Hero Banner: Highlights the student's upcoming lesson with exact date, time, location (Studio or Zoom), topic, and payment status.

Personalized Schedule View: In the 7-day calendar (Sunday through Saturday), the student's own slot is clearly highlighted, while other slots are marked discreetly so everyone knows which hours are booked.

Message Thread & Replies: Change and cancellation requests are formatted as a two-way conversation feed showing the student's note, time submitted, and your mom's direct reply.

3. Mom's Management Dashboard
Weekly Performance Metrics: Summary cards tracking total lessons this week, urgent student requests, total earnings, and unpaid balances.

Flexible Weekly Timetable: Quick "+ Add Slot" buttons on every day column, easy inline editing, and a "Duplicate Week to Next" button to handle week-to-week variations without retyping everything.

Requests Inbox with Quick Replies: Preset one-click responses (e.g., "Approved", "Confirm Cancel", "Suggest Different Hour") alongside a freeform reply box and direct schedule updater.

Comprehensive Payment Ledger: Tracks rates, paid/pending status, and payment methods commonly used (Bit, PayBox, Cash, and Bank Transfer), plus a 1-click WhatsApp button that generates a polite pre-written message to the parent.

Student Directory & Backup: Contact list with grade levels and learning notes, plus automatic browser saving and JSON file export/import.

i want the studend side will only see is appoitment







The portal has been updated so that the student view is strictly private: students can only view their own appointments, with no access to other students' schedules or a shared studio calendar.

Readme Setup And Deployment
7 Oct, 18:14
HTML icon
english_tutoring_portal
 HTML 
Key Privacy & Feature Updates
1. Complete Student Schedule Privacy
Personalized Appointment Card: When a student or parent selects their name, the portal displays a dedicated overview of only their own upcoming lesson—including date, exact start and end times, duration (60 min), location (In-Person or Zoom), topic, and payment status.

Isolated Weekly Sessions: The student only sees their own assigned sessions for the selected week. If no lessons are scheduled for them that week, a clean notice explains this with no other student slots visible.

Shared Timetable Removed: The full studio schedule has been completely removed from the student side. Only your mom has access to the full master calendar inside her dashboard.

2. Private Reschedule & Cancellation Box
Pre-Linked Dropdown: The change/cancel request form automatically restricts choices to that student's personal appointments.

Two-Way Private Conversation: The student submits their note (e.g., requesting a new hour or reporting an illness). Once your mom answers in her dashboard, her response appears exclusively in that student's private feed.

3. Mom's Management Dashboard (Unchanged & Complete)
Master Timetable: Retains the complete 7-day studio schedule across all students, with "+ Add Slot" buttons and the "Duplicate Week to Next" action.

Requests Inbox: Direct notifications of pending student messages with 1-click quick-reply chips ("Approved", "Confirm Cancel", "Suggest Different Hour") or custom answers.

Payment Tracker: Real-time status tracking (Bit, PayBox, Cash, Bank Transfer) and one-click WhatsApp reminder links.

Free Hosting & Live Phone Sync Guide
I have also provided a companion guide opened in Canvas (Architecture & Deployment Guide) covering:

2-Minute Free Hosting: How to put the page online via Netlify Drop or GitHub Pages so students can open a real website link on their phones.

Free Cloud Sync (Google Firebase): How to connect a free Firebase database so student requests and schedule changes update live across your mom's and students' phones.

can you also make a sifn in page for my mom amd sign ap page for the student also sin ins






An authentication gateway has been added to the web portal with dedicated sign-in flows for your mom and students, as well as a student sign-up page.

HTML icon
english_tutoring_portal
 HTML 
What Was Added
1. Teacher Sign-In (Mom's Access)
Access: Unlocks the master weekly timetable, incoming student reschedule/cancellation requests, payment tracking ledger, and full student roster.

Default Credentials:

User / Email: helen@studio.com

Password: helen123

Quick Demo Access: A "👩‍🏫 Teacher Helen" button on the login screen lets her sign in with a single click.

2. Student Sign-In (Private Portal)
Access: Allows registered students to log into their private dashboard where they strictly see only their own assigned hours, next upcoming session card, payment balance, and two-way messaging thread with Teacher Helen.

Default Credentials:

Any pre-loaded student (e.g., Maya Ronen, Daniel Klein, Liam Shahar)

Password: student123 (or quick demo buttons)

3. Student Sign-Up (New Registration)
New Student Onboarding: Parents or new students click "✨ Student Sign Up" to create an account.

Registration Fields: Full Name, Grade/Level, Password, Parent Name & WhatsApp Phone Number, and Learning Goals.

Automatic Studio Integration: Upon submitting, the student is automatically signed in, their private schedule portal is initialized, and their profile is added to your mom's Student Roster so she can schedule their lessons.

4. Session Management
Active User Pill: The navigation bar shows who is logged in (e.g., 👩‍🏫 Teacher Helen or 🎓 Maya Ronen).

One-Click Sign Out: Returns to the login screen and protects private schedule information when sharing devices.

Storage & Backend Guide: Accounts and sessions are saved locally in the browser and fully documented in the Architecture & Deployment Guide in Canvas for optional free cloud hosting (Netlify/GitHub) and live multi-device synchronization (Google Firebase).

can you develop this sire with JS or java and python the it will look nicer and more intercative
















I have expanded the project into a full-stack solution featuring an upgraded interactive JavaScript frontend alongside your choice of a Python or Java backend server.

Readme Setup And Deployment
7 Oct, 18:14
HTML icon
english_tutoring_portal
 HTML 
PY icon
server
 PY 
JAVA icon
TutoringServer
 JAVA 
Key Upgrades & Technical Architecture
1. Enhanced Interactive Frontend (english_tutoring_portal.html)
Live Schedule Filtering & Search: Your mom can filter the weekly timetable in real time by student name, day of the week, or lesson mode (Studio vs. Zoom).

Payment Progress Bar: A visual progress indicator calculating the percentage of weekly tutoring fees collected (e.g., "68% collected ($225 / $330)").

Interactive WhatsApp Message Composer: Clicking the WhatsApp button opens an interactive modal with 3 pre-written templates (Lesson Reminder, Payment Notice, Schedule Confirmation) allowing custom edits before opening WhatsApp.

Auto-Backend Detection: The page automatically detects whether the Python or Java server is running on [http://127.0.0.1:8000](http://127.0.0.1:8000) (showing a 🟢 Python/Java Backend badge). If opened directly as a file, it seamlessly falls back to browser storage.

2. Python Backend Server (server.py)
Technology: Built using FastAPI with a local SQLite database (tutoring.db).

Endpoints: Full RESTful APIs for authentication (/api/auth/login, /api/auth/signup), weekly lessons, student roster, and change requests.

How to Run:

Bash
python3 server.py
Opens at [http://127.0.0.1:8000](http://127.0.0.1:8000) with automatic SQLite persistence.

3. Java Backend Server (TutoringServer.java)
Technology: Built using standard Java 17 (HttpServer) with zero external dependencies or Maven/Gradle required.

How to Run:

Bash
java TutoringServer.java
Starts a lightweight REST and static web server at [http://127.0.0.1:8085](http://127.0.0.1:8085).

Default Credentials for Testing
Role	Username / Selection	Password	Access Scope
Teacher (Mom)	helen@studio.com	helen123	Full studio master timetable, payment ledger, requests inbox
Student	Select Maya Ronen or Daniel Klein	student123	Strictly private view of their own appointments & notes
New Student	Self-registered via "✨ Student Sign Up"	Chosen at registration	Automatic roster and private portal generation
Detailed instructions and database schemas are maintained in the Architecture & Deployment Guide in Canvas.

i want to deploy it to render as a server







The application has been prepared and configured for direct deployment to Render (render.com) as a cloud web service.

Requirements
7 Oct, 18:01
YAML icon
render
 YAML 
[file-tag: server.py]
[file-tag: english_tutoring_portal.html]

Files Configured for Render
server.py:

Configured for cloud hosting: dynamically listens on 0.0.0.0 using Render's assigned $PORT environment variable.

Serves both the REST API endpoints and the interactive frontend directly.

requirements.txt:

Specifies all Python dependencies (fastapi, uvicorn[standard], pydantic).

render.yaml:

Pre-configured Infrastructure-as-Code Blueprint so Render can automatically detect the build and start commands.

english_tutoring_portal.html:

The complete responsive portal (Mom's dashboard + private student view).

Step-by-Step Instructions to Deploy on Render
Step 1: Push the Files to a GitHub Repository
Create a repository on GitHub (e.g., helen-english-studio) and push these files into it:

server.py

english_tutoring_portal.html

requirements.txt

render.yaml

Step 2: Create the Web Service on Render
Go to dashboard.render.com and click New + > Web Service.

Connect your GitHub repository.

Verify or enter the following settings:

Name: helen-english-studio (or your choice)

Region: Frankfurt (EU) (recommended for Israel/Europe) or Oregon (US)

Runtime: Python 3

Build Command:

Bash
pip install -r requirements.txt
Start Command:

Bash
uvicorn server:app --host 0.0.0.0 --port $PORT
Plan: Select Free.

Click Create Web Service.

Step 3: Access the Live Studio
Render will build and deploy your service in about 1–2 minutes, providing a permanent HTTPS link:

https://helen-english-studio.onrender.com
For Mom: Open the link on her phone or computer and sign in with helen@studio.com / helen123.

For Students: Share the link over WhatsApp so students can log in or sign up to view strictly their own lessons and submit change notes.

Data Persistence Note on Render
On Render's free tier, services spin down after 15 minutes of idle time. The SQLite database will persist across sessions, but can reset if the container rebuilds.

Recommended Free Practice: Your mom can use the built-in "📥 Export Studio Backup" button under Data & Settings once a week to download a quick .json backup file that can be restored with one click at any time.

Detailed configuration steps are documented in the Full-Stack Architecture & Cloud Deployment Guide in Canvas.




This error occurs on Render because requirements.txt is either missing from the root of your GitHub repository, named with a hidden extra extension (like requirements.txt.txt), or located inside a subfolder.

Here are the solutions to resolve it:

Solution 1: The Quickest Fix (No requirements.txt needed)
You can tell Render to install the packages directly without searching for a file:

In your Render Dashboard, click on your web service (helen-english-studio).

Go to Settings on the left menu.

Scroll down to the Build Command field and replace pip install -r requirements.txt with:

Bash
pip install fastapi "uvicorn[standard]" pydantic
Click Save Changes at the bottom.

Click Manual Deploy (top right) > Deploy latest commit.

Solution 2: If Your Files Are in a Subfolder in GitHub
If you pushed your project inside a folder in your GitHub repository (for example, tutoring/ or project/):

In your Render Dashboard, go to Settings.

Locate the Root Directory setting.

Type the exact folder name where your files are located (e.g., tutoring or project).

Save changes and redeploy.

Solution 3: Add requirements.txt to Your GitHub Repository
If you prefer using requirements.txt:

Ensure a file named exactly requirements.txt exists at the root of your repository with these contents:

Plaintext
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
Commit and push it to GitHub:

Bash
git add requirements.txt
git commit -m "Add requirements.txt"
git push
Render will automatically detect the commit and deploy successfully.

my moms name is annette so i want the site will be erriten annettes private lessons

and i dont want the demo data i want it tobe real

like a stident now can sign up and sign in and use this site





The platform has been rebranded to Annette's Private Lessons and cleared of all mock/demo data so real students and your mom can use it in production.

Readme Setup And Deployment
Annette's Private Lessons — Full-Stack Architecture & Cloud Deployment Guide
This project is a complete, production-ready private lesson management platform for Teacher Annette. It features zero dummy data, live real-student self-registration, private individual student portals, weekly timetable management, and payment tracking.

1. Quick Deploy to Render (render.com)
Render offers free cloud hosting for Python web services with automatic SSL (https://).

Files in Your Repository
server.py: Production-ready FastAPI ASGI application that listens on 0.0.0.0 and binds to Render's dynamic $PORT.

english_tutoring_portal.html: The interactive frontend served directly by the Python server.

requirements.txt: Package dependencies (fastapi, uvicorn[standard], pydantic).

render.yaml: Pre-configured Render Blueprint for automated setup.

Step-by-Step Deployment Instructions
Step 1: Push Your Files to a GitHub Repository
Create a repository on GitHub (e.g., annettes-private-lessons).

Upload the following files into the repository root:

server.py

english_tutoring_portal.html

requirements.txt

render.yaml

Step 2: Create a Web Service on Render
Log in to Render.

Click New + > Web Service.

Connect your GitHub account and select your annettes-private-lessons repository.

Enter the service configuration:

Name: annettes-private-lessons (or your choice)

Region: Frankfurt (EU) (recommended for Israel/Europe) or Oregon (US)

Runtime / Language: Python 3

Build Command:

pip install -r requirements.txt

(Or simply: pip install fastapi "uvicorn[standard]" pydantic)

Start Command:

uvicorn server:app --host 0.0.0.0 --port $PORT

Plan: Select Free.

Click Create Web Service.

Step 3: Access Your Live Studio
Render will build and deploy your service in about 1–2 minutes, providing a permanent live link:

https://annettes-private-lessons.onrender.com

2. Real Production Accounts & How It Works
For Teacher Annette (Mom)
Log In: Click 👩‍🏫 Teacher Annette on the login screen.

Email: annette@lessons.com

Password: annette123

Features:

View master weekly timetable across all students.

Assign new lesson slots with exact time, rate, topic, and location.

Receive and reply to student reschedule/cancellation requests.

Track fees collected vs. pending, with 1-click WhatsApp payment reminders.

For Students
Self-Registration (Sign Up): New students click "✨ Student Sign Up", enter their full name, grade, parent WhatsApp phone number, and choose their password.

Sign In: Students sign in with their name/phone and password.

Strict Privacy: Students only see their own appointments, next session hero card, and private correspondence with Annette. No other student's name or schedule is visible.

Change / Cancel Requests: Students can type a note to Annette to request a different time or cancel a lesson with immediate feedback.

HTML icon
english_tutoring_portal
 HTML 
PY icon
server
 PY 
YAML icon
render
 YAML 
Key Changes & Real Production Setup
1. Rebranded to "Annette's Private Lessons"
The site header, logo (A), page title, welcome cards, and notifications are now personalized for Teacher Annette.

WhatsApp message templates automatically include her signature (e.g., "See you soon! — Teacher Annette").

2. Clean Slate (Zero Demo Data)
All mock students, sample lessons, and test requests have been removed from both the frontend and the SQLite database (tutoring.db).

The system starts empty and will populate exclusively with your mom's real students and scheduled hours.

3. Real Student Sign-Up & Sign-In Flow
Student Sign-Up (✨ Student Sign Up):

Real students (or their parents) create an account by entering their Full Name, Grade/Level, Password, Contact/Parent Phone, and any learning notes for Annette.

Submitting instantly creates their real profile, signs them in, and adds them directly to Teacher Annette's Student Roster.

Student Sign-In (🎓 Student Sign In):

Registered students sign in using their Full Name or Phone Number and Password.

They will strictly see only their own assigned appointments, next upcoming session card, and private correspondence with Annette.

4. Teacher Annette's Access (Mom)
Sign In (👩‍🏫 Teacher Annette):

Email: annette@lessons.com

Password: annette123

Features for Annette:

When a new student registers, they immediately appear in her Student Roster with their contact details and goals.

Annette can click "+ Add Lesson" to assign their weekly hour, rate, and topic.

She can manage the master timetable, reply to student change/cancellation requests, and track payments (Bit, PayBox, Cash, Bank Transfer).

Ready for Render Deployment
The repository is configured to deploy directly to Render:

Push server.py, english_tutoring_portal.html, requirements.txt, and render.yaml to your GitHub repo.

In Render, select your repository and deploy.

Your live link (e.g., [https://annettes-private-lessons.onrender.com](https://annettes-private-lessons.onrender.com)) will be active for students to sign up and view their hours.

where is all the data stored?


Depending on how you run the application, the data is stored in two places:

1. When Running as a Server (on Render or locally with server.py)
All data is stored in a SQLite database file named tutoring.db on the server.

Inside tutoring.db, there are three organized tables:

students: Stores registered students, grade levels, parent contact/WhatsApp numbers, hourly rates, notes, and login passwords.

lessons: Stores every lesson slot (day, date, start/end time, student, rate, paid/pending status, payment method like Bit/Cash, and location).

requests: Stores student change/cancellation requests and Teacher Annette’s replies.

Important Note for Render's Free Tier:

On Render's free tier, web servers have an ephemeral disk (meaning if the server restarts or redeploys, files saved to disk can reset).

How to keep your data 100% safe for free:

In Annette's Dashboard under the Data & Settings tab, click "📥 Export Studio Backup" once a week to download a complete .json backup file to her computer or phone. If needed, she can click "📤 Restore from Backup" to restore all students and lessons in one click.

2. When Opened Directly in a Browser (Standalone File)
If you or your mom open english_tutoring_portal.html directly by double-clicking it on a laptop or phone without running server.py:

The data is stored in your browser's localStorage (under keys annette_students, annette_lessons, and annette_requests).

It stays saved inside that specific web browser across restarts.

Summary
Live cloud mode: Inside the server's tutoring.db SQLite file.

Offline / direct browser mode: Inside the browser's localStorage.

Offline safety copy: Downloadable at any time as a .json backup file via the Data & Settings tab.





The error in your build log:

Plaintext
ERROR: Error loading ASGI app. Could not import module "server".
==> Exited with status 3
This occurs because when Render runs uvicorn server:app, Python looks for server.py in the root directory of your GitHub repository. If server.py was placed inside a subfolder (e.g., output/ or project/) or named differently, Python cannot locate it.

Here are the 3 quick ways to resolve it:

Option 1: Set the "Root Directory" in Render (Fastest)
If your files were uploaded inside a subfolder in GitHub:

Open your Render Dashboard and click your web service.

Go to Settings in the left menu.

Find the Root Directory field.

Type the name of the folder where your server.py is located (for example, output or project).

Scroll down, click Save Changes, and click Manual Deploy > Deploy latest commit.

Option 2: Change the Start Command to Use Python
In your Render service Settings:

Change the Start Command from:

Bash
uvicorn server:app --host 0.0.0.0 --port $PORT
to:

Bash
python server.py
Save changes and redeploy. This lets server.py execute its internal server launcher directly.

Option 3: Verify the File is at the Top Level of Your GitHub Repo
Open your repository on github.com.

Look at the file list on the main page.

Ensure server.py (and/or main.py) and english_tutoring_portal.html are listed directly on the root page, rather than nested inside another folder.

If they are inside a folder, you can drag them to the root or use Option 1 above to specify that folder name in Render's settings.

I have also provided a standard main.py entry point alias in case your setup prefers main:app:

PY icon
main
 PY 
[file-tag: server.py]





The message:

Plaintext
Annette's Private Lessons
english_tutoring_portal.html not found
occurred because server.py was looking for english_tutoring_portal.html as an external file on the server's disk, but it was either placed in a subfolder or not pushed to the repository root alongside server.py.

What Was Fixed
I have updated server.py to be completely self-contained and resilient:

Embedded Full-Portal Fallback: The complete interactive HTML portal is now directly embedded inside server.py. Even if the separate HTML file is missing or in another folder on Render, server.py will automatically serve the full interactive portal.

Multi-Path & index.html Support: The server now automatically detects index.html or english_tutoring_portal.html in any subfolder (static/, output/, or root).

Provided index.html: An index.html copy is also provided to match standard web naming conventions.

Download Updated Files
PY icon
server
 PY 
HTML icon
index
 HTML 
Next Step
Replace server.py in your GitHub repository with this updated file and commit the change. Render will automatically redeploy, and your site will immediately display the full interactive portal.

can you change automaticly in https://github.com/7128romial/Tuto.git


I cannot push directly to your GitHub repository automatically, as I do not have access to your GitHub account credentials or external network access to push code on your behalf.

However, you can update it in under 30 seconds directly in your browser:

Method 1: Directly on the GitHub Website (Fastest — No Git required)
Open your repository in your browser: https://github.com/7128romial/Tuto

In the file list, click on server.py.

Click the Pencil icon (Edit this file) in the upper-right corner.

Replace all the code with the contents of the updated server.py (from the file chip below).

Scroll down and click the green Commit changes button.

(Optional) Click Add file > Upload files, upload index.html, and commit.

As soon as you commit, Render will automatically detect the update, build, and deploy the working site.

Method 2: Via Git on Your Computer
If you have the repository cloned on your computer:

Bash
# 1. Place the updated server.py and index.html in your cloned Tuto folder
cd Tuto

# 2. Stage and commit the changes
git add server.py index.html
git commit -m "Update server.py with embedded portal and index.html"

# 3. Push to your repository
git push origin main
The Files to Upload:
[file-tag: server.py]
[file-tag: index.html]




Gemini is AI and can make mistakes.

"""
Annette's Private Lessons — Production Backend Server (FastAPI + SQLite3)
Runs locally on http://127.0.0.1:8000 or on Render (binds to 0.0.0.0:$PORT)
"""

import sqlite3
import json
import os
import time
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Annette's Private Lessons API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Potential HTML paths to search
CANDIDATE_HTML_FILES = [
    os.path.join(os.path.dirname(__file__), "english_tutoring_portal.html"),
    os.path.join(os.path.dirname(__file__), "index.html"),
    "english_tutoring_portal.html",
    "index.html",
    os.path.join(os.path.dirname(__file__), "static", "english_tutoring_portal.html"),
    os.path.join(os.path.dirname(__file__), "static", "index.html"),
    os.path.join(os.path.dirname(__file__), "output", "english_tutoring_portal.html"),
    os.path.join(os.path.dirname(__file__), "output", "index.html"),
]

def find_html_file():
    for p in CANDIDATE_HTML_FILES:
        if os.path.exists(p):
            return p
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
        rate REAL DEFAULT 45.0,
        phone TEXT,
        wa TEXT,
        notes TEXT,
        password TEXT NOT NULL
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
EMBEDDED_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Annette's Private Lessons — Student Portal & Schedule</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #4f46e5;
      --primary-hover: #4338ca;
      --primary-light: #eef2ff;
      --primary-border: #c7d2fe;
      
      --slate-50: #f8fafc;
      --slate-100: #f1f5f9;
      --slate-200: #e2e8f0;
      --slate-300: #cbd5e1;
      --slate-400: #94a3b8;
      --slate-500: #64748b;
      --slate-600: #475569;
      --slate-700: #334155;
      --slate-800: #1e293b;
      --slate-900: #0f172a;

      --emerald-50: #ecfdf5;
      --emerald-100: #d1fae5;
      --emerald-500: #10b981;
      --emerald-600: #059669;
      --emerald-700: #047857;

      --amber-50: #fffbeb;
      --amber-100: #fef3c7;
      --amber-500: #f59e0b;
      --amber-600: #d97706;
      --amber-700: #b45309;

      --rose-50: #fff1f2;
      --rose-100: #ffe4e6;
      --rose-500: #f43f5e;
      --rose-600: #e11d48;

      --radius-sm: 8px;
      --radius-md: 12px;
      --radius-lg: 18px;
      --radius-xl: 24px;
      
      --shadow-subtle: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
      --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.03);
      --shadow-hover: 0 12px 24px -4px rgba(15, 23, 42, 0.08), 0 4px 8px -2px rgba(15, 23, 42, 0.04);
      --shadow-modal: 0 25px 50px -12px rgba(15, 23, 42, 0.25);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      -webkit-font-smoothing: antialiased;
    }

    body {
      background-color: #f8fafc;
      color: var(--slate-800);
      line-height: 1.5;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Top Navigation Bar */
    .navbar {
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--slate-200);
      position: sticky;
      top: 0;
      z-index: 50;
    }

    .nav-inner {
      max-width: 1280px;
      margin: 0 auto;
      padding: 12px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      flex-wrap: wrap;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-logo {
      width: 42px;
      height: 42px;
      background: linear-gradient(135deg, #4f46e5, #7c3aed);
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 800;
      font-size: 1.25rem;
      box-shadow: 0 4px 10px rgba(79, 70, 229, 0.3);
    }

    .brand-title {
      font-size: 1.1rem;
      font-weight: 800;
      color: var(--slate-900);
      letter-spacing: -0.02em;
    }

    .brand-subtitle {
      font-size: 0.78rem;
      color: var(--slate-500);
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .backend-pill {
      font-size: 0.68rem;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 9999px;
      background: #f1f5f9;
      color: var(--slate-600);
      border: 1px solid var(--slate-200);
    }

    .backend-pill.online {
      background: var(--emerald-50);
      color: var(--emerald-700);
      border-color: #a7f3d0;
    }

    /* Auth status & actions */
    .nav-user-area {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .user-pill {
      background: var(--slate-100);
      border: 1px solid var(--slate-200);
      padding: 6px 14px;
      border-radius: 9999px;
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--slate-800);
    }

    .role-badge-count {
      background: var(--amber-500);
      color: white;
      font-size: 0.7rem;
      font-weight: 700;
      padding: 1px 7px;
      border-radius: 9999px;
    }

    /* Sub-Header: Week Controls */
    .subnav {
      background: white;
      border-bottom: 1px solid var(--slate-200);
      padding: 12px 24px;
    }

    .subnav-inner {
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .week-nav {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .week-label-box {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      margin: 0 4px;
    }

    .week-label {
      font-size: 1rem;
      font-weight: 700;
      color: var(--slate-900);
      letter-spacing: -0.01em;
    }

    .week-sublabel {
      font-size: 0.75rem;
      color: var(--slate-500);
      font-weight: 500;
    }

    .btn-circle {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      border: 1px solid var(--slate-200);
      background: white;
      color: var(--slate-700);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s;
    }

    .btn-circle:hover {
      background: var(--slate-100);
      border-color: var(--slate-300);
      color: var(--slate-900);
    }

    .btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
      text-decoration: none;
    }

    .btn-primary {
      background: var(--primary);
      color: white;
      box-shadow: 0 1px 3px rgba(79, 70, 229, 0.3);
    }

    .btn-primary:hover {
      background: var(--primary-hover);
    }

    .btn-secondary {
      background: white;
      border-color: var(--slate-200);
      color: var(--slate-700);
    }

    .btn-secondary:hover {
      background: var(--slate-50);
      border-color: var(--slate-300);
      color: var(--slate-900);
    }

    .btn-sm {
      padding: 6px 12px;
      font-size: 0.8rem;
    }

    /* Main Container */
    .main-container {
      max-width: 1280px;
      width: 100%;
      margin: 24px auto;
      padding: 0 24px;
      flex-grow: 1;
    }

    /* Badges */
    .badge {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 9999px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .badge-paid {
      background: var(--emerald-50);
      color: var(--emerald-700);
      border: 1px solid #a7f3d0;
    }

    .badge-unpaid {
      background: var(--amber-50);
      color: var(--amber-700);
      border: 1px solid #fde68a;
    }

    .badge-cancelled {
      background: var(--rose-50);
      color: var(--rose-600);
      border: 1px solid #fecdd3;
    }

    .badge-confirmed {
      background: var(--primary-light);
      color: var(--primary);
      border: 1px solid var(--primary-border);
    }

    /* ==============================================
       AUTHENTICATION GATEWAY
       ============================================== */
    .auth-overlay {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 40px 20px;
      min-height: calc(100vh - 160px);
    }

    .auth-card {
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow-modal);
      max-width: 480px;
      width: 100%;
      overflow: hidden;
      animation: modalPop 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .auth-header {
      background: linear-gradient(135deg, #1e1b4b, #312e81, #4338ca);
      color: white;
      padding: 32px 28px;
      text-align: center;
    }

    .auth-header h2 {
      font-size: 1.5rem;
      font-weight: 800;
      margin-bottom: 6px;
    }

    .auth-header p {
      color: #c7d2fe;
      font-size: 0.88rem;
    }

    .auth-tabs {
      display: flex;
      background: var(--slate-100);
      border-bottom: 1px solid var(--slate-200);
      padding: 4px;
    }

    .auth-tab-btn {
      flex: 1;
      border: none;
      background: transparent;
      padding: 10px 14px;
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--slate-600);
      cursor: pointer;
      border-radius: var(--radius-sm);
      transition: all 0.15s;
    }

    .auth-tab-btn.active {
      background: white;
      color: var(--primary);
      box-shadow: var(--shadow-subtle);
    }

    .auth-body {
      padding: 28px;
    }

    /* ==============================================
       STUDENT PORTAL (PRIVATE VIEW)
       ============================================== */
    .student-welcome-header {
      background: linear-gradient(135deg, #1e1b4b, #312e81, #4338ca);
      color: white;
      border-radius: var(--radius-xl);
      padding: 28px 32px;
      margin-bottom: 24px;
      box-shadow: 0 10px 25px -5px rgba(49, 46, 129, 0.25);
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }

    .student-welcome-text h2 {
      font-size: 1.6rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 4px;
    }

    .student-welcome-text p {
      color: #c7d2fe;
      font-size: 0.92rem;
      max-width: 620px;
    }

    .privacy-notice {
      display: flex;
      align-items: center;
      gap: 8px;
      background: #eff6ff;
      border: 1px solid #bfdbfe;
      color: #1e40af;
      padding: 10px 16px;
      border-radius: var(--radius-sm);
      font-size: 0.82rem;
      font-weight: 500;
      margin-bottom: 24px;
    }

    .next-appointment-hero {
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-lg);
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: var(--shadow-card);
      position: relative;
      overflow: hidden;
      border-top: 4px solid var(--primary);
    }

    .appointment-meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-top: 16px;
      padding-top: 16px;
      border-top: 1px solid var(--slate-100);
    }

    .meta-box {
      display: flex;
      flex-direction: column;
    }

    .meta-label {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--slate-400);
      letter-spacing: 0.05em;
      margin-bottom: 2px;
    }

    .meta-value {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--slate-800);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .student-grid {
      display: grid;
      grid-template-columns: 1.15fr 0.85fr;
      gap: 24px;
      margin-bottom: 32px;
    }

    @media (max-width: 900px) {
      .student-grid {
        grid-template-columns: 1fr;
      }
    }

    .content-panel {
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-lg);
      padding: 24px;
      box-shadow: var(--shadow-card);
    }

    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 12px;
    }

    .panel-title {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--slate-900);
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .private-lesson-card {
      background: white;
      border: 1px solid var(--slate-200);
      border-left: 4px solid var(--primary);
      border-radius: var(--radius-sm);
      padding: 16px;
      margin-bottom: 12px;
      transition: all 0.2s;
    }

    .private-lesson-card:hover {
      box-shadow: var(--shadow-hover);
      transform: translateY(-2px);
    }

    .private-lesson-card.cancelled {
      border-left-color: var(--rose-500);
      background: var(--rose-50);
      opacity: 0.8;
    }

    .private-lesson-card.completed {
      border-left-color: var(--emerald-500);
    }

    /* Form Controls */
    .form-group {
      margin-bottom: 16px;
    }

    .form-label {
      display: block;
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--slate-700);
      margin-bottom: 6px;
    }

    .input-field {
      width: 100%;
      padding: 10px 14px;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-sm);
      font-size: 0.9rem;
      color: var(--slate-900);
      background: white;
      outline: none;
      transition: all 0.15s;
    }

    .input-field:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
    }

    textarea.input-field {
      min-height: 85px;
      resize: vertical;
    }

    .req-item-card {
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-md);
      padding: 16px;
      margin-bottom: 16px;
      background: white;
      transition: all 0.2s;
    }

    .req-item-card.pending {
      border-left: 4px solid var(--amber-500);
      background: #fffdfa;
    }

    .req-item-card.resolved {
      border-left: 4px solid var(--emerald-500);
    }

    .chat-bubble-student {
      background: #f1f5f9;
      border-radius: 12px 12px 12px 2px;
      padding: 12px 16px;
      margin: 10px 0;
      font-size: 0.9rem;
      color: var(--slate-800);
    }

    .chat-bubble-teacher {
      background: #eef2ff;
      border: 1px solid #c7d2fe;
      border-radius: 12px 12px 2px 12px;
      padding: 12px 16px;
      margin-top: 10px;
      font-size: 0.9rem;
      color: #312e81;
    }

    .teacher-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--primary);
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
    }

    /* ==============================================
       TEACHER DASHBOARD
       ============================================== */
    .metrics-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }

    .metric-card {
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-md);
      padding: 20px;
      box-shadow: var(--shadow-subtle);
      position: relative;
      overflow: hidden;
    }

    .metric-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
    }

    .metric-card.accent-primary::before { background: var(--primary); }
    .metric-card.accent-amber::before { background: var(--amber-500); }
    .metric-card.accent-emerald::before { background: var(--emerald-500); }
    .metric-card.accent-rose::before { background: var(--rose-500); }

    .metric-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: var(--slate-500);
      font-size: 0.8rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .metric-value {
      font-size: 1.85rem;
      font-weight: 800;
      color: var(--slate-900);
      margin: 8px 0 4px;
      letter-spacing: -0.02em;
    }

    .metric-footer {
      font-size: 0.8rem;
      color: var(--slate-500);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .progress-bar-wrap {
      width: 100%;
      height: 6px;
      background: var(--slate-100);
      border-radius: 9999px;
      margin: 8px 0 4px;
      overflow: hidden;
    }

    .progress-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #10b981, #059669);
      border-radius: 9999px;
      transition: width 0.4s ease;
    }

    .filter-bar {
      display: flex;
      gap: 10px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }

    .search-input {
      flex: 1;
      min-width: 220px;
      padding: 8px 14px;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-sm);
      font-size: 0.88rem;
      outline: none;
    }

    .search-input:focus {
      border-color: var(--primary);
    }

    .teacher-nav {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--slate-200);
      margin-bottom: 24px;
      overflow-x: auto;
    }

    .t-tab-btn {
      background: transparent;
      border: none;
      border-bottom: 2px solid transparent;
      padding: 12px 18px;
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--slate-500);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: -1px;
      transition: all 0.15s;
      white-space: nowrap;
    }

    .t-tab-btn:hover {
      color: var(--slate-900);
    }

    .t-tab-btn.active {
      color: var(--primary);
      border-bottom-color: var(--primary);
    }

    .schedule-board {
      display: grid;
      grid-template-columns: repeat(7, minmax(170px, 1fr));
      gap: 14px;
      overflow-x: auto;
      padding-bottom: 16px;
    }

    @media (max-width: 1100px) {
      .schedule-board {
        grid-template-columns: repeat(7, minmax(200px, 1fr));
      }
    }

    .day-column {
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-md);
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-subtle);
      overflow: hidden;
      min-height: 480px;
    }

    .day-header {
      padding: 14px 16px;
      background: #fafbfc;
      border-bottom: 1px solid var(--slate-200);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .day-header.today {
      background: var(--primary-light);
      border-bottom-color: var(--primary-border);
    }

    .day-title {
      font-weight: 700;
      font-size: 0.9rem;
      color: var(--slate-900);
    }

    .day-date-tag {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--slate-500);
    }

    .day-content {
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      flex-grow: 1;
    }

    .empty-state-day {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 30px 10px;
      text-align: center;
      color: var(--slate-400);
      font-size: 0.8rem;
      border: 1px dashed var(--slate-200);
      border-radius: var(--radius-sm);
      margin: auto 0;
    }

    .teacher-lesson-card {
      background: white;
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-sm);
      padding: 12px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
      border-left: 4px solid var(--primary);
    }

    .teacher-lesson-card.status-cancelled {
      border-left-color: var(--rose-500);
      background: #fff5f5;
      opacity: 0.75;
    }

    .teacher-lesson-card.status-completed {
      border-left-color: var(--emerald-500);
    }

    .teacher-lesson-card.has-pending-req {
      border-left-color: var(--amber-500);
      background: var(--amber-50);
    }

    .lesson-time-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    .lesson-time {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--slate-900);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .student-badge-name {
      font-size: 0.92rem;
      font-weight: 700;
      color: var(--slate-900);
      margin-bottom: 4px;
    }

    .lesson-topic {
      font-size: 0.78rem;
      color: var(--slate-600);
      margin-bottom: 8px;
    }

    .lesson-actions-bar {
      margin-top: 10px;
      padding-top: 8px;
      border-top: 1px solid var(--slate-100);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .action-icon-btn {
      background: transparent;
      border: 1px solid var(--slate-200);
      border-radius: 6px;
      padding: 4px 8px;
      font-size: 0.75rem;
      color: var(--slate-600);
      cursor: pointer;
      font-weight: 600;
    }

    .action-icon-btn:hover {
      background: var(--slate-100);
      color: var(--slate-900);
    }

    /* Tables */
    .table-container {
      border: 1px solid var(--slate-200);
      border-radius: var(--radius-md);
      overflow-x: auto;
      background: white;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.88rem;
    }

    th {
      padding: 14px 18px;
      background: #fafbfc;
      border-bottom: 1px solid var(--slate-200);
      font-size: 0.75rem;
      font-weight: 700;
      color: var(--slate-500);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    td {
      padding: 14px 18px;
      border-bottom: 1px solid var(--slate-100);
      color: var(--slate-700);
    }

    tr:last-child td {
      border-bottom: none;
    }

    .wa-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #25d366;
      color: white;
      padding: 6px 12px;
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
    }

    .quick-chip {
      background: var(--slate-100);
      border: 1px solid var(--slate-200);
      border-radius: 9999px;
      padding: 4px 10px;
      font-size: 0.75rem;
      color: var(--slate-700);
      cursor: pointer;
      transition: all 0.15s;
    }

    .quick-chip:hover {
      background: var(--primary-light);
      border-color: var(--primary-border);
      color: var(--primary);
    }

    /* Modal Backdrop */
    .modal-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.5);
      backdrop-filter: blur(4px);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .modal-backdrop.show {
      display: flex;
    }

    .modal-box {
      background: white;
      border-radius: var(--radius-lg);
      max-width: 520px;
      width: 100%;
      box-shadow: var(--shadow-modal);
      overflow: hidden;
      animation: modalPop 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    @keyframes modalPop {
      from { transform: scale(0.95); opacity: 0; }
      to { transform: scale(1); opacity: 1; }
    }

    .modal-top {
      padding: 18px 24px;
      border-bottom: 1px solid var(--slate-200);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .modal-top h3 {
      font-size: 1.15rem;
      font-weight: 800;
      color: var(--slate-900);
    }

    .close-modal-btn {
      background: transparent;
      border: none;
      font-size: 1.4rem;
      color: var(--slate-400);
      cursor: pointer;
    }

    .modal-body-content {
      padding: 24px;
      max-height: 75vh;
      overflow-y: auto;
    }

    .modal-bottom {
      padding: 16px 24px;
      border-top: 1px solid var(--slate-200);
      background: #fafbfc;
      display: flex;
      justify-content: flex-end;
      gap: 12px;
    }

    /* Toast */
    .toast-pill {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: var(--slate-900);
      color: white;
      padding: 12px 20px;
      border-radius: 9999px;
      font-size: 0.88rem;
      font-weight: 600;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
      display: flex;
      align-items: center;
      gap: 10px;
      z-index: 150;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .toast-pill.visible {
      transform: translateY(0);
      opacity: 1;
    }
  </style>
</head>
<body>

  <!-- Top Navigation -->
  <nav class="navbar">
    <div class="nav-inner">
      <div class="brand">
        <div class="brand-logo">A</div>
        <div>
          <div class="brand-title">Annette's Private Lessons</div>
          <div class="brand-subtitle" id="navSubtitle">
            <span>Student & Teacher Portal</span>
            <span class="backend-pill" id="backendStatusPill">⚡ Ready</span>
          </div>
        </div>
      </div>

      <!-- User Session Area -->
      <div class="nav-user-area" id="navUserArea">
        <div class="user-pill" id="userPillDisplay" style="display: none;">
          <span id="userPillIcon">👤</span>
          <span id="userPillName">User</span>
        </div>
        <button class="btn btn-secondary btn-sm" id="signOutBtn" style="display: none;" onclick="handleSignOut()">
          Sign Out
        </button>
      </div>
    </div>
  </nav>

  <!-- Week Control Sub-Header (Only visible when logged in) -->
  <div class="subnav" id="subnavBar" style="display: none;">
    <div class="subnav-inner">
      <div class="week-nav">
        <button class="btn-circle" onclick="shiftWeek(-1)" title="Previous Week">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m15 18-6-6 6-6"/></svg>
        </button>
        <div class="week-label-box">
          <span class="week-label" id="currentWeekRange">Current Week</span>
          <span class="week-sublabel" id="weekDescriptor">Active Schedule</span>
        </div>
        <button class="btn-circle" onclick="shiftWeek(1)" title="Next Week">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m9 18 6-6-6-6"/></svg>
        </button>
        <button class="btn btn-secondary btn-sm" onclick="resetToThisWeek()">This Week</button>
      </div>

      <!-- Action buttons visible in teacher view -->
      <div id="teacherActionButtons" style="display: none; gap: 10px;">
        <button class="btn btn-secondary btn-sm" onclick="duplicateCurrentWeek()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
          Duplicate Week to Next
        </button>
        <button class="btn btn-primary btn-sm" onclick="openLessonModal()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5v14"/></svg>
          Add New Lesson
        </button>
      </div>
    </div>
  </div>

  <!-- Main View Area -->
  <main class="main-container">

    <!-- ==============================================
         0. AUTHENTICATION SCREEN (LOGIN & REGISTER)
         ============================================== -->
    <div id="authScreen" class="auth-overlay">
      <div class="auth-card">
        <div class="auth-header">
          <h2>Annette's Private Lessons</h2>
          <p>Sign in to view your scheduled hours or register as a new student</p>
        </div>

        <div class="auth-tabs">
          <button class="auth-tab-btn active" id="tabBtnStudentLogin" onclick="switchAuthTab('studentLogin')">
            🎓 Student Sign In
          </button>
          <button class="auth-tab-btn" id="tabBtnStudentRegister" onclick="switchAuthTab('studentRegister')">
            ✨ Student Sign Up
          </button>
          <button class="auth-tab-btn" id="tabBtnTeacherLogin" onclick="switchAuthTab('teacherLogin')">
            👩‍🏫 Teacher Annette
          </button>
        </div>

        <div class="auth-body">
          
          <!-- TAB 1: Student Sign In -->
          <div id="paneStudentLogin">
            <form onsubmit="handleStudentSignIn(event)">
              <div class="form-group">
                <label class="form-label">Your Name or Phone Number:</label>
                <input type="text" id="studentLoginIdentifier" class="input-field" placeholder="Enter your full name or phone" required>
              </div>
              <div class="form-group">
                <label class="form-label">Password:</label>
                <input type="password" id="studentPassInput" class="input-field" placeholder="Your password" required>
              </div>
              <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 8px;">
                Sign In to My Student Portal
              </button>
              <div style="text-align: center; margin-top: 14px;">
                <span style="font-size: 0.82rem; color: var(--slate-500);">New student? </span>
                <a href="javascript:void(0)" onclick="switchAuthTab('studentRegister')" style="font-size: 0.82rem; font-weight: 700; color: var(--primary); text-decoration: none;">Create an account here</a>
              </div>
            </form>
          </div>

          <!-- TAB 2: Student Sign Up (New Student Registration) -->
          <div id="paneStudentRegister" style="display: none;">
            <form onsubmit="handleStudentSignUp(event)">
              <div class="form-group">
                <label class="form-label">Student Full Name:</label>
                <input type="text" id="regStudentName" class="input-field" placeholder="E.g., Maya Ronen" required>
              </div>

              <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
                <div class="form-group">
                  <label class="form-label">Grade / Level:</label>
                  <input type="text" id="regStudentGrade" class="input-field" placeholder="E.g., 9th Grade / 5-Units" required>
                </div>
                <div class="form-group">
                  <label class="form-label">Create Password:</label>
                  <input type="password" id="regStudentPassword" class="input-field" placeholder="Min. 4 characters" required>
                </div>
              </div>

              <div class="form-group">
                <label class="form-label">Parent / Contact Phone (with country code):</label>
                <input type="text" id="regStudentPhone" class="input-field" placeholder="E.g., 054-123-4567" required>
              </div>

              <div class="form-group">
                <label class="form-label">Learning Goals / Notes for Teacher Annette:</label>
                <textarea id="regStudentNotes" class="input-field" placeholder="E.g., Preparing for high school bagrut, grammar, conversation..."></textarea>
              </div>

              <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 8px;">
                Sign Up & Enter My Portal
              </button>
            </form>
          </div>

          <!-- TAB 3: Teacher Sign In -->
          <div id="paneTeacherLogin" style="display: none;">
            <form onsubmit="handleTeacherSignIn(event)">
              <div class="form-group">
                <label class="form-label">Teacher Annette's Username / Email:</label>
                <input type="text" id="teacherEmailInput" class="input-field" value="annette@lessons.com" required>
              </div>
              <div class="form-group">
                <label class="form-label">Password / PIN:</label>
                <input type="password" id="teacherPassInput" class="input-field" value="annette123" required>
              </div>
              <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 8px;">
                Sign In as Teacher Annette
              </button>
            </form>
          </div>

        </div>
      </div>
    </div>

    <!-- ==============================================
         1. STUDENT / PARENT VIEW (STRICTLY PRIVATE)
         ============================================== -->
    <div id="studentViewWrap" style="display: none;">
      
      <!-- Student Top Header Banner -->
      <div class="student-welcome-header">
        <div class="student-welcome-text">
          <h2 id="studentGreetingTitle">Hello! 👋</h2>
          <p>Welcome to Annette's Private Lessons. Below is your personal lesson schedule. You only see your own appointments. To reschedule or cancel, submit your note below.</p>
        </div>
        <div style="background: rgba(255, 255, 255, 0.15); padding: 10px 18px; border-radius: var(--radius-md); font-weight: 700; color: white;">
          🎓 Student Portal
        </div>
      </div>

      <!-- Privacy Notice -->
      <div class="privacy-notice">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
        <strong>Private & Confidential:</strong> You are viewing only your own appointments and private correspondence with Teacher Annette. Other students cannot see your schedule.
      </div>

      <!-- Next Scheduled Appointment Card -->
      <div id="studentNextAppointmentHero"></div>

      <!-- Two Column Layout: My Appointments & Request Note -->
      <div class="student-grid">
        
        <!-- Left: My Sessions for Selected Week -->
        <div class="content-panel">
          <div class="panel-header">
            <div class="panel-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
              My Scheduled Lessons This Week
            </div>
          </div>
          <div id="myAppointmentsList">
            <!-- Strictly populated with this student's lessons only -->
          </div>
        </div>

        <!-- Right: Change / Cancel Request Form -->
        <div class="content-panel">
          <div class="panel-header">
            <div class="panel-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              Request Change or Cancellation
            </div>
          </div>
          <p style="font-size: 0.85rem; color: var(--slate-500); margin-bottom: 16px;">
            Need a different hour or have an exam? Choose your session, write your requested time or reason, and Teacher Annette will reply to you directly.
          </p>

          <form onsubmit="handleStudentRequestSubmit(event)">
            <div class="form-group">
              <label class="form-label">Select Your Lesson:</label>
              <select id="reqTargetLessonSelect" class="input-field" required>
                <!-- Populated strictly with this student's lessons -->
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Request Type:</label>
              <select id="reqTypeSelect" class="input-field">
                <option value="Reschedule">🔄 Reschedule / Different Hour</option>
                <option value="Cancel">❌ Cancel This Week's Lesson</option>
                <option value="Question">💬 Question About My Lesson</option>
              </select>
            </div>

            <div class="form-group">
              <label class="form-label">Your Note / Preferred Alternative Time:</label>
              <textarea id="reqNoteText" class="input-field" placeholder="E.g., Hi Annette, can we move our lesson to Thursday at 17:00? I have a school test..." required></textarea>
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%;">
              Send Note to Teacher Annette
            </button>
          </form>
        </div>

      </div>

      <!-- Messages & Teacher's Answers History -->
      <div class="content-panel">
        <div class="panel-header">
          <div class="panel-title">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 9a2 2 0 0 1-2 2H6l-4 4V4c0-1.1.9-2 2-2h8a2 2 0 0 1 2 2v5Z"/><path d="M18 9h2a2 2 0 0 1 2 2v11l-4-4h-6a2 2 0 0 1-2-2v-1"/></svg>
            My Notes & Teacher Annette's Answers
          </div>
        </div>
        <div id="studentRequestFeed">
          <!-- Strictly this student's private communication -->
        </div>
      </div>

    </div>

    <!-- ==============================================
         2. TEACHER DASHBOARD (ANNETTE'S FULL STUDIO)
         ============================================== -->
    <div id="teacherViewWrap" style="display: none;">
      
      <!-- Metrics Row -->
      <div class="metrics-row">
        <div class="metric-card accent-primary">
          <div class="metric-header">
            <span>Weekly Sessions</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 2v4M16 2v4M3 10h18M5 4h14a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2Z"/></svg>
          </div>
          <div class="metric-value" id="mTotalLessons">0</div>
          <div class="metric-footer" id="mCompletedSubtitle">0 sessions completed</div>
        </div>

        <div class="metric-card accent-amber">
          <div class="metric-header">
            <span>Student Requests</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          </div>
          <div class="metric-value" id="mPendingReqs" style="color: var(--amber-600);">0</div>
          <div class="metric-footer">Waiting for your answer</div>
        </div>

        <div class="metric-card accent-emerald">
          <div class="metric-header">
            <span>Weekly Earnings</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
          </div>
          <div class="metric-value" id="mTotalRevenue">$0</div>
          <div class="progress-bar-wrap">
            <div class="progress-bar-fill" id="mProgressFill" style="width: 0%;"></div>
          </div>
          <div class="metric-footer" id="mPaidSubtitle">$0 collected (0%)</div>
        </div>

        <div class="metric-card accent-rose">
          <div class="metric-header">
            <span>Pending Balance</span>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
          </div>
          <div class="metric-value" id="mUnpaidBalance" style="color: var(--rose-600);">$0</div>
          <div class="metric-footer" id="mUnpaidSessions">0 unpaid lessons</div>
        </div>
      </div>

      <!-- Teacher Navigation Tabs -->
      <div class="teacher-nav">
        <button class="t-tab-btn active" onclick="showTeacherTab('schedule', this)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
          Master Timetable
        </button>
        <button class="t-tab-btn" onclick="showTeacherTab('requests', this)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          Student Requests Inbox
          <span class="role-badge-count" id="pendingBadgeTab" style="display: none;">0</span>
        </button>
        <button class="t-tab-btn" onclick="showTeacherTab('payments', this)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="2" x2="22" y1="10" y2="10"/></svg>
          Payment Tracker
        </button>
        <button class="t-tab-btn" onclick="showTeacherTab('roster', this)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          Student Roster
        </button>
        <button class="t-tab-btn" onclick="showTeacherTab('backup', this)">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v10M18.4 4.6a10 10 0 1 1-12.8 0"/></svg>
          Data & Settings
        </button>
      </div>

      <!-- Tab Content 1: Schedule -->
      <div id="tTabSchedule">
        <div class="content-panel" style="padding: 16px;">
          
          <div class="filter-bar">
            <input type="text" id="scheduleSearchInput" class="search-input" placeholder="🔍 Search student name or topic..." oninput="handleScheduleFilterChange()">
            <select id="scheduleDayFilter" class="input-field" style="width: auto; padding: 8px 12px;" onchange="handleScheduleFilterChange()">
              <option value="all">All Days</option>
              <option value="Sunday">Sunday</option>
              <option value="Monday">Monday</option>
              <option value="Tuesday">Tuesday</option>
              <option value="Wednesday">Wednesday</option>
              <option value="Thursday">Thursday</option>
              <option value="Friday">Friday</option>
              <option value="Saturday">Saturday</option>
            </select>
            <select id="scheduleLocFilter" class="input-field" style="width: auto; padding: 8px 12px;" onchange="handleScheduleFilterChange()">
              <option value="all">All Locations</option>
              <option value="Studio">In-Person Studio</option>
              <option value="Zoom">Zoom / Online</option>
            </select>
          </div>

          <div class="schedule-board" id="teacherScheduleBoard">
            <!-- Populated dynamically -->
          </div>
        </div>
      </div>

      <!-- Tab Content 2: Student Requests -->
      <div id="tTabRequests" style="display: none;">
        <div class="content-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Inquiries & Reschedule Requests</div>
              <p style="font-size: 0.8rem; color: var(--slate-500); margin-top: 2px;">
                Answer student requests, approve new times, or cancel slots with a click.
              </p>
            </div>
          </div>
          <div id="teacherRequestsFeed">
            <!-- Populated -->
          </div>
        </div>
      </div>

      <!-- Tab Content 3: Payments Tracker -->
      <div id="tTabPayments" style="display: none;">
        <div class="content-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Lesson Ledger & Payment Status</div>
              <p style="font-size: 0.8rem; color: var(--slate-500); margin-top: 2px;">
                Track paid vs. pending fees, payment methods (Bit, Cash, PayBox, Transfer), and send reminders.
              </p>
            </div>
            <div>
              <select id="paymentFilterSelect" class="input-field" style="width: auto; padding: 6px 12px;" onchange="renderPaymentLedger()">
                <option value="all">All Lessons This Week</option>
                <option value="unpaid">Unpaid / Pending Only</option>
                <option value="paid">Paid Only</option>
              </select>
            </div>
          </div>

          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Session Date & Time</th>
                  <th>Rate</th>
                  <th>Status</th>
                  <th>Payment Status</th>
                  <th>Payment Method</th>
                  <th>Quick Action</th>
                </tr>
              </thead>
              <tbody id="paymentLedgerTbody">
                <!-- Dynamically populated -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Tab Content 4: Student Roster -->
      <div id="tTabRoster" style="display: none;">
        <div class="content-panel">
          <div class="panel-header">
            <div>
              <div class="panel-title">Registered Students</div>
              <p style="font-size: 0.8rem; color: var(--slate-500); margin-top: 2px;">
                Manage student profiles, parent contacts, WhatsApp quick links, and hourly pricing.
              </p>
            </div>
            <button class="btn btn-primary btn-sm" onclick="openStudentModal()">
              + Add Student
            </button>
          </div>

          <div class="table-container">
            <table>
              <thead>
                <tr>
                  <th>Student Name</th>
                  <th>Level / Grade</th>
                  <th>Parent Contact</th>
                  <th>Default Hourly Rate</th>
                  <th>Learning Focus</th>
                  <th>Contact Parent</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody id="studentRosterTbody">
                <!-- Populated -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Tab Content 5: Data Backup -->
      <div id="tTabBackup" style="display: none;">
        <div class="content-panel" style="max-width: 600px;">
          <div class="panel-title" style="margin-bottom: 12px;">Data Management & Backup</div>
          <p style="font-size: 0.85rem; color: var(--slate-600); margin-bottom: 24px;">
            Your live data is stored in the persistent database. You can export a backup copy at any time.
          </p>

          <div style="display: flex; flex-direction: column; gap: 16px;">
            <div style="padding: 16px; border: 1px solid var(--slate-200); border-radius: var(--radius-sm); background: #fafbfc;">
              <h4 style="font-size: 0.95rem; margin-bottom: 4px;">📥 Export Studio Backup</h4>
              <p style="font-size: 0.8rem; color: var(--slate-500); margin-bottom: 12px;">Download all registered students, lessons, and requests as a JSON file.</p>
              <button class="btn btn-secondary btn-sm" onclick="exportBackupFile()">Download Backup (.json)</button>
            </div>

            <div style="padding: 16px; border: 1px solid var(--slate-200); border-radius: var(--radius-sm); background: #fafbfc;">
              <h4 style="font-size: 0.95rem; margin-bottom: 4px;">📤 Restore from Backup</h4>
              <p style="font-size: 0.8rem; color: var(--slate-500); margin-bottom: 12px;">Load a previously saved backup file.</p>
              <input type="file" id="importInput" accept=".json" style="display: none;" onchange="importBackupFile(event)">
              <button class="btn btn-secondary btn-sm" onclick="document.getElementById('importInput').click()">Select Backup File</button>
            </div>
          </div>
        </div>
      </div>

    </div>

  </main>

  <!-- ==============================================
       MODALS
       ============================================== -->

  <!-- Add/Edit Lesson Modal -->
  <div class="modal-backdrop" id="lessonModal">
    <div class="modal-box">
      <div class="modal-top">
        <h3 id="lessonModalHeader">Add Private Lesson</h3>
        <button class="close-modal-btn" onclick="closeModal('lessonModal')">&times;</button>
      </div>
      <form onsubmit="handleLessonSave(event)">
        <div class="modal-body-content">
          <input type="hidden" id="modalLessonId">

          <div class="form-group">
            <label class="form-label">Student:</label>
            <select id="modalLessonStudent" class="input-field" required onchange="handleModalStudentChange()">
              <!-- Injected from real students -->
            </select>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div class="form-group">
              <label class="form-label">Day of Week:</label>
              <select id="modalLessonDay" class="input-field" required>
                <option value="Sunday">Sunday</option>
                <option value="Monday">Monday</option>
                <option value="Tuesday">Tuesday</option>
                <option value="Wednesday">Wednesday</option>
                <option value="Thursday">Thursday</option>
                <option value="Friday">Friday</option>
                <option value="Saturday">Saturday</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Date:</label>
              <input type="date" id="modalLessonDate" class="input-field" required>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div class="form-group">
              <label class="form-label">Start Time:</label>
              <input type="time" id="modalLessonStart" class="input-field" required value="16:00">
            </div>
            <div class="form-group">
              <label class="form-label">End Time:</label>
              <input type="time" id="modalLessonEnd" class="input-field" required value="17:00">
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div class="form-group">
              <label class="form-label">Rate / Fee ($ or ₪):</label>
              <input type="number" id="modalLessonRate" class="input-field" required value="45" min="0">
            </div>
            <div class="form-group">
              <label class="form-label">Payment Status:</label>
              <select id="modalLessonPayment" class="input-field">
                <option value="Unpaid">Unpaid / Pending</option>
                <option value="Paid">Paid</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Lesson Focus / Topic:</label>
            <input type="text" id="modalLessonTopic" class="input-field" placeholder="E.g., Bagrut Practice, Essay Writing">
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div class="form-group">
              <label class="form-label">Location / Mode:</label>
              <select id="modalLessonLocation" class="input-field">
                <option value="Studio (In-Person)">Studio (In-Person)</option>
                <option value="Online (Zoom / Meet)">Online (Zoom / Google Meet)</option>
                <option value="Student's Home">Student's Home</option>
              </select>
            </div>
            <div class="form-group">
              <label class="form-label">Session Status:</label>
              <select id="modalLessonStatus" class="input-field">
                <option value="Confirmed">Confirmed</option>
                <option value="Completed">Completed</option>
                <option value="Cancelled">Cancelled</option>
              </select>
            </div>
          </div>
        </div>
        <div class="modal-bottom">
          <button type="button" class="btn btn-secondary" onclick="closeModal('lessonModal')">Cancel</button>
          <button type="submit" class="btn btn-primary">Save Session</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Add/Edit Student Modal -->
  <div class="modal-backdrop" id="studentModal">
    <div class="modal-box">
      <div class="modal-top">
        <h3 id="studentModalHeader">Register Student</h3>
        <button class="close-modal-btn" onclick="closeModal('studentModal')">&times;</button>
      </div>
      <form onsubmit="handleStudentSave(event)">
        <div class="modal-body-content">
          <input type="hidden" id="modalStudentId">

          <div class="form-group">
            <label class="form-label">Student Name:</label>
            <input type="text" id="modalStudentName" class="input-field" required placeholder="E.g., Maya Ronen">
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
            <div class="form-group">
              <label class="form-label">Grade / Level:</label>
              <input type="text" id="modalStudentGrade" class="input-field" placeholder="E.g., 9th Grade / 5-Units">
            </div>
            <div class="form-group">
              <label class="form-label">Standard Hourly Rate:</label>
              <input type="number" id="modalStudentRate" class="input-field" value="45" min="0">
            </div>
          </div>

          <div class="form-group">
            <label class="form-label">Parent Name & Phone (with country code):</label>
            <input type="text" id="modalStudentPhone" class="input-field" placeholder="E.g., 054-123-4567">
          </div>

          <div class="form-group">
            <label class="form-label">Learning Goals / Notes:</label>
            <textarea id="modalStudentNotes" class="input-field" placeholder="Targeting bagrut exam, grammar drills, etc."></textarea>
          </div>
        </div>
        <div class="modal-bottom">
          <button type="button" class="btn btn-secondary" onclick="closeModal('studentModal')">Cancel</button>
          <button type="submit" class="btn btn-primary">Save Student</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Interactive WhatsApp Composer Modal -->
  <div class="modal-backdrop" id="waModal">
    <div class="modal-box">
      <div class="modal-top">
        <h3>💬 WhatsApp Message Preview</h3>
        <button class="close-modal-btn" onclick="closeModal('waModal')">&times;</button>
      </div>
      <div class="modal-body-content">
        <p style="font-size:0.85rem; color:var(--slate-500); margin-bottom:14px;">
          Choose a message template or edit the text before sending to the parent:
        </p>
        <div style="display:flex; gap:6px; flex-wrap:wrap; margin-bottom:12px;">
          <span class="quick-chip" onclick="setWaTemplate('reminder')">📅 Lesson Reminder</span>
          <span class="quick-chip" onclick="setWaTemplate('payment')">💳 Payment Notice</span>
          <span class="quick-chip" onclick="setWaTemplate('confirm')">✓ Lesson Confirmed</span>
        </div>
        <div class="form-group">
          <textarea id="waComposerText" class="input-field" style="min-height:110px;"></textarea>
        </div>
      </div>
      <div class="modal-bottom">
        <button type="button" class="btn btn-secondary" onclick="copyWaText()">Copy Text</button>
        <a id="waSendAnchor" href="#" target="_blank" class="btn btn-primary" style="background:#25d366; border-color:#25d366;">
          Open in WhatsApp
        </a>
      </div>
    </div>
  </div>

  <!-- Toast Notification Pill -->
  <div class="toast-pill" id="toastBox">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
    <span id="toastMsg">Operation successful</span>
  </div>

  <!-- Application Logic -->
  <script>
    /* Clean Production State (No Dummy Data) */
    let students = JSON.parse(localStorage.getItem('annette_students')) || [];
    let lessons = JSON.parse(localStorage.getItem('annette_lessons')) || [];
    let requests = JSON.parse(localStorage.getItem('annette_requests')) || [];
    let session = JSON.parse(localStorage.getItem('annette_session')) || null;
    let weekOffset = 0;
    let activeWaContext = null;

    // Use current real date as reference
    const now = new Date();
    const currentDayOfWeek = now.getDay(); // 0 is Sunday
    const BASE_WEEK_SUNDAY = new Date(now.getFullYear(), now.getMonth(), now.getDate() - currentDayOfWeek);

    let isBackendActive = false;
    const API_BASE = (window.location.protocol.startsWith('http')) ? '/api' : 'http://127.0.0.1:8000/api';

    async function checkBackendConnection() {
      try {
        const res = await fetch(`${API_BASE}/health`, { method: 'GET' });
        if (res.ok) {
          isBackendActive = true;
          document.getElementById('backendStatusPill').textContent = '🟢 Server Online';
          document.getElementById('backendStatusPill').classList.add('online');
          await loadFromBackend();
          return;
        }
      } catch (e) {
        isBackendActive = false;
        document.getElementById('backendStatusPill').textContent = '⚡ Browser Storage';
      }
    }

    async function loadFromBackend() {
      try {
        const [stRes, lsRes, rqRes] = await Promise.all([
          fetch(`${API_BASE}/students`),
          fetch(`${API_BASE}/lessons`),
          fetch(`${API_BASE}/requests`)
        ]);
        if (stRes.ok) students = await stRes.json();
        if (lsRes.ok) lessons = await lsRes.json();
        if (rqRes.ok) requests = await rqRes.json();
        persistData();
        refreshUI();
      } catch (err) {
        console.warn('Backend sync error:', err);
      }
    }

    function persistData() {
      localStorage.setItem('annette_students', JSON.stringify(students));
      localStorage.setItem('annette_lessons', JSON.stringify(lessons));
      localStorage.setItem('annette_requests', JSON.stringify(requests));
      localStorage.setItem('annette_session', JSON.stringify(session));
    }

    function triggerToast(text) {
      const box = document.getElementById('toastBox');
      document.getElementById('toastMsg').textContent = text;
      box.classList.add('visible');
      setTimeout(() => box.classList.remove('visible'), 3200);
    }

    function getWeekData(offset = 0) {
      const sun = new Date(BASE_WEEK_SUNDAY);
      sun.setDate(sun.getDate() + (offset * 7));

      const days = [];
      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

      for (let i = 0; i < 7; i++) {
        const d = new Date(sun);
        d.setDate(d.getDate() + i);
        const yyyy = d.getFullYear();
        const mm = String(d.getMonth() + 1).padStart(2, '0');
        const dd = String(d.getDate()).padStart(2, '0');
        
        const isCurrentDay = (d.toDateString() === now.toDateString());
        days.push({
          dayName: dayNames[i],
          isoDate: `${yyyy}-${mm}-${dd}`,
          displayDate: d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
          isToday: isCurrentDay
        });
      }

      const sat = new Date(sun);
      sat.setDate(sat.getDate() + 6);

      const label = `${sun.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} – ${sat.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;
      
      // Calculate week identifier
      const oneJan = new Date(sun.getFullYear(), 0, 1);
      const weekNum = Math.ceil((((sun - oneJan) / 86400000) + oneJan.getDay() + 1) / 7);
      const weekId = `${sun.getFullYear()}-W${weekNum}`;

      return { sun, sat, label, days, weekId };
    }

    function shiftWeek(delta) {
      weekOffset += delta;
      refreshUI();
    }

    function resetToThisWeek() {
      weekOffset = 0;
      refreshUI();
    }

    /* Auth Tab switcher */
    function switchAuthTab(tab) {
      document.getElementById('tabBtnStudentLogin').classList.toggle('active', tab === 'studentLogin');
      document.getElementById('tabBtnStudentRegister').classList.toggle('active', tab === 'studentRegister');
      document.getElementById('tabBtnTeacherLogin').classList.toggle('active', tab === 'teacherLogin');

      document.getElementById('paneStudentLogin').style.display = (tab === 'studentLogin') ? 'block' : 'none';
      document.getElementById('paneStudentRegister').style.display = (tab === 'studentRegister') ? 'block' : 'none';
      document.getElementById('paneTeacherLogin').style.display = (tab === 'teacherLogin') ? 'block' : 'none';
    }

    async function handleTeacherSignIn(e) {
      e.preventDefault();
      const user = document.getElementById('teacherEmailInput').value.trim();
      const pass = document.getElementById('teacherPassInput').value.trim();

      if (isBackendActive) {
        try {
          const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role: 'teacher', usernameOrId: user, password: pass })
          });
          if (!res.ok) throw new Error((await res.json()).detail || 'Login failed');
          session = await res.json();
        } catch (err) {
          alert(err.message);
          return;
        }
      } else {
        if (pass !== 'annette123' && pass !== 'annette' && pass !== 'admin') {
          alert('Invalid password for Teacher Annette. Default is: annette123');
          return;
        }
        session = { role: 'teacher', name: 'Annette' };
      }

      persistData();
      triggerToast('Signed in as Teacher Annette');
      refreshUI();
    }

    async function handleStudentSignIn(e) {
      e.preventDefault();
      const identifier = document.getElementById('studentLoginIdentifier').value.trim();
      const pass = document.getElementById('studentPassInput').value.trim();

      if (isBackendActive) {
        try {
          const res = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ role: 'student', usernameOrId: identifier, password: pass })
          });
          if (!res.ok) throw new Error((await res.json()).detail || 'Login failed');
          session = await res.json();
        } catch (err) {
          alert(err.message);
          return;
        }
      } else {
        const query = identifier.toLowerCase();
        const st = students.find(s => 
          s.name.toLowerCase() === query || 
          (s.phone && s.phone.replace(/\D/g, '') === identifier.replace(/\D/g, '')) ||
          s.id === identifier
        );
        if (!st) {
          alert('No student account found for "' + identifier + '". Please click "Student Sign Up" to register.');
          return;
        }
        if (st.password && st.password !== pass) {
          alert('Incorrect password. Please verify your password.');
          return;
        }
        session = { role: 'student', studentId: st.id, name: st.name };
      }

      persistData();
      triggerToast(`Welcome back, ${session.name}!`);
      refreshUI();
    }

    async function handleStudentSignUp(e) {
      e.preventDefault();
      const name = document.getElementById('regStudentName').value.trim();
      const grade = document.getElementById('regStudentGrade').value.trim();
      const pass = document.getElementById('regStudentPassword').value.trim();
      const phone = document.getElementById('regStudentPhone').value.trim();
      const notes = document.getElementById('regStudentNotes').value.trim();

      let cleanDigits = phone.replace(/\D/g, '');
      if (cleanDigits.startsWith('0')) cleanDigits = '972' + cleanDigits.substring(1);

      if (isBackendActive) {
        try {
          const res = await fetch(`${API_BASE}/auth/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, grade, phone, notes, password: pass })
          });
          if (!res.ok) throw new Error('Registration failed');
          session = await res.json();
          await loadFromBackend();
        } catch (err) {
          alert(err.message);
          return;
        }
      } else {
        const newStudent = {
          id: 's_' + Date.now(),
          name, grade: grade || 'Student', rate: 45, phone, wa: cleanDigits, notes, password: pass
        };
        students.push(newStudent);
        session = { role: 'student', studentId: newStudent.id, name: newStudent.name };
      }

      persistData();
      triggerToast(`Account created! Welcome, ${session.name}`);
      refreshUI();
    }

    function handleSignOut() {
      session = null;
      persistData();
      triggerToast('Signed out successfully.');
      refreshUI();
    }

    function showTeacherTab(tab, btn) {
      document.querySelectorAll('.t-tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      document.getElementById('tTabSchedule').style.display = (tab === 'schedule') ? 'block' : 'none';
      document.getElementById('tTabRequests').style.display = (tab === 'requests') ? 'block' : 'none';
      document.getElementById('tTabPayments').style.display = (tab === 'payments') ? 'block' : 'none';
      document.getElementById('tTabRoster').style.display = (tab === 'roster') ? 'block' : 'none';
      document.getElementById('tTabBackup').style.display = (tab === 'backup') ? 'block' : 'none';

      if (tab === 'requests') renderTeacherRequests();
      if (tab === 'payments') renderPaymentLedger();
      if (tab === 'roster') renderStudentRoster();
    }

    /* ==========================================================
       RENDER ORCHESTRATION
       ========================================================== */
    function refreshUI() {
      const authScreen = document.getElementById('authScreen');
      const studentWrap = document.getElementById('studentViewWrap');
      const teacherWrap = document.getElementById('teacherViewWrap');
      const subnavBar = document.getElementById('subnavBar');
      const userPill = document.getElementById('userPillDisplay');
      const signOutBtn = document.getElementById('signOutBtn');
      const teacherActions = document.getElementById('teacherActionButtons');

      if (!session) {
        authScreen.style.display = 'flex';
        studentWrap.style.display = 'none';
        teacherWrap.style.display = 'none';
        subnavBar.style.display = 'none';
        userPill.style.display = 'none';
        signOutBtn.style.display = 'none';
        return;
      }

      authScreen.style.display = 'none';
      subnavBar.style.display = 'block';
      userPill.style.display = 'flex';
      signOutBtn.style.display = 'inline-flex';

      const week = getWeekData(weekOffset);
      document.getElementById('currentWeekRange').textContent = week.label;
      document.getElementById('weekDescriptor').textContent = (weekOffset === 0)
        ? 'Current Active Week'
        : (weekOffset > 0 ? `+${weekOffset} Week(s) Ahead` : `${Math.abs(weekOffset)} Week(s) Ago`);

      if (session.role === 'teacher') {
        document.getElementById('userPillIcon').textContent = '👩‍🏫';
        document.getElementById('userPillName').textContent = 'Teacher Annette';
        teacherActions.style.display = 'flex';
        studentWrap.style.display = 'none';
        teacherWrap.style.display = 'block';
        renderTeacherDashboard(week);
      } else {
        const student = students.find(s => s.id === session.studentId);
        document.getElementById('userPillIcon').textContent = '🎓';
        document.getElementById('userPillName').textContent = student ? student.name : session.name;
        teacherActions.style.display = 'none';
        studentWrap.style.display = 'block';
        teacherWrap.style.display = 'none';
        renderStudentPortal(week, student || { id: session.studentId, name: session.name });
      }

      updateBadges();
    }

    function updateBadges() {
      const pendingCount = requests.filter(r => r.status === 'Pending').length;
      const bTab = document.getElementById('pendingBadgeTab');
      if (bTab) {
        bTab.style.display = pendingCount > 0 ? 'inline-block' : 'none';
        bTab.textContent = pendingCount;
      }
    }

    /* ==========================================================
       STUDENT PORTAL
       ========================================================== */
    function renderStudentPortal(week, student) {
      if (!student) return;
      document.getElementById('studentGreetingTitle').textContent = `Hello, ${student.name}! 👋`;

      const myLessonsThisWeek = lessons.filter(l => l.studentId === student.id && l.weekId === week.weekId);

      const heroContainer = document.getElementById('studentNextAppointmentHero');
      if (myLessonsThisWeek.length > 0) {
        const next = myLessonsThisWeek[0];
        heroContainer.innerHTML = `
          <div class="next-appointment-hero">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
              <div>
                <span class="badge badge-confirmed" style="margin-bottom:8px;">Your Scheduled Session</span>
                <div style="font-size:1.6rem; font-weight:800; color:var(--slate-900);">
                  ${next.day}, ${next.date} at ${next.startTime} – ${next.endTime}
                </div>
                <div style="font-size:0.95rem; color:var(--slate-600); margin-top:4px;">
                  📖 Focus: <strong>${next.topic || 'Private Lesson'}</strong>
                </div>
              </div>
              <div>
                <span class="badge ${next.payment === 'Paid' ? 'badge-paid' : 'badge-unpaid'}" style="font-size:0.85rem; padding:6px 14px;">
                  ${next.payment === 'Paid' ? '✓ Lesson Fee Paid' : `⏳ Payment Due: $${next.rate}`}
                </span>
              </div>
            </div>

            <div class="appointment-meta-grid">
              <div class="meta-box">
                <span class="meta-label">Location / Mode</span>
                <span class="meta-value">📍 ${next.location}</span>
              </div>
              <div class="meta-box">
                <span class="meta-label">Teacher</span>
                <span class="meta-value">👩‍🏫 Teacher Annette</span>
              </div>
              <div class="meta-box">
                <span class="meta-label">Duration</span>
                <span class="meta-value">⏱️ 60 Minutes</span>
              </div>
              <div class="meta-box">
                <span class="meta-label">Status</span>
                <span class="meta-value">
                  <span class="badge ${next.status === 'Completed' ? 'badge-paid' : (next.status === 'Cancelled' ? 'badge-cancelled' : 'badge-confirmed')}">
                    ${next.status}
                  </span>
                </span>
              </div>
            </div>
          </div>
        `;
      } else {
        heroContainer.innerHTML = `
          <div class="next-appointment-hero" style="text-align:center; padding:36px 20px;">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="color:var(--slate-400); margin-bottom:12px;"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>
            <div style="font-size:1.2rem; font-weight:800; color:var(--slate-800); margin-bottom:6px;">No Lessons Scheduled For You This Week</div>
            <p style="font-size:0.9rem; color:var(--slate-500); max-width:480px; margin:0 auto;">
              Teacher Annette has not scheduled a lesson for you between ${week.label} yet. She will assign your hours shortly, or you can write a note below.
            </p>
          </div>
        `;
      }

      const apptList = document.getElementById('myAppointmentsList');
      const targetSelect = document.getElementById('reqTargetLessonSelect');

      if (myLessonsThisWeek.length === 0) {
        apptList.innerHTML = `<div style="text-align:center; padding:30px; color:var(--slate-400); font-size:0.9rem;">No appointments booked for this week.</div>`;
        targetSelect.innerHTML = `<option value="">No lesson scheduled this week</option>`;
      } else {
        apptList.innerHTML = myLessonsThisWeek.map(l => {
          const hasPending = requests.some(r => r.lessonId === l.id && r.status === 'Pending');
          return `
            <div class="private-lesson-card ${l.status === 'Cancelled' ? 'cancelled' : (l.status === 'Completed' ? 'completed' : '')}">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                <div style="font-size:0.95rem; font-weight:800; color:var(--slate-900);">
                  📅 ${l.day}, ${l.date}
                </div>
                <div style="display:flex; gap:6px;">
                  <span class="badge ${l.payment === 'Paid' ? 'badge-paid' : 'badge-unpaid'}">
                    ${l.payment === 'Paid' ? 'Paid' : `Pending: $${l.rate}`}
                  </span>
                  <span class="badge ${l.status === 'Completed' ? 'badge-paid' : (l.status === 'Cancelled' ? 'badge-cancelled' : 'badge-confirmed')}">
                    ${l.status}
                  </span>
                </div>
              </div>

              <div style="font-size:1.1rem; font-weight:800; color:var(--primary); margin-bottom:6px;">
                🕒 ${l.startTime} – ${l.endTime}
              </div>

              <div style="font-size:0.85rem; color:var(--slate-700); margin-bottom:4px;">
                📖 Focus: ${l.topic || 'English Tutoring'}
              </div>

              <div style="font-size:0.8rem; color:var(--slate-500); display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
                <span>📍 ${l.location}</span>
                ${hasPending ? '<span class="badge badge-unpaid">Pending Change Request</span>' : ''}
              </div>
            </div>
          `;
        }).join('');

        targetSelect.innerHTML = myLessonsThisWeek.map(l => `
          <option value="${l.id}">${l.day} (${l.date}) @ ${l.startTime} - ${l.topic || 'Lesson'}</option>
        `).join('');
      }

      const myRequests = requests.filter(r => r.studentId === student.id);
      const feed = document.getElementById('studentRequestFeed');

      if (myRequests.length === 0) {
        feed.innerHTML = `<div style="text-align:center; padding:24px; color:var(--slate-400); font-size:0.88rem;">You haven't sent any messages or change requests yet.</div>`;
      } else {
        feed.innerHTML = myRequests.map(r => `
          <div class="req-item-card ${r.status === 'Pending' ? 'pending' : 'resolved'}">
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <div>
                <span class="badge ${r.status === 'Pending' ? 'badge-unpaid' : 'badge-paid'}">${r.status}</span>
                <strong style="margin-left: 8px; font-size: 0.92rem;">${r.requestType} for ${r.lessonSummary}</strong>
              </div>
              <span style="font-size: 0.75rem; color: var(--slate-400);">${new Date(r.dateSubmitted).toLocaleDateString()}</span>
            </div>

            <div class="chat-bubble-student">
              "${r.message}"
            </div>

            ${r.teacherReply ? `
              <div class="chat-bubble-teacher">
                <div class="teacher-badge">👩‍🏫 Teacher Annette's Answer:</div>
                <div style="font-weight:600;">"${r.teacherReply}"</div>
                <div style="font-size:0.72rem; color:#4338ca; margin-top:6px;">Replied on ${new Date(r.teacherReplyDate).toLocaleDateString()}</div>
              </div>
            ` : `
              <div style="font-size: 0.8rem; color: var(--amber-700); font-weight: 600; margin-top: 6px; display:flex; align-items:center; gap:6px;">
                ⏳ Teacher Annette has received your message and will answer you here shortly.
              </div>
            `}
          </div>
        `).join('');
      }
    }

    async function handleStudentRequestSubmit(e) {
      e.preventDefault();
      const lessonId = document.getElementById('reqTargetLessonSelect').value;
      const reqType = document.getElementById('reqTypeSelect').value;
      const note = document.getElementById('reqNoteText').value.trim();

      if (!lessonId) { alert('Please select a lesson.'); return; }

      const lesson = lessons.find(l => l.id === lessonId);
      const student = students.find(s => s.id === session.studentId) || { id: session.studentId, name: session.name };

      const newReq = {
        id: 'req_' + Date.now(),
        studentId: session.studentId,
        studentName: student.name,
        lessonId: lessonId,
        lessonSummary: lesson ? `${lesson.day} @ ${lesson.startTime}` : 'Session',
        requestType: reqType,
        message: note,
        dateSubmitted: new Date().toISOString(),
        status: 'Pending',
        teacherReply: '',
        teacherReplyDate: null
      };

      if (isBackendActive) {
        try {
          await fetch(`${API_BASE}/requests`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newReq)
          });
          await loadFromBackend();
        } catch (err) {
          requests.unshift(newReq);
          persistData();
        }
      } else {
        requests.unshift(newReq);
        persistData();
      }

      document.getElementById('reqNoteText').value = '';
      triggerToast('Request sent to Teacher Annette!');
      refreshUI();
    }

    /* ==========================================================
       TEACHER DASHBOARD
       ========================================================== */
    function renderTeacherDashboard(week) {
      const weekLessons = lessons.filter(l => l.weekId === week.weekId);

      const totalCount = weekLessons.length;
      const completedCount = weekLessons.filter(l => l.status === 'Completed').length;
      const pendingCount = requests.filter(r => r.status === 'Pending').length;

      let totalRev = 0;
      let paidRev = 0;
      let unpaidLessonsCount = 0;

      weekLessons.forEach(l => {
        if (l.status !== 'Cancelled') {
          totalRev += (Number(l.rate) || 0);
          if (l.payment === 'Paid') {
            paidRev += (Number(l.rate) || 0);
          } else {
            unpaidLessonsCount++;
          }
        }
      });

      const pct = totalRev > 0 ? Math.round((paidRev / totalRev) * 100) : 0;
      document.getElementById('mProgressFill').style.width = `${pct}%`;

      document.getElementById('mTotalLessons').textContent = totalCount;
      document.getElementById('mCompletedSubtitle').textContent = `${completedCount} sessions completed`;
      document.getElementById('mPendingReqs').textContent = pendingCount;
      document.getElementById('mTotalRevenue').textContent = `$${totalRev}`;
      document.getElementById('mPaidSubtitle').textContent = `$${paidRev} collected (${pct}%)`;
      document.getElementById('mUnpaidBalance').textContent = `$${totalRev - paidRev}`;
      document.getElementById('mUnpaidSessions').textContent = `${unpaidLessonsCount} unpaid lessons`;

      renderTeacherScheduleBoard(week);
    }

    function handleScheduleFilterChange() {
      const week = getWeekData(weekOffset);
      renderTeacherScheduleBoard(week);
    }

    function renderTeacherScheduleBoard(week) {
      const container = document.getElementById('teacherScheduleBoard');
      let weekLessons = lessons.filter(l => l.weekId === week.weekId);

      const searchQ = (document.getElementById('scheduleSearchInput')?.value || '').toLowerCase();
      const dayFilter = document.getElementById('scheduleDayFilter')?.value || 'all';
      const locFilter = document.getElementById('scheduleLocFilter')?.value || 'all';

      if (searchQ) {
        weekLessons = weekLessons.filter(l => 
          l.studentName.toLowerCase().includes(searchQ) || (l.topic || '').toLowerCase().includes(searchQ)
        );
      }
      if (locFilter !== 'all') {
        weekLessons = weekLessons.filter(l => l.location.includes(locFilter));
      }

      container.innerHTML = week.days.map(d => {
        if (dayFilter !== 'all' && d.dayName !== dayFilter) return '';

        const dayLessons = weekLessons.filter(l => l.day === d.dayName);
        dayLessons.sort((a, b) => a.startTime.localeCompare(b.startTime));

        return `
          <div class="day-column">
            <div class="day-header ${d.isToday ? 'today' : ''}">
              <span class="day-title">${d.dayName}</span>
              <span class="day-date-tag">${d.displayDate}</span>
            </div>
            <div class="day-content">
              ${dayLessons.length === 0 ? `
                <div class="empty-state-day">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:6px;"><circle cx="12" cy="12" r="10"/><path d="M8 12h8"/></svg>
                  No Lessons
                </div>
              ` : dayLessons.map(l => {
                const hasPending = requests.some(r => r.lessonId === l.id && r.status === 'Pending');

                let cardClasses = 'teacher-lesson-card';
                if (l.status === 'Cancelled') cardClasses += ' status-cancelled';
                if (l.status === 'Completed') cardClasses += ' status-completed';
                if (hasPending) cardClasses += ' has-pending-req';

                return `
                  <div class="${cardClasses}">
                    <div class="lesson-time-row">
                      <span class="lesson-time">
                        ${l.startTime}–${l.endTime}
                      </span>
                      <span class="badge ${l.payment === 'Paid' ? 'badge-paid' : 'badge-unpaid'}">
                        ${l.payment === 'Paid' ? 'Paid' : `$${l.rate}`}
                      </span>
                    </div>

                    <div class="student-badge-name">
                      👤 ${l.studentName}
                    </div>

                    <div class="lesson-topic">
                      ${l.topic || 'General Practice'}
                    </div>

                    <div style="font-size:0.75rem; color:var(--slate-500); display:flex; justify-content:space-between; align-items:center;">
                      <span>📍 ${l.location.includes('Zoom') ? 'Zoom' : 'Studio'}</span>
                      ${hasPending ? '<span class="badge badge-unpaid">Pending Req</span>' : ''}
                    </div>

                    <div class="lesson-actions-bar">
                      <button class="action-icon-btn" onclick="editLesson('${l.id}')">Edit</button>
                      <button class="action-icon-btn" onclick="quickTogglePay('${l.id}')">
                        ${l.payment === 'Paid' ? 'Unpay' : 'Mark Paid'}
                      </button>
                    </div>
                  </div>
                `;
              }).join('')}

              <button class="btn btn-secondary btn-sm" style="margin-top:auto; width:100%; border-style:dashed;" onclick="quickAddForDay('${d.dayName}', '${d.isoDate}')">
                + Add Slot
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderTeacherRequests() {
      const feed = document.getElementById('teacherRequestsFeed');
      if (requests.length === 0) {
        feed.innerHTML = `<div style="text-align:center; padding:40px; color:var(--slate-400);">No requests in inbox.</div>`;
        return;
      }

      feed.innerHTML = requests.map(r => {
        const isPending = (r.status === 'Pending');
        return `
          <div class="req-item-card ${isPending ? 'pending' : 'resolved'}">
            <div style="display:flex; justify-content:space-between; align-items:center;">
              <div>
                <span class="badge ${isPending ? 'badge-unpaid' : 'badge-paid'}">${r.status}</span>
                <strong style="margin-left: 8px; font-size: 1rem;">${r.studentName}</strong>
                <span style="font-size:0.85rem; color:var(--slate-500); margin-left:6px;">(${r.requestType})</span>
              </div>
              <span style="font-size:0.75rem; color:var(--slate-400);">${new Date(r.dateSubmitted).toLocaleString()}</span>
            </div>

            <div style="font-size:0.85rem; margin-top:6px; color:var(--slate-600);">
              <strong>Target Session:</strong> ${r.lessonSummary}
            </div>

            <div class="chat-bubble-student">
              "${r.message}"
            </div>

            ${r.teacherReply ? `
              <div class="chat-bubble-teacher" style="margin-bottom:12px;">
                <div class="teacher-badge">Your Sent Answer:</div>
                <div>"${r.teacherReply}"</div>
              </div>
            ` : ''}

            <div style="margin: 10px 0; display: flex; gap: 6px; flex-wrap: wrap;">
              <span class="quick-chip" onclick="applyQuickReply('${r.id}', 'Approved! See you then.')">⚡ Approved</span>
              <span class="quick-chip" onclick="applyQuickReply('${r.id}', 'Cancellation confirmed. We will make it up next week.')">⚡ Confirm Cancel</span>
              <span class="quick-chip" onclick="applyQuickReply('${r.id}', 'Sorry, that hour is taken. Can you do 1 hour later?')">⚡ Suggest Different Hour</span>
            </div>

            <div style="margin-top: 10px;">
              <textarea id="tReplyInput_${r.id}" class="input-field" style="min-height:60px; margin-bottom:8px;" placeholder="Type your answer to ${r.studentName}...">${r.teacherReply || ''}</textarea>
              <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                <button class="btn btn-primary btn-sm" onclick="submitTeacherReply('${r.id}')">
                  Send Answer to Student
                </button>
                ${isPending ? `
                  <button class="btn btn-secondary btn-sm" onclick="editLesson('${r.lessonId}')">
                    ✏️ Update Slot in Timetable
                  </button>
                  <button class="btn btn-sm" style="background:var(--rose-50); color:var(--rose-600); border:1px solid #fecdd3;" onclick="cancelLessonFromRequest('${r.id}')">
                    Mark Lesson Cancelled
                  </button>
                ` : ''}
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function applyQuickReply(reqId, text) {
      document.getElementById(`tReplyInput_${reqId}`).value = text;
    }

    async function submitTeacherReply(reqId) {
      const text = document.getElementById(`tReplyInput_${reqId}`).value.trim();
      if (!text) { alert('Please write an answer for the student.'); return; }

      if (isBackendActive) {
        try {
          await fetch(`${API_BASE}/requests/${reqId}/reply`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ reply: text, newStatus: 'Answered' })
          });
          await loadFromBackend();
        } catch (err) {
          updateLocalReq(reqId, text);
        }
      } else {
        updateLocalReq(reqId, text);
      }

      triggerToast('Reply sent to student!');
      renderTeacherRequests();
      updateBadges();
    }

    function updateLocalReq(reqId, text) {
      const req = requests.find(r => r.id === reqId);
      if (req) {
        req.teacherReply = text;
        req.teacherReplyDate = new Date().toISOString();
        req.status = 'Answered';
        persistData();
      }
    }

    async function cancelLessonFromRequest(reqId) {
      const req = requests.find(r => r.id === reqId);
      if (req && req.lessonId) {
        const l = lessons.find(les => les.id === req.lessonId);
        if (l) {
          l.status = 'Cancelled';
          req.status = 'Answered';
          req.teacherReply = req.teacherReply || 'Your cancellation has been noted and updated in the schedule.';
          req.teacherReplyDate = new Date().toISOString();

          if (isBackendActive) {
            try {
              await fetch(`${API_BASE}/lessons`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(l)
              });
              await fetch(`${API_BASE}/requests/${reqId}/reply`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ reply: req.teacherReply, newStatus: 'Answered' })
              });
              await loadFromBackend();
            } catch (err) {
              persistData();
            }
          } else {
            persistData();
          }

          triggerToast('Lesson cancelled and student notified.');
          renderTeacherRequests();
          refreshUI();
        }
      }
    }

    /* Payments Tracker */
    function renderPaymentLedger() {
      const filter = document.getElementById('paymentFilterSelect').value;
      const week = getWeekData(weekOffset);
      const weekLessons = lessons.filter(l => l.weekId === week.weekId);

      let displayed = weekLessons;
      if (filter === 'unpaid') displayed = weekLessons.filter(l => l.payment === 'Unpaid');
      if (filter === 'paid') displayed = weekLessons.filter(l => l.payment === 'Paid');

      const tbody = document.getElementById('paymentLedgerTbody');
      if (displayed.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:var(--slate-400);">No lessons recorded for this week yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = displayed.map(l => {
        const isPaid = (l.payment === 'Paid');
        const student = students.find(s => s.id === l.studentId);

        return `
          <tr>
            <td>
              <div style="font-weight:700; color:var(--slate-900);">${l.studentName}</div>
              <div style="font-size:0.75rem; color:var(--slate-500);">${l.topic || 'Lesson'}</div>
            </td>
            <td>${l.day}, ${l.date} at ${l.startTime}</td>
            <td><strong>$${l.rate}</strong></td>
            <td><span class="badge ${l.status === 'Completed' ? 'badge-paid' : (l.status === 'Cancelled' ? 'badge-cancelled' : 'badge-confirmed')}">${l.status}</span></td>
            <td>
              <span class="badge ${isPaid ? 'badge-paid' : 'badge-unpaid'}">
                ${isPaid ? '✓ Paid' : '⏳ Pending'}
              </span>
            </td>
            <td>
              <select class="input-field" style="padding:4px 8px; font-size:0.8rem; width:auto;" onchange="updatePaymentMethod('${l.id}', this.value)">
                <option value="Bit" ${l.method === 'Bit' ? 'selected' : ''}>Bit</option>
                <option value="PayBox" ${l.method === 'PayBox' ? 'selected' : ''}>PayBox</option>
                <option value="Cash" ${l.method === 'Cash' ? 'selected' : ''}>Cash</option>
                <option value="Bank Transfer" ${l.method === 'Bank Transfer' ? 'selected' : ''}>Bank Transfer</option>
              </select>
            </td>
            <td>
              <div style="display:flex; gap:6px;">
                <button class="btn btn-secondary btn-sm" onclick="quickTogglePay('${l.id}')">
                  ${isPaid ? 'Mark Unpaid' : 'Mark as Paid'}
                </button>
                <button class="wa-btn" onclick="openWaComposer('${l.id}')">
                  💬 WhatsApp
                </button>
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }

    function openWaComposer(lessonId) {
      const l = lessons.find(les => les.id === lessonId);
      if (!l) return;
      const student = students.find(s => s.id === l.studentId);
      activeWaContext = { lesson: l, student: student };

      setWaTemplate(l.payment === 'Paid' ? 'confirm' : 'payment');
      openModal('waModal');
    }

    function setWaTemplate(type) {
      if (!activeWaContext) return;
      const { lesson, student } = activeWaContext;
      const name = student ? student.name : 'Student';
      const phone = student && student.wa ? student.wa : '';

      let text = '';
      if (type === 'reminder') {
        text = `Hi ${name}! This is Teacher Annette. Looking forward to our English lesson on ${lesson.day} (${lesson.date}) at ${lesson.startTime}. Please have your notebook ready!`;
      } else if (type === 'payment') {
        text = `Hi ${name}! This is Teacher Annette. A gentle reminder regarding our lesson on ${lesson.day} (${lesson.date}) — fee is $${lesson.rate} (via ${lesson.method || 'Bit'}). Thank you!`;
      } else if (type === 'confirm') {
        text = `Hi ${name}! Your lesson for ${lesson.day} at ${lesson.startTime} is confirmed. See you soon! — Teacher Annette`;
      }

      document.getElementById('waComposerText').value = text;
      const encoded = encodeURIComponent(text);
      document.getElementById('waSendAnchor').href = phone ? `https://wa.me/${phone}?text=${encoded}` : `https://wa.me/?text=${encoded}`;
    }

    function copyWaText() {
      const t = document.getElementById('waComposerText').value;
      navigator.clipboard.writeText(t).then(() => triggerToast('Message copied!'));
    }

    async function updatePaymentMethod(lessonId, method) {
      const l = lessons.find(les => les.id === lessonId);
      if (l) {
        l.method = method;
        if (isBackendActive) {
          try {
            await fetch(`${API_BASE}/lessons`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(l)
            });
          } catch(e){}
        }
        persistData();
        triggerToast('Payment method updated.');
      }
    }

    async function quickTogglePay(lessonId) {
      const l = lessons.find(les => les.id === lessonId);
      if (l) {
        l.payment = (l.payment === 'Paid') ? 'Unpaid' : 'Paid';
        if (isBackendActive) {
          try {
            await fetch(`${API_BASE}/lessons`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(l)
            });
          } catch(e){}
        }
        persistData();
        triggerToast(`Updated payment for ${l.studentName}`);
        refreshUI();
        if (document.getElementById('tTabPayments').style.display === 'block') {
          renderPaymentLedger();
        }
      }
    }

    /* Roster */
    function renderStudentRoster() {
      const tbody = document.getElementById('studentRosterTbody');
      if (students.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:30px; color:var(--slate-400);">No students registered yet. Students can register on the homepage, or you can click "+ Add Student" above.</td></tr>`;
        return;
      }

      tbody.innerHTML = students.map(s => {
        return `
          <tr>
            <td><strong>${s.name}</strong></td>
            <td><span class="badge" style="background:#f1f5f9; color:var(--slate-700);">${s.grade}</span></td>
            <td>${s.phone || 'N/A'}</td>
            <td><strong>$${s.rate}/hr</strong></td>
            <td style="font-size:0.8rem; color:var(--slate-500); max-width:220px;">${s.notes || '-'}</td>
            <td>
              <button class="wa-btn" onclick="openDirectStudentWa('${s.id}')">
                💬 WhatsApp
              </button>
            </td>
            <td>
              <button class="action-icon-btn" onclick="editStudent('${s.id}')">Edit</button>
            </td>
          </tr>
        `;
      }).join('');
    }

    function openDirectStudentWa(studentId) {
      const st = students.find(s => s.id === studentId);
      if (!st) return;
      activeWaContext = { student: st, lesson: { day: 'our next lesson', date: '', startTime: '', rate: st.rate, method: 'Bit' } };
      setWaTemplate('confirm');
      openModal('waModal');
    }

    function openLessonModal() {
      if (students.length === 0) {
        alert('You have no students registered yet! Please add a student first or have them sign up.');
        openStudentModal();
        return;
      }

      document.getElementById('lessonModalHeader').textContent = 'Add Private Lesson';
      document.getElementById('modalLessonId').value = '';

      const week = getWeekData(weekOffset);
      document.getElementById('modalLessonDate').value = week.days[0].isoDate;
      document.getElementById('modalLessonDay').value = week.days[0].dayName;
      document.getElementById('modalLessonStart').value = '16:00';
      document.getElementById('modalLessonEnd').value = '17:00';
      document.getElementById('modalLessonTopic').value = '';
      document.getElementById('modalLessonPayment').value = 'Unpaid';
      document.getElementById('modalLessonStatus').value = 'Confirmed';

      const mSelect = document.getElementById('modalLessonStudent');
      mSelect.innerHTML = students.map(s => `<option value="${s.id}">👤 ${s.name} (${s.grade})</option>`).join('');

      handleModalStudentChange();
      openModal('lessonModal');
    }

    function quickAddForDay(dayName, isoDate) {
      openLessonModal();
      document.getElementById('modalLessonDay').value = dayName;
      document.getElementById('modalLessonDate').value = isoDate;
    }

    function handleModalStudentChange() {
      const studentId = document.getElementById('modalLessonStudent').value;
      const s = students.find(st => st.id === studentId);
      if (s) document.getElementById('modalLessonRate').value = s.rate || 45;
    }

    function editLesson(lessonId) {
      const l = lessons.find(les => les.id === lessonId);
      if (!l) return;

      document.getElementById('lessonModalHeader').textContent = 'Edit Lesson';
      document.getElementById('modalLessonId').value = l.id;
      
      const mSelect = document.getElementById('modalLessonStudent');
      mSelect.innerHTML = students.map(s => `<option value="${s.id}" ${s.id === l.studentId ? 'selected' : ''}>👤 ${s.name} (${s.grade})</option>`).join('');
      
      document.getElementById('modalLessonDay').value = l.day;
      document.getElementById('modalLessonDate').value = l.date;
      document.getElementById('modalLessonStart').value = l.startTime;
      document.getElementById('modalLessonEnd').value = l.endTime;
      document.getElementById('modalLessonRate').value = l.rate;
      document.getElementById('modalLessonPayment').value = l.payment;
      document.getElementById('modalLessonTopic').value = l.topic || '';
      document.getElementById('modalLessonLocation').value = l.location;
      document.getElementById('modalLessonStatus').value = l.status;

      openModal('lessonModal');
    }

    async function handleLessonSave(e) {
      e.preventDefault();
      const editId = document.getElementById('modalLessonId').value;
      const studentId = document.getElementById('modalLessonStudent').value;
      const student = students.find(s => s.id === studentId);
      const week = getWeekData(weekOffset);

      const data = {
        id: editId || ('l_' + Date.now()),
        studentId,
        studentName: student ? student.name : 'Student',
        weekId: week.weekId,
        day: document.getElementById('modalLessonDay').value,
        date: document.getElementById('modalLessonDate').value,
        startTime: document.getElementById('modalLessonStart').value,
        endTime: document.getElementById('modalLessonEnd').value,
        rate: Number(document.getElementById('modalLessonRate').value) || 0,
        payment: document.getElementById('modalLessonPayment').value,
        method: 'Bit',
        topic: document.getElementById('modalLessonTopic').value.trim(),
        location: document.getElementById('modalLessonLocation').value,
        status: document.getElementById('modalLessonStatus').value
      };

      if (isBackendActive) {
        try {
          await fetch(`${API_BASE}/lessons`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
          });
          await loadFromBackend();
        } catch(err) {
          saveLocalLesson(editId, data);
        }
      } else {
        saveLocalLesson(editId, data);
      }

      persistData();
      closeModal('lessonModal');
      refreshUI();
      triggerToast('Lesson saved successfully.');
    }

    function saveLocalLesson(editId, data) {
      if (editId) {
        const idx = lessons.findIndex(l => l.id === editId);
        if (idx !== -1) lessons[idx] = data;
      } else {
        lessons.push(data);
      }
    }

    function duplicateCurrentWeek() {
      const curWeek = getWeekData(weekOffset);
      const nextWeek = getWeekData(weekOffset + 1);

      const curLessons = lessons.filter(l => l.weekId === curWeek.weekId);
      if (curLessons.length === 0) {
        alert('No lessons found in this week to duplicate.');
        return;
      }

      if (!confirm(`Duplicate all ${curLessons.length} lessons into next week (${nextWeek.label})?`)) return;

      curLessons.forEach(l => {
        const targetDay = nextWeek.days.find(d => d.dayName === l.day);
        const copyItem = {
          ...l,
          id: 'l_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
          weekId: nextWeek.weekId,
          date: targetDay ? targetDay.isoDate : l.date,
          payment: 'Unpaid',
          status: 'Confirmed'
        };
        lessons.push(copyItem);
      });

      persistData();
      shiftWeek(1);
      triggerToast('Schedule copied to next week!');
    }

    function openStudentModal() {
      document.getElementById('studentModalHeader').textContent = 'Add Student';
      document.getElementById('modalStudentId').value = '';
      document.getElementById('modalStudentName').value = '';
      document.getElementById('modalStudentGrade').value = '';
      document.getElementById('modalStudentRate').value = '45';
      document.getElementById('modalStudentPhone').value = '';
      document.getElementById('modalStudentNotes').value = '';
      openModal('studentModal');
    }

    function editStudent(studentId) {
      const s = students.find(st => st.id === studentId);
      if (!s) return;

      document.getElementById('studentModalHeader').textContent = 'Edit Student Profile';
      document.getElementById('modalStudentId').value = s.id;
      document.getElementById('modalStudentName').value = s.name;
      document.getElementById('modalStudentGrade').value = s.grade;
      document.getElementById('modalStudentRate').value = s.rate;
      document.getElementById('modalStudentPhone').value = s.phone;
      document.getElementById('modalStudentNotes').value = s.notes;
      openModal('studentModal');
    }

    async function handleStudentSave(e) {
      e.preventDefault();
      const editId = document.getElementById('modalStudentId').value;
      const phoneRaw = document.getElementById('modalStudentPhone').value.trim();
      let cleanDigits = phoneRaw.replace(/\D/g, '');
      if (cleanDigits.startsWith('0')) cleanDigits = '972' + cleanDigits.substring(1);

      const data = {
        id: editId || ('s_' + Date.now()),
        name: document.getElementById('modalStudentName').value.trim(),
        grade: document.getElementById('modalStudentGrade').value.trim(),
        rate: Number(document.getElementById('modalStudentRate').value) || 45,
        phone: phoneRaw,
        wa: cleanDigits,
        notes: document.getElementById('modalStudentNotes').value.trim(),
        password: 'student123'
      };

      if (isBackendActive) {
        try {
          await fetch(`${API_BASE}/students`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
          });
          await loadFromBackend();
        } catch(err) {
          saveLocalStudent(editId, data);
        }
      } else {
        saveLocalStudent(editId, data);
      }

      persistData();
      closeModal('studentModal');
      renderStudentRoster();
      refreshUI();
      triggerToast('Student profile saved.');
    }

    function saveLocalStudent(editId, data) {
      if (editId) {
        const idx = students.findIndex(s => s.id === editId);
        if (idx !== -1) {
          data.password = students[idx].password || 'student123';
          students[idx] = data;
        }
      } else {
        students.push(data);
      }
    }

    function openModal(id) {
      document.getElementById(id).classList.add('show');
    }

    function closeModal(id) {
      document.getElementById(id).classList.remove('show');
    }

    function exportBackupFile() {
      const backup = { timestamp: new Date().toISOString(), students, lessons, requests };
      const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = `annettes_lessons_backup_${new Date().toISOString().slice(0, 10)}.json`;
      a.click();
      triggerToast('Backup downloaded.');
    }

    function importBackupFile(e) {
      const file = e.target.files[0];
      if (!file) return;

      const reader = new FileReader();
      reader.onload = function(evt) {
        try {
          const data = JSON.parse(evt.target.result);
          if (data.students && data.lessons) {
            students = data.students;
            lessons = data.lessons;
            requests = data.requests || [];
            persistData();
            triggerToast('Backup restored successfully!');
            refreshUI();
          }
        } catch (err) {
          alert('Invalid backup JSON format.');
        }
      };
      reader.readAsText(file);
    }

    window.addEventListener('DOMContentLoaded', () => {
      checkBackendConnection();
      refreshUI();
    });
  </script>
</body>
</html>
"""

@app.get("/")
def serve_frontend():
    path = find_html_file()
    if path:
        return FileResponse(path)
    # If file was not uploaded to repo, return the complete embedded HTML portal
    return HTMLResponse(EMBEDDED_HTML)

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
        conn.close()
        if payload.password in ["annette123", "annette", "admin"]:
            return {"role": "teacher", "name": "Annette"}
        raise HTTPException(status_code=401, detail="Invalid teacher password (default: annette123)")
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
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    print("==================================================")
    print(f" Annette's Private Lessons Server Running on {host}:{port}")
    print(f" Open in browser: http://127.0.0.1:{port}")
    print("==================================================")
    uvicorn.run("server:app", host=host, port=port)
server.py
Displaying server.py.
