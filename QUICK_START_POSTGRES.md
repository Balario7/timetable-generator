# 🚀 Quick Start Guide - PostgreSQL Setup

## **For Your First Time Setup**

### **Download PostgreSQL FIRST**

1. **Download PostgreSQL:**
   - https://www.postgresql.org/download/windows/
   - Download PostgreSQL 15 or 16

2. **Install PostgreSQL:**
   - Run the installer
   - **Password for postgres user:** Set to `postgres` (or remember what you set)
   - **Port:** Keep as `5432`
   - Finish installation

3. **Verify Installation:**
   ```powershell
   psql --version
   ```

---

## **Create Database**

Open PowerShell:

```powershell
psql -U postgres
```

When prompted for password, enter your password from install (default: `postgres`)

Then type:
```sql
CREATE DATABASE timetable_db ENCODING 'UTF8';
\q
```

---

## **Start Your Application**

### **Quick Start (All-in-One):**

Double-click: `COMPLETE_STARTUP.bat`

This will verify everything and show you startup commands.

---

### **Manual Start (If batch doesn't work):**

**Terminal 1 - Backend:**
```powershell
cd c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master
.\.venv\Scripts\Activate.ps1
cd backend
python app.py
```

**Terminal 2 - Frontend:**
```powershell
cd c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master
npm start
```

---

## **Access Your App**

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000

---

## **Common Issues & Fixes**

| Issue | Solution |
|-------|----------|
| `psql command not found` | PostgreSQL not installed or not in PATH |
| `connection refused` | PostgreSQL not running (check Windows Services) |
| `database does not exist` | Run: `psql -U postgres -c "CREATE DATABASE timetable_db ENCODING 'UTF8';"` |
| `Network Error in app` | Backend not running on `localhost:8000` |
| `Cannot connect to 127.0.0.1:5432` | PostgreSQL service not running |

---

## **Check if Services Running**

```powershell
# Backend running?
Test-NetConnection localhost -Port 8000

# Frontend running?
Test-NetConnection localhost -Port 3000

# PostgreSQL running?
Test-NetConnection localhost -Port 5432

# Full test
Invoke-WebRequest http://localhost:8000/get-courses
```

---

## **Reset Everything (Start Fresh)**

```powershell
# Drop database and recreate
psql -U postgres -c "DROP DATABASE IF EXISTS timetable_db;"
psql -U postgres -c "CREATE DATABASE timetable_db ENCODING 'UTF8';"

# Then restart backend (it will create tables automatically)
python app.py
```

---

## **If You Need to Reinstall PostgreSQL**

1. Uninstall PostgreSQL (Windows Control Panel → Programs)
2. Download fresh from: https://www.postgresql.org/download/windows/
3. Run installer with password = `postgres`
4. Create database again
5. Start fresh

---

**You're ready to go! Start with `COMPLETE_STARTUP.bat` ✅**
