# Timetable Generator Verification TODO
Current Working Directory: c:/Users/GUGAN/OneDrive/Documents/Timetable generator/timetable-generator-master/

## Plan Breakdown & Progress Tracking

**Approved Plan Summary:**
- Code complete: Frontend CRUD → Backend PG → CSP generate → Display table
- No code errors; Ready post-setup (PostgreSQL + run_all.bat)
- Courses/constraints stored in PG; Timetable generated/shown (not persisted)

**Steps:**

### [ ] 1. Environment Check (Services/DB)
- Check PostgreSQL running on 5432
- Check if backend/frontend terminals active

### [ ] 2. Run Startup Script
- Execute `run_all.bat` or manual: setup_postgres.bat → start_backend.bat → start_frontend.bat

### [ ] 3. Automated Tests
- Run `backend/test_complete.py` (verifies courses/constraints/generate)

### [ ] 4. Manual End-to-End Test
- Add course via AddCourses
- Add constraints via AddConstraints
- Generate & view timetable
- Confirm no errors, data persists (query DB)

### [ ] 5. Verify Timetable Storage
- Note: Generated timetable not DB-persisted (ephemeral, shown in UI)
- Courses/constraints yes stored/retrieved from PG

### [ ] 6. Completion
- attempt_completion with status

**Next Step:** Start with env check & startup.

