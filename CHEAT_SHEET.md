# 📌 PostgreSQL Setup Cheat Sheet

## **QUICK COMMANDS**

```powershell
# 1. Download PostgreSQL
# Go to: https://www.postgresql.org/download/windows/
# Download & Install

# 2. Create Database
psql -U postgres
CREATE DATABASE timetable_db ENCODING 'UTF8';
\q

# 3. Activate Python
.\.venv\Scripts\Activate.ps1

# 4. Start Backend (Terminal 1)
cd backend
python app.py

# 5. Start Frontend (Terminal 2)
npm start

# 6. Open App
http://localhost:3000
```

---

## **DATABASE CREDENTIALS**

```
Host:     localhost
Port:     5432
Database: timetable_db
User:     postgres
Password: postgres
```

---

## **PORTS**

```
Frontend:  http://localhost:3000
Backend:   http://127.0.0.1:8000
Database:  localhost:5432
```

---

## **VERIFICATION**

```powershell
# PostgreSQL installed?
psql --version

# Database exists?
psql -U postgres -d timetable_db -c "SELECT 1;"

# Backend running?
Invoke-WebRequest http://127.0.0.1:8000/get-courses

# Frontend running?
Invoke-WebRequest http://localhost:3000
```

---

## **COMMON ISSUES**

| Issue | Fix |
|-------|-----|
| Network Error | Start backend: `python app.py` |
| DB not found | Create: `CREATE DATABASE timetable_db;` |
| psql not found | Install PostgreSQL |
| Port in use | Stop other services |
| Connection refused | PostgreSQL service not running |

---

## **RESET DATABASE**

```powershell
# Drop and recreate
psql -U postgres -c "DROP DATABASE IF EXISTS timetable_db;"
psql -U postgres -c "CREATE DATABASE timetable_db ENCODING 'UTF8';"

# Then restart backend
python app.py
```

---

## **DOCUMENTATION**

| File | Purpose |
|------|---------|
| README_POSTGRESQL.md | Overview & quick start |
| QUICK_START_POSTGRES.md | 5-minute guide |
| SETUP_CHECKLIST.md | Step-by-step |
| POSTGRES_SETUP.md | Complete guide |

---

## **DIRECTORY**

```
c:\Users\GUGAN\OneDrive\Documents\Timetable generator\timetable-generator-master\
```

---

## **TEST CHECKLIST**

- [ ] PostgreSQL installed
- [ ] Database created
- [ ] Backend started
- [ ] Frontend started
- [ ] App opened at http://localhost:3000
- [ ] added course
- [ ] Added constraints
- [ ] Generated timetable
- [ ] ✅ No errors!

---

**Print this page for quick reference!**
