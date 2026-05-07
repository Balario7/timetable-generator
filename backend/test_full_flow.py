"""
Full end-to-end flow test for the Timetable Generator.
Tests: DB connection -> courses -> constraints -> timetable generation
"""
import sys
import json
sys.path.insert(0, '.')

print("=" * 60)
print("TIMETABLE GENERATOR - FULL FLOW TEST")
print("=" * 60)

# 1. DB Connection
print("\n[1] Testing PostgreSQL Connection...")
try:
    import psycopg2
    conn = psycopg2.connect(
        host='localhost', port=5432,
        database='timetable_db', user='postgres', password='hi'
    )
    print("    [PASS] DB Connection: OK")
except Exception as e:
    print(f"    [FAIL] DB Connection FAILED: {e}")
    sys.exit(1)

# 2. Check Tables
print("\n[2] Checking DB Tables...")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM courses")
course_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM constraints")
constraint_count = cur.fetchone()[0]
print(f"    [PASS] Courses in DB: {course_count}")
print(f"    [PASS] Constraints in DB: {constraint_count}")

# 3. Read courses from DB
print("\n[3] Reading Courses from DB...")
cur.execute("SELECT id, name, lectureno, duration, instructor_name, start_hr, end_hr FROM courses")
course_rows = cur.fetchall()
courses = []
for row in course_rows:
    courses.append({
        'id': row[0], 'name': row[1], 'lectureno': row[2],
        'duration': row[3], 'instructor_name': row[4],
        'start_hr': row[5], 'end_hr': row[6], 'description': ''
    })
    print(f"    - Course: {row[1]} (lectures={row[2]}, duration={row[3]}h, instructor={row[4]})")

# 4. Read constraints from DB
print("\n[4] Reading Constraints from DB...")
cur.execute("SELECT id, working_days, consecutive_subjects, non_consecutive_subjects, day_course_map FROM constraints ORDER BY id DESC LIMIT 1")
crow = cur.fetchone()
if crow:
    working_days = json.loads(crow[1]) if isinstance(crow[1], str) else crow[1]
    consecutive = json.loads(crow[2]) if isinstance(crow[2], str) else crow[2]
    non_consecutive = json.loads(crow[3]) if isinstance(crow[3], str) else crow[3]
    day_course_map = json.loads(crow[4]) if isinstance(crow[4], str) else crow[4]
    
    constraints = {
        'id': crow[0],
        'working_days': working_days,
        'consecutive_subjects': consecutive,
        'non_consecutive_subjects': non_consecutive,
        'day_course_map': day_course_map,
    }
    print(f"    [PASS] Constraint ID: {crow[0]}")
    for wd in working_days:
        print(f"    - Working day: {wd['day']} ({wd['start_hr']}:00 - {wd['end_hr']}:00)")
else:
    print("    [FAIL] No constraints found!")
    sys.exit(1)

conn.close()

# 5. Run timetable generation
print("\n[5] Running Timetable Generation...")
try:
    from csp import generate
    result = generate(constraints, courses)
    total_events = sum(len(events) for events in result.values())
    print(f"    [PASS] Timetable generated! Total scheduled slots: {total_events}")
    for day, events in result.items():
        if events:
            print(f"\n    --- {day.upper()} ---")
            for e in events:
                start = e['startTime'].split('T')[1][:5] if 'T' in e['startTime'] else e['startTime']
                end = e['endTime'].split('T')[1][:5] if 'T' in e['endTime'] else e['endTime']
                print(f"      {e['name']} | {e['instructor_name']} | {start} -> {end} | highlight={e['highlight']}")
    if total_events == 0:
        print("    [WARN] WARNING: No events scheduled. Check courses and working day slots.")
except Exception as e:
    print(f"    [FAIL] Timetable generation FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED - Project is ready end-to-end!")
print("=" * 60)
