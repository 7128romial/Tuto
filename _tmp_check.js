
    /* Clean Production State (No Dummy Data) */
    let students = JSON.parse(localStorage.getItem('annette_students')) || [];
    let lessons = JSON.parse(localStorage.getItem('annette_lessons')) || [];
    let requests = JSON.parse(localStorage.getItem('annette_requests')) || [];
    let teacherAccounts = JSON.parse(localStorage.getItem('annette_teacher_accounts')) || [];
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
      localStorage.setItem('annette_teacher_accounts', JSON.stringify(teacherAccounts));
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

      document.getElementById('paneStudentLogin').style.display = (tab === 'studentLogin') ? 'block' : 'none';
      document.getElementById('paneStudentRegister').style.display = (tab === 'studentRegister') ? 'block' : 'none';
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
          const data = await res.json().catch(() => ({}));
          if (!res.ok) throw new Error(data.detail || 'Login failed');
          session = data;
        } catch (err) {
          alert(err.message);
          return;
        }
      } else {
        const normalizedUser = user.toLowerCase();
        const teacher = teacherAccounts.find(t => t.email.toLowerCase() === normalizedUser || t.name.toLowerCase() === normalizedUser);
        if (teacher) {
          if (teacher.password !== pass) {
            alert('Incorrect teacher password.');
            return;
          }
          session = { role: 'teacher', teacherId: teacher.id, name: teacher.name };
        } else if (['annette', 'annette@lessons.com', 'annette@lessons'].includes(normalizedUser) && ['annette123', 'annette', 'admin'].includes(pass)) {
          session = { role: 'teacher', teacherId: 't_annette', name: 'Annette' };
        } else {
          alert('Invalid teacher login. Please use the default Annette login or contact the admin.');
          return;
        }
      }

      persistData();
      triggerToast(`Signed in as ${session.name || 'Teacher'}`);
      refreshUI();
    }

    async function handleStudentSignIn(e) {
      e.preventDefault();
      const identifier = document.getElementById('studentLoginIdentifier').value.trim();
      const pass = document.getElementById('studentPassInput').value.trim();

      if (!identifier || !pass) {
        alert('Please enter your name, email, phone, or password.');
        return;
      }

      const normalizedUser = identifier.toLowerCase();
      const teacher = teacherAccounts.find(t => t.email.toLowerCase() === normalizedUser || t.name.toLowerCase() === normalizedUser);
      if (teacher) {
        if (teacher.password !== pass) {
          alert('Incorrect password.');
          return;
        }
        session = { role: 'teacher', teacherId: teacher.id, name: teacher.name };
        persistData();
        triggerToast('Signed in as Teacher');
        refreshUI();
        return;
      }

      if (['annette', 'annette@lessons.com', 'annette@lessons'].includes(normalizedUser) && ['annette123', 'annette', 'admin'].includes(pass)) {
        session = { role: 'teacher', teacherId: 't_annette', name: 'Annette' };
        persistData();
        triggerToast('Signed in as Teacher Annette');
        refreshUI();
        return;
      }

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
          alert('No account found for "' + identifier + '". Please sign up first.');
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

      if (!name || !phone || !pass) {
        alert('Please complete the student name, phone number, and password.');
        return;
      }

      let cleanDigits = phone.replace(/\D/g, '');
      if (cleanDigits.startsWith('0')) cleanDigits = '972' + cleanDigits.substring(1);

      const matchedStudent = students.find(s => {
        const sName = (s.name || '').trim().toLowerCase();
        const sPhone = (s.phone || '').replace(/\D/g, '');
        const normalizedPhone = cleanDigits.startsWith('972') ? cleanDigits : (cleanDigits.startsWith('0') ? '972' + cleanDigits.substring(1) : cleanDigits);
        return sName === name.toLowerCase() && sPhone === normalizedPhone;
      });

      if (matchedStudent) {
        matchedStudent.password = pass;
        matchedStudent.grade = grade || matchedStudent.grade || 'Student';
        matchedStudent.notes = notes || matchedStudent.notes || '';
        matchedStudent.wa = cleanDigits;
        matchedStudent.phone = phone;
        matchedStudent.rate = Number(matchedStudent.rate) || 220;
        students = students.map(s => s.id === matchedStudent.id ? matchedStudent : s);
        session = { role: 'student', studentId: matchedStudent.id, name: matchedStudent.name };
        persistData();
        triggerToast(`Welcome back, ${matchedStudent.name}!`);
        refreshUI();
        return;
      }

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
          name, grade: grade || 'Student', rate: 220, phone, wa: cleanDigits, notes, password: pass
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
        document.getElementById('userPillName').textContent = `Teacher ${session.name || 'Annette'}`;
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
            <div class="day-content" data-day-name="${d.dayName}" data-iso-date="${d.isoDate}">
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
                  <div class="${cardClasses}" draggable="true" data-lesson-id="${l.id}" data-start-time="${l.startTime}" data-end-time="${l.endTime}" aria-label="${l.studentName} lesson">
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

      document.querySelectorAll('.teacher-lesson-card').forEach(card => {
        card.addEventListener('dragstart', (event) => {
          event.dataTransfer.setData('text/plain', card.dataset.lessonId);
          event.dataTransfer.effectAllowed = 'move';
        });
      });

      document.querySelectorAll('.day-content').forEach(dayEl => {
        dayEl.addEventListener('dragover', e => {
          e.preventDefault();
          dayEl.style.borderColor = 'var(--primary)';
          dayEl.style.background = 'rgba(99, 102, 241, 0.04)';
        });

        dayEl.addEventListener('dragleave', () => {
          dayEl.style.borderColor = '';
          dayEl.style.background = '';
        });

        dayEl.addEventListener('drop', e => {
          e.preventDefault();
          dayEl.style.borderColor = '';
          dayEl.style.background = '';
          const lessonId = e.dataTransfer.getData('text/plain');
          const targetCard = e.target.closest('.teacher-lesson-card');
          const targetDayName = dayEl.dataset.dayName;
          const targetDate = dayEl.dataset.isoDate;

          if (targetCard && targetCard.dataset.lessonId !== lessonId) {
            moveLessonToDay(
              lessonId,
              targetDayName,
              targetDate,
              targetCard.dataset.startTime,
              targetCard.dataset.endTime
            );
            return;
          }

          moveLessonToDay(lessonId, targetDayName, targetDate);
        });
      });
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

      const req = requests.find(r => r.id === reqId);
      const syncLesson = req && req.requestType === 'Reschedule' ? syncApprovedReschedule(req, text) : false;

      if (isBackendActive) {
        try {
          const lesson = req && req.lessonId ? lessons.find(l => l.id === req.lessonId) : null;
          await fetch(`${API_BASE}/requests/${reqId}/reply`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              reply: text,
              newStatus: 'Answered',
              lessonId: req?.lessonId || null,
              newDay: lesson?.day || null,
              newDate: lesson?.date || null,
              newStartTime: lesson?.startTime || null,
              newEndTime: lesson?.endTime || null,
              updateLesson: syncLesson
            })
          });
          await loadFromBackend();
        } catch (err) {
          updateLocalReq(reqId, text);
          if (syncLesson) refreshUI();
        }
      } else {
        updateLocalReq(reqId, text);
        if (syncLesson) refreshUI();
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

    function getWeekIdFromDate(dateStr) {
      if (!dateStr) return null;
      const date = new Date(`${dateStr}T00:00:00`);
      if (Number.isNaN(date.getFullYear())) return null;
      const sun = new Date(date);
      sun.setDate(date.getDate() - date.getDay());
      const oneJan = new Date(sun.getFullYear(), 0, 1);
      const weekNum = Math.ceil((((sun - oneJan) / 86400000) + oneJan.getDay() + 1) / 7);
      return `${sun.getFullYear()}-W${weekNum}`;
    }

    function syncApprovedReschedule(req, replyText) {
      if (!req || req.requestType !== 'Reschedule') return false;
      if (!req.lessonId) return false;

      const lesson = lessons.find(l => l.id === req.lessonId);
      if (!lesson) return false;

      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const reply = String(replyText || '').trim();
      if (!reply) return false;

      const matchDay = reply.match(/\b(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)\b/i);
      const matchTime = reply.match(/(\d{1,2}:\d{2})\s*(?:-|–|to)\s*(\d{1,2}:\d{2})/i);
      const matchStartOnly = reply.match(/(?:at|on|for|\bto\b)\s*(\d{1,2}:\d{2})/i);

      if (!matchDay && !matchTime && !matchStartOnly) return false;

      const dayName = matchDay ? matchDay[1].charAt(0).toUpperCase() + matchDay[1].slice(1).toLowerCase() : lesson.day;
      const newDate = matchDay ? (() => {
        const targetIndex = dayNames.indexOf(dayName);
        const currentDate = new Date(`${lesson.date}T00:00:00`);
        const currentIndex = currentDate.getDay();
        const diff = (targetIndex - currentIndex + 7) % 7;
        const nextDate = new Date(currentDate);
        nextDate.setDate(currentDate.getDate() + diff);
        const yyyy = nextDate.getFullYear();
        const mm = String(nextDate.getMonth() + 1).padStart(2, '0');
        const dd = String(nextDate.getDate()).padStart(2, '0');
        return `${yyyy}-${mm}-${dd}`;
      })() : lesson.date;

      const startValue = matchTime ? matchTime[1] : (matchStartOnly ? matchStartOnly[1] : lesson.startTime);
      const endValue = matchTime ? matchTime[2] : (() => {
        const spare = reply.match(/(\d{1,2}:\d{2})\s*(?:-|–|to)\s*(\d{1,2}:\d{2})/i);
        if (spare && spare[2]) return spare[2];
        const startMinutes = timeToMinutes(startValue);
        return minutesToTime(startMinutes + 60);
      })();

      lesson.day = dayName;
      lesson.date = newDate;
      lesson.startTime = startValue;
      lesson.endTime = endValue;
      lesson.weekId = getWeekIdFromDate(newDate) || lesson.weekId;

      if (hasLessonTimeConflict(lesson, lesson.id)) {
        lesson.day = req.lessonDay || lesson.day;
        lesson.date = req.lessonDate || lesson.date;
        lesson.startTime = req.lessonStartTime || lesson.startTime;
        lesson.endTime = req.lessonEndTime || lesson.endTime;
        return false;
      }

      persistData();
      return true;
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
              <button class="action-icon-btn" onclick="deleteStudent('${s.id}')" style="margin-left:6px; background:#fee2e2; color:#991b1b;">Delete</button>
            </td>
          </tr>
        `;
      }).join('');
    }

    function deleteStudent(studentId) {
      const student = students.find(s => s.id === studentId);
      if (!student) return;
      const confirmed = confirm(`Delete student "${student.name}" and all their lessons/requests?`);
      if (!confirmed) return;

      students = students.filter(s => s.id !== studentId);
      lessons = lessons.filter(l => l.studentId !== studentId);
      requests = requests.filter(r => r.studentId !== studentId);
      persistData();
      renderStudentRoster();
      refreshUI();
      triggerToast('Student removed.');
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

    function timeToMinutes(value) {
      if (!value || typeof value !== 'string') return 0;
      const [hours, minutes] = value.split(':').map(Number);
      return (hours || 0) * 60 + (minutes || 0);
    }

    function minutesToTime(totalMinutes) {
      const normalized = ((totalMinutes % (24 * 60)) + (24 * 60)) % (24 * 60);
      const hours = Math.floor(normalized / 60);
      const minutes = normalized % 60;
      return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
    }

    function moveLessonToDay(lessonId, targetDayName, targetIsoDate, overrideStart = null, overrideEnd = null) {
      const lesson = lessons.find(l => l.id === lessonId);
      if (!lesson) return;

      const currentWeek = getWeekData(weekOffset);
      const targetDay = currentWeek.days.find(d => d.dayName === targetDayName && d.isoDate === targetIsoDate);
      if (!targetDay) return;

      const originalDate = lesson.date;
      const originalDay = lesson.day;
      const originalStart = lesson.startTime;
      const originalEnd = lesson.endTime;

      lesson.day = targetDayName;
      lesson.date = targetIsoDate;
      lesson.weekId = currentWeek.weekId;

      const durationMinutes = timeToMinutes(originalEnd) - timeToMinutes(originalStart);
      const nextStart = overrideStart || lesson.startTime;
      const nextEnd = overrideEnd || minutesToTime(timeToMinutes(nextStart) + durationMinutes);
      lesson.startTime = nextStart;
      lesson.endTime = nextEnd;

      if (hasLessonTimeConflict(lesson, lesson.id)) {
        lesson.day = originalDay;
        lesson.date = originalDate;
        lesson.startTime = originalStart;
        lesson.endTime = originalEnd;
        alert('This move creates a time overlap. Move was cancelled.');
        return;
      }

      persistData();
      refreshUI();
      triggerToast(`Lesson moved to ${targetDayName}.`);
    }

    function quickAddForDay(dayName, isoDate) {
      openLessonModal();
      document.getElementById('modalLessonDay').value = dayName;
      document.getElementById('modalLessonDate').value = isoDate;
    }

    function handleModalStudentChange() {
      const studentId = document.getElementById('modalLessonStudent').value;
      const s = students.find(st => st.id === studentId);
      if (s) document.getElementById('modalLessonRate').value = s.rate || 220;
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

    function hasLessonTimeConflict(data, ignoreId = null) {
      if (!data.date || !data.startTime || !data.endTime) return false;
      const start = new Date(`${data.date}T${data.startTime}:00`);
      const end = new Date(`${data.date}T${data.endTime}:00`);
      if (Number.isNaN(start.getTime()) || Number.isNaN(end.getTime()) || start >= end) {
        return false;
      }

      return lessons.some(existing => {
        if (ignoreId && existing.id === ignoreId) return false;
        if (!existing.date || !existing.startTime || !existing.endTime) return false;
        if (existing.date !== data.date) return false;

        const existingStart = new Date(`${existing.date}T${existing.startTime}:00`);
        const existingEnd = new Date(`${existing.date}T${existing.endTime}:00`);
        if (Number.isNaN(existingStart.getTime()) || Number.isNaN(existingEnd.getTime())) return false;

        return start < existingEnd && end > existingStart;
      });
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

      if (hasLessonTimeConflict(data, editId)) {
        const conflict = lessons.find(existing => {
          if (editId && existing.id === editId) return false;
          if (existing.date !== data.date) return false;
          const start = new Date(`${data.date}T${data.startTime}:00`);
          const end = new Date(`${data.date}T${data.endTime}:00`);
          const existingStart = new Date(`${existing.date}T${existing.startTime}:00`);
          const existingEnd = new Date(`${existing.date}T${existing.endTime}:00`);
          return start < existingEnd && end > existingStart;
        });

        alert(`Time conflict detected: ${student ? student.name : 'This student'} already has a lesson at ${conflict ? conflict.day + ' ' + conflict.startTime : 'that time'}. Please adjust the class timing.`);
        return;
      }

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
      document.getElementById('modalStudentRate').value = '220';
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
        rate: Number(document.getElementById('modalStudentRate').value) || 220,
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
  