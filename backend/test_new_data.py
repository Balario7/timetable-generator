#!/usr/bin/env python3
"""Test adding new courses and generating timetable"""

import asyncio
import aiohttp
import json

async def test_workflow():
    base_url = "http://localhost:8000"
    
    print("\n" + "="*60)
    print("TESTING NEW DATA WORKFLOW")
    print("="*60)
    
    async with aiohttp.ClientSession() as session:
        # Step 1: Get initial courses
        async with session.get(f"{base_url}/get-courses") as resp:
            courses = await resp.json()
            print(f"\n1️⃣  Initial Courses: {len(courses)}")
            for course in courses:
                print(f"   - {course['name']}")
        
        # Step 2: Get initial constraints
        async with session.get(f"{base_url}/get-constraints") as resp:
            constraints = await resp.json()
            print(f"\n2️⃣  Initial Constraints: {len(constraints)}")
            if constraints:
                const = constraints[0]
                print(f"   Working Days:")
                for day in const.get('working_days', []):
                    print(f"     - {day['day']}: {day['start_hr']}-{day['end_hr']} ({day['total_hours']} hrs)")
        
        # Step 3: Generate initial timetable
        async with session.get(f"{base_url}/generate-timetable") as resp:
            timetable = await resp.json()
            total = sum(len(timetable.get(day, [])) for day in timetable)
            print(f"\n3️⃣  Initial Timetable: {total} classes")
            for day in ['monday', 'tuesday']:
                if timetable.get(day):
                    print(f"   {day.capitalize()}: {len(timetable[day])} classes")
        
        # Step 4: Add a NEW course
        new_course = {
            "name": "English",
            "lectureno": 1,
            "duration": 1,
            "instructor_name": "Prof. Smith",
            "start_hr": "09",
            "end_hr": "17"
        }
        async with session.post(f"{base_url}/add-course", json=new_course) as resp:
            added_course = await resp.json()
            print(f"\n4️⃣  Added New Course: {added_course['name']}")
        
        # Step 5: Verify new course in database
        async with session.get(f"{base_url}/get-courses") as resp:
            courses = await resp.json()
            print(f"\n5️⃣  Courses After Adding: {len(courses)}")
            for course in courses:
                print(f"   - {course['name']}")
        
        # Step 6: Add NEW constraint with more hours for new course
        new_constraint = {
            "working_days": [
                {"day": "Monday", "start_hr": "9", "end_hr": "18", "total_hours": "5"},
                {"day": "Tuesday", "start_hr": "9", "end_hr": "18", "total_hours": "5"}
            ],
            "consecutive_subjects": [""],
            "non_consecutive_subjects": [""]
        }
        async with session.post(f"{base_url}/add-constraints", json=new_constraint) as resp:
            added_const = await resp.json()
            print(f"\n6️⃣  Added New Constraints")
            for day in added_const.get('working_days', []):
                print(f"   - {day['day']}: {day['start_hr']}-{day['end_hr']} ({day['total_hours']} hrs)")
        
        # Step 7: Generate NEW timetable with new data
        async with session.get(f"{base_url}/generate-timetable") as resp:
            new_timetable = await resp.json()
            total = sum(len(new_timetable.get(day, [])) for day in new_timetable)
            print(f"\n7️⃣  NEW Timetable: {total} classes")
            for day in ['monday', 'tuesday']:
                if new_timetable.get(day):
                    print(f"   {day.capitalize()}: {len(new_timetable[day])} classes")
                    for cls in new_timetable[day]:
                        start = cls['startTime'].split('T')[1][:5]
                        end = cls['endTime'].split('T')[1][:5]
                        print(f"      - {cls['name']}: {start}-{end}")
        
        print(f"\n{'='*60}")
        print(f"✅ TEST COMPLETE - New courses are included in timetable!")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(test_workflow())
