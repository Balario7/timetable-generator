# ✅ PostgreSQL + Project Setup Checklist

## **Step 1: Download & Install PostgreSQL** ☐

- [ ] Visit: https://www.postgresql.org/download/windows/
- [ ] Download PostgreSQL 15 or 16 (64-bit)
- [ ] Run installer: `postgresql-15.x-x64-setup.exe`
- [ ] **Installation Settings:**
  - [ ] Port: **5432** (IMPORTANT!)
  - [ ] Password for postgres: **`postgres`** (or remember your password)
  - [ ] Keep all components selected
- [ ] Finish installation
- [ ] PostgreSQL service should start automatically

**Verify:** Open PowerShell and run:
```powershell
psql --version
```
Should show PostgreSQL version number

---

## **Step 2: Create Database** ☐

Open PowerShell:

```powershell
psql -U postgres
```

When asked for password, enter: `postgres` (or your password from install)

Then run:
```sql
CREATE DATABASE timetable_db ENCODING 'UTF8';
\q
```

**Verify:** 
```powershell
psql -U postgres -d timetable_db -c "SELECT version();"
```
Should show PostgreSQL version info

---

## **Step 3: Update Project Files** ☐

✅ **Already Done!**
- Backend code updated to use PostgreSQL (✓)
- Requirements.txt has psycopg2-binary (✓)
- Database initialization scripts ready (✓)

---

## **Step 4: Prepare Python Environment** ☐

```powershell
cd "c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master"

# Create virtual environment (if not exists)
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
cd backend
pip install -r requirements.txt
```

**Verify:**
```powershell
python -c "import psycopg2; print('SUCCESS')"
```

---

## **Step 5: Install Frontend Dependencies** ☐

```powershell
cd "c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master"
npm install
```

---

## **Step 6: Start the Application** ☐

### **Terminal 1 - Backend:**
```powershell
cd "c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master"
.\.venv\Scripts\Activate.ps1
cd backend
python app.py
```

Wait for message: `Uvicorn running on http://127.0.0.1:8000`

### **Terminal 2 - Frontend:**
```powershell
cd "c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master"
npm start
```

Wait for browser to open at `http://localhost:3000`

---

## **Step 7: Test the Application** ☐

- [ ] Open http://localhost:3000
- [ ] Navigation shows: ADD COURSES | ADD CONSTRAINTS | VIEW TIME TABLE
- [ ] Click "ADD COURSES" - should load without Network Error
- [ ] Add sample course:
  - Name: Math 101
  - Lectures: 3
  - Duration: 1
  - Instructor: Dr. Smith
  - Start: 09:00 AM
  - End: 05:00 PM
- [ ] Click "ADD CONSTRAINTS"
- [ ] Set working days and constraints
- [ ] Click "VIEW TIME TABLE"
- [ ] Should generate timetable without errors

---

## **Troubleshooting Checklist** ☐

### **If you get "Network Error":**

- [ ] Is Backend running? (Check Terminal 1 for "Uvicorn running on")
- [ ] Is PostgreSQL running? 
  ```powershell
  Test-NetConnection localhost -Port 5432
  ```
- [ ] Is database created?
  ```powershell
  psql -U postgres -d timetable_db -c "SELECT 1;"
  ```
- [ ] Check backend logs for errors

### **If backend won't start:**

- [ ] Check Python version: `python --version` (should be 3.9+)
- [ ] Check all packages installed: `pip list`
- [ ] Reinstall requirements: `pip install -r requirements.txt --force-reinstall`
- [ ] Check PostgreSQL connection details match (host, port, user, password)

### **If frontend won't start:**

- [ ] Check Node.js: `node --version`
- [ ] Delete `node_modules` folder and run `npm install` again
- [ ] Check if port 3000 is in use: `Test-NetConnection localhost -Port 3000`

### **If database tables don't exist:**

```powershell
# Run from backend directory with activated venv
python -c "from app import initialize_database; initialize_database(); print('Tables created!')"
```

---

## **Quick Test Commands** ☐

```powershell
# Test PostgreSQL
psql -U postgres -d timetable_db -c "SELECT COUNT(*) FROM courses;"

# Test Backend API
Invoke-WebRequest http://localhost:8000/get-courses -Headers @{}

# Test Frontend
Invoke-WebRequest http://localhost:3000
```

---

## **Reset Everything (Nuclear Option)** ☐

If something goes wrong completely:

```powershell
# 1. Stop all terminals (Ctrl+C)

# 2. Delete database and recreate
psql -U postgres -c "DROP DATABASE timetable_db;"
psql -U postgres -c "CREATE DATABASE timetable_db ENCODING 'UTF8';"

# 3. Clean Python environment
Remove-Item -Recurse -Force .venv

# 4. Recreate and reinstall
python -m venv .venv
.\.venv\Scripts\Activate.ps1
cd backend
pip install -r requirements.txt

# 5. Start fresh
python app.py
```

---

## **Files Modified/Created** ✓

- ✅ `backend/app.py` - Updated to PostgreSQL
- ✅ `POSTGRES_SETUP.md` - Complete PostgreSQL guide
- ✅ `setup_postgres.bat` - Automated database setup
- ✅ `COMPLETE_STARTUP.bat` - One-click startup
- ✅ `QUICK_START_POSTGRES.md` - Quick reference guide

---

## **Next Steps**

1. **Complete Step 1-6** of this checklist
2. **Test** the application following Step 7
3. **Add your courses and constraints**
4. **Generate timetable** without errors! ✨

---

**Status: 🟢 Ready to Deploy**

Your project is configured for PostgreSQL and ready to run!
