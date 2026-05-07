import requests
import json
import sys

print("=" * 80)
print("TIMETABLE GENERATOR - TESTING WITH SAMPLE DATA")
print("=" * 80)

try:
    # Test 1: Check if courses exist
    print("\n[1] Checking courses in database...")
    response = requests.get('http://localhost:8000/get-courses')
    courses = response.json()
    print(f"✓ Found {len(courses)} courses:")
    for course in courses:
        print(f"   - {course['name']}: {course['lectureno']} lectures × {course['duration']} hour(s)")
    
    # Test 2: Check if constraints exist
    print("\n[2] Checking constraints in database...")
    response = requests.get('http://localhost:8000/get-constraints')
    constraints = response.json()
    print(f"✓ Found {len(constraints)} constraint(s)")
    if constraints:
        constraint = constraints[0]
        print(f"   Working days: {len(constraint['working_days'])} days")
        for day in constraint['working_days']:
            print(f"     - {day['day']}: {day['start_hr']}:00 to {day['end_hr']}:00 ({day['total_hours']} hours)")
    
    # Test 3: Generate timetable
    print("\n[3] Generating timetable...")
    response = requests.get('http://localhost:8000/generate-timetable')
    timetable = response.json()
    
    print("\n" + "=" * 80)
    print("GENERATED TIMETABLE")
    print("=" * 80)
    
    has_classes = False
    for day, classes in sorted(timetable.items()):
        print(f"\n{day.upper()}:")
        if classes:
            has_classes = True
            for cls in classes:
                print(f"  • {cls['name']} - {cls['startTime'].split('T')[1][:5]} to {cls['endTime'].split('T')[1][:5]}")
        else:
            print("  (No classes)")
    
    if has_classes:
        print("\n" + "=" * 80)
        print("✓ TIMETABLE GENERATED SUCCESSFULLY!")
        print("=" * 80)
        print("\nThe application is working perfectly!")
        print("You can now:")
        print("  1. Visit http://localhost:3000 in your browser")
        print("  2. Click 'Generate Time Table' to see the schedule")
        print("  3. Add more courses using the 'Add Courses' tab")
        print("  4. Set constraints using the 'Add Constraints' tab")
    else:
        print("\n⚠ Warning: No classes scheduled. Problem might be over-constrained.")
    
    print("\n")

except Exception as e:
    print(f"\n✗ Error: {e}")
    sys.exit(1)
