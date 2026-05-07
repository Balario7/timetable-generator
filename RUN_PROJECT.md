# 🚀 READY TO LAUNCH - EXACT COMMANDS TO RUN

## Status: ✅ ALL ERRORS FIXED AND PROJECT READY

---

## Prerequisites (One-Time Installation)

### 1. Install MongoDB
```
👉 Download from: https://www.mongodb.com/try/download/community
👉 Run the installer (click Next → Finish)
👉 It will install and run automatically
👉 Verify: MongoDB should appear in Windows Services
```

### 2. Verify Python & Node.js Are Installed
```bash
# In Command Prompt, verify Python
python --version

# Verify Node.js
node --version  
npm --version
```

If either is missing:
- Python: https://www.python.org/downloads/
- Node.js: https://nodejs.org/

---

## EASIEST WAY - ONE CLICK SETUP

### Step 1: Running the Automated Setup (First Time Only)
```bash
# In the project root folder, double-click:
setup.bat

# This will:
# ✅ Create Python virtual environment
# ✅ Install all Python packages (including python-constraint)
# ✅ Install all Node packages
# ✅ Add sample data to MongoDB
# ✅ Everything takes ~5 minutes

# When done, you'll see:
# "Setup Complete!"
```

### Step 2: Start Backend Server
```bash
# Double-click this file:
start_backend.bat

# You should see:
# "Backend server starting on http://127.0.0.1:8000"
# 
# KEEP THIS WINDOW OPEN!
```

### Step 3: Start Frontend Server (NEW COMMAND PROMPT WINDOW)
```bash
# Double-click this file:
start_frontend.bat

# You should see:
# [1] "Frontend server starting on http://localhost:3000"
# [2] Browser opens automatically
#
# KEEP THIS WINDOW OPEN!
```

### Step 4: Use the Application
```
✅ Open http://localhost:3000 in your browser (if not already open)
✅ Click on "Add Courses" tab
✅ Click on "Add Constraints" tab  
✅ Click on "View Time Table" and click "Generate Time Table"
✅ Your timetable appears! 📅
```

---

## MANUAL WAY - Step by Step

If the batch files don't work, follow these commands:

### Backend Setup
```bash
# 1. Navigate to backend folder
cd backend

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate

# 4. Install dependencies (This fixed the errors!)
pip install -r requirements.txt

# 5. Add sample data
python add_sample_data.py

# 6. Start the server
python app.py

# You should see:
# "Uvicorn running on http://127.0.0.1:8000"
# KEEP THIS RUNNING!
```

### Frontend Setup (New Command Prompt Window)
```bash
# 1. Navigate to project root (close the backend folder)
cd ..

# 2. Install Node packages
npm install

# 3. Start the app
npm start

# You should see:
# App opens on http://localhost:3000
# KEEP THIS RUNNING!
```

---

## What Each Window Should Show

### Backend Window (Running python app.py)
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Frontend Window (Running npm start)
```
Compiled successfully!
You can now view timetable-generator in the browser.
  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### Browser
```
Timetable Generator
├─ Tab 1: Add Courses
├─ Tab 2: Add Constraints
└─ Tab 3: View Time Table
```

---

## MongoDB Verification

### Check MongoDB is Running
```bash
# In Command Prompt:
mongo --version

# Or check Windows Services:
# Press Windows+R
# Type: services.msc
# Look for: MongoDB
# Should show: Running status
```

### Start MongoDB If Not Running
```bash
# In Command Prompt (as Administrator):
net start MongoDB

# If that doesn't work, check Services:
# Services → MongoDB → Right-click → Start
```

---

## Testing the Setup

Once both servers are running:

1. **Open Browser**: http://localhost:3000
2. **Should see**: "Time Table Generator" app load
3. **Click**: "Add Courses" tab
4. **Click**: "Add Constraints" tab
5. **Click**: "View Time Table" → "Generate Time Table"
6. **Result**: Your schedule appears! ✅

---

## If Something Goes Wrong

### Error: "Cannot find module constraint"
```
✅ This is FIXED! The import has been corrected.
✅ Make sure you ran: pip install -r requirements.txt
```

### Error: "Port 8000 already in use"
```bash
# Find what's using port 8000:
netstat -ano | findstr 8000

