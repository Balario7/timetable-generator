# 📋 How to Add New Data and Generate Timetables

## Complete Workflow Guide

### ✅ System Architecture
- **Frontend**: React app on `http://localhost:3000`
- **Backend**: FastAPI on `http://localhost:8000`
- **Database**: MongoDB on `localhost:27017`

When you add new data, it's **automatically saved to the database** and included in timetable generation!

---

## 🎯 STEP-BY-STEP: Adding New Courses and Generating Timetable

### **STEP 1: Add Courses**
1. Open browser: `http://localhost:3000`
2. Click **"ADD COURSES"** tab
3. Fill in the form:
   - **Course Name**: e.g., "Web Development"
   - **Number of Lectures**: e.g., 2
   - **Duration per lecture (hours)**: 1
   - **Instructor Name**: e.g., "Prof. Johnson"
4. Click **"ADD COURSE"** button
5. ✅ Course saved to database!

**Repeat Step 1** to add more courses if needed.

---

### **STEP 2: Set Constraints** 
1. Click **"ADD CONSTRAINTS"** tab
2. Select which days you want to schedule:
   - ☑️ Check: Monday, Tuesday, Wednesday, etc.
3. **For each selected day**, set working hours:
   - Click "Start Time" → Pick **9:00 AM** (or your preferred start)
   - Click "End Time" → Pick **5:00 PM** (or your preferred end)
   
**⚠️ IMPORTANT**: 
- Total hours available must be ≥ total course hours needed
- Example: 3 courses × 2 hours = 6 hours needed
  - So you need at least 2 days × 3 hours = 6 hours available
  - Or 1 day × 6 hours = 6 hours available

4. Click **"ADD CONSTRAINTS"** button
5. ✅ Constraints saved (replaces old ones)!

---

### **STEP 3: Generate Timetable**
1. Click **"VIEW TIME TABLE"** tab
2. Click **"GENERATE TIME TABLE"** button
3. ⏳ Wait a moment for generation...
4. 🎉 **YOU'LL SEE A TABLE WITH:**
   - **Day** column (Monday, Tuesday, etc.)
   - **Course** column (course names)
   - **Start Time** column (scheduled start time)
   - **End Time** column (scheduled end time)

---

## 📊 Example Workflow

### Scenario: Add "English" Course to Existing Schedule

**Initial State:**
- Database has: Math, Physics, Chemistry (3 courses, 6 hours total)
- Constraints: Monday 9-5 PM, Tuesday 9-5 PM (8 hours available)
- Generated timetable: 6 classes scheduled

**What You Do:**
1. Go to "ADD COURSES"
2. Add: "English" course with 1 lecture, 1 hour
3. Go to "ADD CONSTRAINTS"
4. Keep Monday & Tuesday BUT change to:
   - Monday: 9 AM - 6 PM (9 hours)
   - Tuesday: 9 AM - 5 PM (8 hours)
   - Total: 17 hours available (for 7 hours needed)
5. Click "ADD CONSTRAINTS"
6. Go to "VIEW TIME TABLE" and click "GENERATE TIME TABLE"

**Result:**
- 🎉 You'll see 7 classes scheduled including the new English course!
- Monday & Tuesday will show all courses distributed across the time slots

---

## ⚠️ Common Issues & Solutions

### **Issue: "No timetable solution found"**
**Reason**: Not enough constraint hours for the courses

**Solution**:
- Count total course hours: (lectures × duration) for each course
- Add them up
- In "ADD CONSTRAINTS", ensure you have enough hours
- Example: If you have 7 courses × 2 hours = 14 hours needed
  - Set constraints for multiple days with enough total hours
  - 3 days × 5 hours = 15 hours ✅

### **Issue: New course not showing in timetable**
**Reason**: Usually not enough constraint hours OR solver couldn't fit it

**Solution**:
1. Add more constraint hours
2. Or reduce lectures/duration for some courses
3. Or add more working days

### **Issue: Want to remove a course completely**
**Solution**: Database saves all courses added. To start fresh:
- Run the reset script: `python reset_data.py`
- Or use MongoDB directly to delete courses

---

## 🔧 Technical Details

### How the System Works:
1. **ADD COURSE**: Data → MongoDB courses collection
2. **ADD CONSTRAINTS**: Replaces old constraint → MongoDB constraints collection
3. **GENERATE TIMETABLE**: 
   - Fetches ALL courses from database
   - Fetches LATEST constraint from database
   - CSP Solver schedules courses to available time slots
   - Returns scheduled timetable

### Database Reset Command:
```bash
cd backend
venv_final\Scripts\activate.bat
python reset_data.py
```

This clears all courses and constraints, reloads original test data.

---

## ✅ Verification Checklist

- ✅ Backend running: `http://localhost:8000/get-courses` returns list
- ✅ Frontend running: `http://localhost:3000` loads without errors
- ✅ MongoDB running: data persists after browser refresh
- ✅ New courses appear in both ADD COURSES tab and generation
- ✅ New constraints override old ones (only latest is used)
- ✅ Timetable shows all courses across working days

---

## 📝 Example Data for Testing

**Test Configuration 1: Basic Schedule**
- Courses: Math (2 hrs), Physics (2 hrs), Chemistry (2 hrs)
- Constraints: Monday 9-5 PM, Tuesday 9-5 PM (8 hrs available)
- Result: All 6 hours scheduled across 2 days ✅

**Test Configuration 2: Expanded Schedule**
- Courses: Add "English" (1 hr) to above
- Constraints: Monday 9-6 PM, Tuesday 9-5 PM, Wednesday 9-12 PM (17 hrs, 7 hrs needed)
- Result: All 7 hours scheduled across 3 days ✅

---

**You're all set! Add data via the UI and the timetable will automatically include it! 🎉**
