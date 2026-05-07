# Quick Start Guide

## Super Easy Setup (3 Steps)

### Step 1: Download and Install MongoDB
- Download: https://www.mongodb.com/try/download/community
- Run the installer (default settings)
- It will run automatically as a Windows service

### Step 2: Run Setup (One-Time)
Double-click: **`setup.bat`**

This will automatically:
- Create Python virtual environment
- Install all Python packages
- Install all Node packages
- Add sample data to MongoDB

### Step 3: Start the Project
In two separate Command Prompt windows, run:

**Window 1:**
```
start_backend.bat
```

**Window 2:**
```
start_frontend.bat
```

## That's it! 🎉

The app will open automatically at `http://localhost:3000`

---

## What to Do in the App

1. **Tab 1: Add Courses**
   - Sample courses are already added
   - Add more if you want

2. **Tab 2: Add Constraints**
   - Select working days (Mon-Fri)
   - Set hours (9 AM to 5 PM is good)
   - Add any special requests

3. **Tab 3: View Time Table**
   - Click "Generate Time Table"
   - Your schedule appears!

---

## Troubleshooting

### MongoDB won't start?
1. Check: Windows Start → Services → MongoDB 
2. If not running: Right-click → Start
3. Or download/reinstall from https://www.mongodb.com/

### Port 8000/3000 in use?
Close other apps or restart your computer

### Still having issues?
See **SETUP_GUIDE.md** for detailed help

---

Enjoy! 📅
