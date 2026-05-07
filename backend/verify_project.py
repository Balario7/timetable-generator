import requests
import json
import time

def verify_project():
    base_url = "http://127.0.0.1:8000"
    
    print("--- 1. Cleaning up old data ---")
    # There isn't a direct clear-all endpoint, but we overwrite constraints
    # and we could delete courses if needed, but let's just add new ones.
    
    print("\n--- 2. Adding Courses (Core Subjects) ---")
    courses = [
        {"name": "Maths", "lectureno": 3, "duration": 1, "instructor_name": "Dr. Smith"},
        {"name": "Physics", "lectureno": 2, "duration": 1, "instructor_name": "Dr. Johnson"},
        {"name": "Computer Science", "lectureno": 2, "duration": 2, "instructor_name": "Prof. Alan"}
    ]
    # Total hours: 3*1 + 2*1 + 2*2 = 3 + 2 + 4 = 9 hours.
    
    for course in courses:
        resp = requests.post(f"{base_url}/add-course", json=course)
        if resp.status_code == 200:
            print(f"Added course: {course['name']}")
        else:
            print(f"Failed to add course {course['name']}: {resp.text}")

    print("\n--- 3. Adding Constraints (Mon, Tue, Wed | 9AM to 5AM) ---")
    # 9 to 5 is 8 hours. With my -1 lunch fix, it's 7 slots per day.
    # 3 days * 7 = 21 slots. Plenty for 9 hours.
    constraints = {
        "working_days": [
            {"day": "Monday", "start_hr": "9", "end_hr": "17", "total_hours": "8"},
            {"day": "Tuesday", "start_hr": "9", "end_hr": "17", "total_hours": "8"},
            {"day": "Wednesday", "start_hr": "9", "end_hr": "17", "total_hours": "8"}
        ],
        "consecutive_subjects": [""],
        "non_consecutive_subjects": [""]
    }
    
    resp = requests.post(f"{base_url}/add-constraints", json=constraints)
    if resp.status_code == 200:
        print("Constraints added successfully!")
    else:
        print(f"Failed to add constraints: {resp.text}")

    print("\n--- 4. Generating Timetable ---")
    start_time = time.time()
    resp = requests.get(f"{base_url}/generate-timetable")
    end_time = time.time()
    
    if resp.status_code == 200:
        print(f"Timetable generated successfully in {end_time - start_time:.4f} seconds!")
        data = resp.json()
        for day in ['monday', 'tuesday', 'wednesday']:
            print(f"\n[{day.upper()}] Timeline:")
            events = data.get(day, [])
            for event in events:
                # Extracted start_hr from startTime string '2018-02-25T09:00:00'
                hr = event['startTime'].split('T')[1].split(':')[0]
                print(f"  {hr}:00 - {event['name']} ({event['type']})")
    else:
        print(f"Failed to generate timetable: {resp.text}")

if __name__ == "__main__":
    try:
        verify_project()
    except Exception as e:
        print(f"Error: {e}. Is the backend running at http://localhost:8000?")