# Kill that process (replace XXXX with the PID):
taskkill /PID XXXX /F

# Then restart: python app.py
```

### Error: "Port 3000 already in use"
```bash
# Find what's using port 3000:
netstat -ano | findstr 3000

# Kill that process (replace XXXX with the PID):
taskkill /PID XXXX /F

# Then restart: npm start
```

### Error: "MongoDB connection refused"
```bash
# Check if MongoDB is running:
# Services → MongoDB → Should be "Running"

# If not, start it (Admin Command Prompt):
net start MongoDB

# If that fails, reinstall MongoDB:
# https://www.mongodb.com/try/download/community
```

### Error: "npm: command not found"
```
✅ Install Node.js from https://nodejs.org/
✅ Restart Command Prompt after installation
✅ Try npm start again
```

### Error: "python: command not found"
```
✅ Install Python 3.8+ from https://www.python.org/
✅ Restart Command Prompt after installation
✅ Try python app.py again
```

---

## Quick Checklist Before Starting

- [x] MongoDB installed and running? Check Services
- [x] Python 3.8+ installed? Run: python --version
- [x] Node.js 14+ installed? Run: node --version
- [x] In correct folder? (Where setup.bat is)
- [x] setup.bat completed? (Look for "Setup Complete!")

---

## Expected Timeline

| Step | Time | What Happens |
|------|------|--------------|
| Install MongoDB | 5 min | Download + install one-time |
| Run setup.bat | 5 min | Auto setup Python + Node |
| Start backend | <1 min | Backend server starts |
| Start frontend | <1 min | Frontend server starts |
| **TOTAL** | **~15 min** | Ready to use! |

---

## Success Indicators

### You'll Know It Works When:

✅ Backend window shows: "Uvicorn running on http://127.0.0.1:8000"
✅ Frontend window shows: "Compiled successfully!"
✅ Browser opens to: http://localhost:3000
✅ App shows three tabs: Add Courses, Add Constraints, View Time Table
✅ You can add a course
✅ You can set constraints
✅ You can generate a timetable

---

## Support Resources

| Issue | Resource |
|-------|----------|
| Quick start | This file or QUICKSTART.md |
| Detailed setup | SETUP_GUIDE.md |
| What was fixed | FIXES_SUMMARY.md |
| Need everything | README_FIXES.md |
| All error scenarios | SETUP_GUIDE.md → Troubleshooting |

---

## All Errors FIXED ✅

```
BEFORE (Broken):
└─ from constraint import *  ❌ File doesn't exist

AFTER (Fixed):
└─ from constraint import Problem  ✅ Uses python-constraint library
```

```
BEFORE (Missing):
└─ python-constraint not in requirements.txt  ❌

AFTER (Fixed):
└─ python-constraint==1.4.0 added  ✅
```

---

## You're All Set! 🎉

**Right now:**
1. MongoDB should be installed ✅
2. All code is fixed ✅  
3. All documentation is ready ✅
4. Batch scripts are prepared ✅

**Next action:**
👉 Double-click setup.bat in the project folder

**Then:**
👉 Double-click start_backend.bat in window 1
👉 Double-click start_frontend.bat in window 2

**Finally:**
👉 Go to http://localhost:3000 and start creating timetables!

---

**Questions?** Check the appropriate .md file:
- QUICKSTART.md - 5 minute setup
- SETUP_GUIDE.md - Detailed instructions
- FIXES_SUMMARY.md - What was fixed
- README_FIXES.md - Complete reference
- VERIFICATION_REPORT.md - Quality assurance

---

**Everything is ready. Enjoy! 📅**
