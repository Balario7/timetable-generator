# Timetable Generator - Complete Setup Guide

## Prerequisites

Before you start, ensure you have:
- **Python 3.8+** installed
- **Node.js 14+** installed
- **MongoDB** installed and running locally

---

## Step 1: Install MongoDB (Windows)

### Option A: Using MongoDB Community Edition
1. Download from: https://www.mongodb.com/try/download/community
2. Run the installer and follow default installation steps
3. MongoDB will run as a Windows service
4. Verify: Open Command Prompt and run `mongo --version`

### Option B: Using Chocolatey (if installed)
```bash
choco install mongodb-community
```

### Option C: Using MongoDB Atlas Cloud (Alternative)
1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a cluster
4. Update the connection string in `backend/app.py`:
   ```python
   client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://username:password@cluster.mongodb.net/timetable')
   ```

---

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory
```bash
cd timetable-generator-master\backend
```

### 2.2 Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2.4 Add Sample Data to MongoDB
```bash
python add_sample_data.py
```

You should see output like:
```
Inserted course: Mathematics with ID: ...
Inserted course: Physics with ID: ...
Inserted course: Chemistry with ID: ...
Inserted course: English with ID: ...
Inserted constraint with ID: ...

Sample data added successfully!
```

### 2.5 Start the Backend Server
```bash
python app.py
```

You should see:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!**

---

## Step 3: Frontend Setup

### 3.1 In a New Terminal, Navigate to Frontend Directory
```bash
cd timetable-generator-master
```

### 3.2 Install Node Dependencies
```bash
npm install
```

### 3.3 Start the Frontend Development Server
```bash
npm start
```

The app will automatically open at `http://localhost:3000`

---

## Step 4: Verify Everything Works

1. **Backend** should be running on `http://localhost:8000`
2. **Frontend** should be running on `http://localhost:3000`
3. You should see the Timetable Generator app with three tabs:
   - Add Courses
   - Add Constraints
   - View Time Table

---

## Step 5: Generate Your First Timetable

### 5.1 Add Courses (Tab 1: Add Courses)
- Sample data already added, but you can add more courses
- Fill in:
  - Course Name
  - Number of Lectures (per week)
  - Duration (hours per lecture)
  - Instructor Name
- Click "Add Course"

### 5.2 Set Working Schedule (Tab 2: Add Constraints)
- Select working days (Monday-Friday recommended)
- Set start and end hours (e.g., 9 AM to 5 PM)
- Optionally set consecutive/non-consecutive course preferences
- Click "Add Constraints"

### 5.3 Generate Timetable (Tab 3: View Time Table)
- Click "Generate Time Table"
- Your schedule will be displayed

---

## Troubleshooting

### Issue: "Cannot find module constraint.error"
**Solution:** Already fixed! The import has been corrected to use the python-constraint library.

### Issue: MongoDB Connection Error
```
ERROR: Could not connect to MongoDB at 'mongodb://localhost:27017'
```
**Solutions:**
1. Ensure MongoDB is running:
   ```bash
   # Windows
   sc query MongoDB
   
   # If not running, start it:
   net start MongoDB
   ```
2. Check MongoDB is listening on port 27017:
   ```bash
   netstat -an | findstr 27017
   ```
3. Use MongoDB Atlas instead (see Step 1, Option C)

### Issue: "Port 8000 already in use"
**Solution:** The backend is already running. Check if you have another instance:
```bash
netstat -ano | findstr 8000
```
To kill the process:
```bash
taskkill /PID <PID> /F
```

### Issue: "Port 3000 already in use"
**Solution:** Similar to above:
```bash
netstat -ano | findstr 3000
taskkill /PID <PID> /F
```

### Issue: "npm: command not found"
**Solution:** Install Node.js from https://nodejs.org/

### Issue: "No solution found" when generating timetable
**Possible causes:**
1. No courses added - Click "Add Courses" tab first
2. No constraints set - Click "Add Constraints" tab
3. Over-constrained problem - The solver found it impossible to fit all courses in the given time slots

**Solutions:**
1. Ensure total working hours >= total course hours needed
   - Example: 4 days × 5 hours = 20 hours available
   - Courses: 3 lectures × 1 hour = 3 hours needed
2. Reduce constraints or add more working hours

---

## Project Structure

```
timetable-generator-master/
├── backend/
│   ├── app.py                 # FastAPI backend server
│   ├── model.py               # Data models (Pydantic)
│   ├── csp.py                 # Constraint Solving Problem logic
│   ├── add_sample_data.py      # Initialize sample data
│   ├── requirements.txt        # Python dependencies
│   └── __pycache__/
│
├── src/
│   ├── App.js                 # Main React app
│   ├── App.css                # App styles
│   ├── theme.js               # Material-UI theme
│   ├── index.js               # React entry point
│   ├── components/
│   │   ├── AddCourses.jsx      # Add courses UI
│   │   ├── AddConstraints.jsx  # Add constraints UI
│   │   └── ViewTimeTable.jsx   # Display timetable UI
│   └── pages/
│       └── Dashboard.jsx       # Main dashboard page
│
├── public/
│   ├── index.html             # HTML entry point
│   ├── manifest.json          # PWA manifest
│   └── robots.txt             # SEO robots file
│
├── package.json               # Node.js dependencies
└── SETUP_GUIDE.md            # This file
```

---

## Key Technologies

- **Backend:** FastAPI, Python, Motor (async MongoDB), python-constraint (CSP solver)
- **Frontend:** React, Material-UI, Axios
- **Database:** MongoDB
- **Build Tool:** React Scripts

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/get-courses` | Fetch all courses |
| GET | `/get-constraints` | Fetch all constraints |
| POST | `/add-course` | Add a new course |
| POST | `/add-constraints` | Add constraints |
| GET | `/generate-timetable` | Generate timetable based on courses & constraints |

---

## Common Commands

### Backend
```bash
# Activate virtual environment
venv\Scripts\activate

# Run backend server
python app.py

# Add sample data
python add_sample_data.py

# Deactivate virtual environment
deactivate
```

### Frontend
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build

# Run tests
npm test
```

---

## Next Steps

1. Explore the UI and test with different courses/constraints
2. Customize the theme in `src/theme.js`
3. Add more sample data in `backend/add_sample_data.py`
4. Deploy to production (see respective documentation for FastAPI and React)

---

## Support

If you encounter issues:
1. Check this guide's Troubleshooting section
2. Verify all services are running (MongoDB, backend, frontend)
3. Check browser console for frontend errors (F12)
4. Check terminal output for backend errors

---

**Enjoy generating your timetables! 📅**
