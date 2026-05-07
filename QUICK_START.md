# QUICK START GUIDE

## ⚡ Fastest Way to Run the Entire Project

### STEP 1: Ensure MongoDB is Running
Before running the application, MongoDB must be running on your system.

**Options to start MongoDB:**
1. **Windows Service:** Run `mongod` in Command Prompt
2. **MongoDB Compass:** Open MongoDB Compass GUI
3. **Docker:** Run `docker run -d -p 27017:27017 mongo`

---

## STEP 2: Double-Click `run_all.bat`

Located in: `timetable-generator-master/run_all.bat`

This batch file will automatically:
✓ Check if MongoDB is running
✓ Check if Node.js is installed
✓ Install npm dependencies (if needed)
✓ Start Backend Server (FastAPI) on http://localhost:8000
✓ Start Frontend Server (React) on http://localhost:3000
✓ Open the application in your default browser

---

## STEP 3: Use the Application

Once the application opens in your browser:

```
┌─────────────────────────────────────────┐
│          TIMETABLE GENERATOR            │
├─────────────────────────────────────────┤
│  Tab 1: Add Courses                     │
│  ├─ Course Name                         │
│  ├─ Number of Lectures (per week)       │
│  ├─ Duration (in hours)                 │
│  └─ Instructor Name                     │
│                                         │
│  Tab 2: Add Constraints                 │
│  ├─ Working Days (Mon-Fri, 9-17)        │
│  ├─ Consecutive Subjects                │
│  └─ Non-Consecutive Subjects            │
│                                         │
│  Tab 3: View Time Table                 │
│  └─ Click "Generate Timetable"          │
└─────────────────────────────────────────┘
```

---

## Alternative: Run Services Separately

If you prefer to run each service in a separate window:

### Terminal 1: Start MongoDB
```bash
mongod
```

### Terminal 2: Start Backend
```batch
start_backend.bat
```
- Backend will run on http://localhost:8000
- API Docs: http://localhost:8000/docs

### Terminal 3: Start Frontend
```batch
start_frontend.bat
```
- Frontend will run on http://localhost:3000

---

## Verify MongoDB Connection

To check if MongoDB has all your data:

```batch
verify_mongodb.bat
```

This script will show:
- All courses in the database
- All constraints in the database
- API endpoint configuration
- Full connectivity status

---

## Default Ports

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| MongoDB | 27017 | mongodb://localhost:27017 |

---

## API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## Troubleshooting

### "MongoDB is not running"
→ Start MongoDB service: `mongod`

### "Port 3000 already in use"
→ Kill process: `netstat -ano | findstr :3000`

### "npm not found"
→ Install Node.js from https://nodejs.org

### "Cannot connect to backend"
→ Check backend window for errors
→ Verify port 8000 is not blocked

---

## Stop All Services

Simply close all three command/terminal windows:
- Close MongoDB terminal
- Close Backend window
- Close Frontend window

---

## Default Database Collections

### Courses (8 records)
- Maths (3 lectures, 1 hr each)
- Physics (2 lectures, 1 hr each)
- Computer Science (2 lectures, 2 hrs each)
- Mathematics (3 lectures, 1 hr each)
- ... and more

### Constraints (1 record)
- Working Days: Monday-Friday, 9:00-16:00
- Consecutive & Non-Consecutive subjects

---

**That's it! Your timetable generator is ready to use! 🎉**

Run `run_all.bat` and start creating timetables!
