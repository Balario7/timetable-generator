# 🎨 Visual Setup Guide

## **Your PostgreSQL Setup Flow**

```
START
  ↓
[1] Download PostgreSQL
    └─→ https://www.postgresql.org/download/windows/
  ↓
[2] Install PostgreSQL
    ├─→ Port: 5432
    ├─→ Password: postgres
    └─→ Finish Installation
  ↓
[3] Create Database
    └─→ Run: psql -U postgres
        Then: CREATE DATABASE timetable_db;
  ↓
[4] Activate Python Env
    └─→ .\.venv\Scripts\Activate.ps1
  ↓
[5] Start Backend
    └─→ python app.py
        (Backend runs on http://127.0.0.1:8000)
  ↓
[6] Start Frontend
    └─→ npm start
        (Frontend runs on http://localhost:3000)
  ↓
[7] Add Courses & Constraints
    └─→ UI available at http://localhost:3000
  ↓
[8] Generate Timetable
    └─→ Click "VIEW TIME TABLE"
  ↓
✅ SUCCESS - Timetable Generated!
```

---

## **System Architecture**

```
┌─────────────────────────────────────────────────┐
│                 Your Computer                    │
├─────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────────────┐         ┌──────────────┐  │
│  │   PostgreSQL     │         │  React App   │  │
│  │   Port: 5432     │         │  Port: 3000  │  │
│  └────────┬─────────┘         └──────┬───────┘  │
│           │                          │           │
│           │◄─────Connection──────────┤           │
│           │    (HTTP/API)            │           │
│           │                          │           │
│           │         FastAPI          │           │
│           │      (Port: 8000)        │           │
│           │      Backend Python      │           │
│           └──────────┬───────────────┘           │
│                      │                           │
│             [Manages Database]                  │
│                                                   │
└─────────────────────────────────────────────────┘

User Browser (http://localhost:3000)
         │
         ↓
    [Frontend UI]
         │
    (API Calls)
         │
         ↓
    [Backend Server]
         │
    (SQL Queries)
         │
         ↓
    [PostgreSQL DB]
```

---

## **File Organization**

```
Your Project Folder/
│
├── 📄 POSTGRESQL_READY.md ............. Read This First!
├── 📄 QUICK_START_POSTGRES.md ........ Quick Reference
├── 📄 POSTGRES_SETUP.md ............. Detailed Instructions
├── 📄 SETUP_CHECKLIST.md ............ Step-by-Step Checklist
│
├── 🔧 COMPLETE_STARTUP.bat ......... One-Click Setup
├── 🔧 setup_postgres.bat ........... DB Creation
│
├── 📁 backend/ ..................... Python Backend
│  ├── app.py (✅ UPDATED)
│  ├── requirements.txt
│  ├── .env.example (✅ UPDATED)
│  └── model.py
│
├── 📁 src/ ......................... React Frontend
│  ├── App.js
│  ├── index.js
│  └── components/
│
└── 📁 .venv/ ....................... Python Virtual Env
   ├── Scripts/
   └── Lib/
```

---

## **Dependency Flow**

```
Your App Needs ──→ PostgreSQL ──→ Port 5432
     ↑                              ↑
     │                              │
Backend (Python)            Database Server
  ↓                              ↑
Frontend (React)            SQL Queries
  ↓                              │
Browser                      Tables & Data
```

---

## **Step-by-Step Timeline**

| Step | Action | Time | Result |
|------|--------|------|--------|
| 1 | Download PostgreSQL | 5 min | `postgresql-15.exe` |
| 2 | Install PostgreSQL | 10 min | Service running on :5432 |
| 3 | Create Database | 1 min | `timetable_db` created |
| 4 | Activate Python | 1 min | `(.venv)` in terminal |
| 5 | Install Packages | 3 min | `psycopg2` ready |
| 6 | Start Backend | 2 min | `http://127.0.0.1:8000` |
| 7 | Start Frontend | 2 min | `http://localhost:3000` |
| 8 | Test App | 2 min | Add course & generate |
| **Total** | | **26 min** | **Ready!** |

---

## **Communication Ports**

```
Browser → Port 3000 (Frontend/React)
           ↓
           ↓ HTTP Request (/add-course)
           ↓
FrontEnd → Port 8000 (Backend/FastAPI)
           ↓
           ↓ SQL Query
           ↓
Backend  → Port 5432 (PostgreSQL Database)
           ↓
           ↓ Data
           ↓
Backend  → Port 8000 (Response JSON)
           ↓
           ↓ JSON Response
           ↓
FrontEnd → Port 3000 (Display in UI)
           ↓
           ↓
Browser: Shows Timetable ✅
```

---

## **What Each Component Does**

### **PostgreSQL (Port 5432)**
- Stores all your course and constraint data
- Manages timetable information
- Runs SQL queries from backend

### **Backend/FastAPI (Port 8000)**
- Receives requests from frontend
- Calls PostgreSQL for data
- Runs timetable generation algorithm
- Returns results to frontend

### **Frontend/React (Port 3000)**
- User interface
- Form to add courses
- Form to add constraints
- Display generated timetable
- Communicates with backend

---

## **Error Diagnosis Flow**

```
❌ Network Error?
    ↓
    [Is Backend Running?]
    ├─ NO  → Start: python app.py
    └─ YES → [Is PostgreSQL Running?]
            ├─ NO  → Start PostgreSQL Service
            └─ YES → [Does DB Exist?]
                   ├─ NO  → Create: CREATE DATABASE timetable_db;
                   └─ YES → [Check Error Logs]
```

---

## **Quick Health Check**

```powershell
# ✅ Check 1: PostgreSQL Running?
Test-NetConnection localhost -Port 5432

# ✅ Check 2: Backend Running?
Test-NetConnection localhost -Port 8000

# ✅ Check 3: Frontend Running?
Test-NetConnection localhost -Port 3000

# ✅ Check 4: Can Connect to DB?
psql -U postgres -d timetable_db -c "SELECT 1;"

# ✅ Check 5: Backend API Works?
Invoke-WebRequest http://localhost:8000/get-courses

# ✅ Check 6: Frontend Loading?
Invoke-WebRequest http://localhost:3000
```

All should return success! ✅

---

## **Your Path to Success**

```
📥 Download
  ↓
💾 Install
  ↓
⚙️ Configure
  ↓
🔌 Connect
  ↓
▶️ Start
  ↓
✨ Use
  ↓
🎉 SUCCESS!
```

---

**Start with Step 1 and follow through Step 8 above.** 

**You'll have a fully working Timetable Generator! 🚀**
