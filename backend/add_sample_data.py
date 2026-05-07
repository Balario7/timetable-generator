import asyncio
import motor.motor_asyncio
from model import Course, Constraint, WorkingDay

async def add_sample_data():
    # Connect to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/timetable')
    database = client.timetable
    courses_collection = database.courses
    constraints_collection = database.constraints
    
    # Clear existing data
    await courses_collection.delete_many({})
    await constraints_collection.delete_many({})
    
    # Sample Courses (4 courses)
    courses = [
        {
            "name": "Mathematics",
            "lectureno": 3,  # 3 lectures per week
            "duration": 1,   # 1 hour each
            "instructor_name": "Dr. Smith",
            "start_hr": "9",
            "end_hr": "17"
        },
        {
            "name": "Physics",
            "lectureno": 2,  # 2 lectures per week
            "duration": 1,
            "instructor_name": "Dr. Johnson",
            "start_hr": "9",
            "end_hr": "17"
        },
        {
            "name": "Chemistry",
            "lectureno": 2,  # 2 lectures per week
            "duration": 1,
            "instructor_name": "Dr. Williams",
            "start_hr": "9",
            "end_hr": "17"
        },
        {
            "name": "English",
            "lectureno": 2,  # 2 lectures per week
            "duration": 1,
            "instructor_name": "Prof. Brown",
            "start_hr": "9",
            "end_hr": "17"
        }
    ]
    
    # Sample Constraints
    # Total lectures needed: 3 + 2 + 2 + 2 = 9 hours
    # Available slots: Monday(4) + Tuesday(4) + Wednesday(4) + Thursday(4) + Friday(4) = 20 slots
    # This gives plenty of room for scheduling
    constraint = {
        "working_days": [
            {"day": "Monday", "start_hr": "9", "end_hr": "17", "total_hours": "5"},
            {"day": "Tuesday", "start_hr": "9", "end_hr": "17", "total_hours": "5"},
            {"day": "Wednesday", "start_hr": "9", "end_hr": "17", "total_hours": "5"},
            {"day": "Thursday", "start_hr": "9", "end_hr": "17", "total_hours": "5"},
            {"day": "Friday", "start_hr": "9", "end_hr": "17", "total_hours": "5"}
        ],
        "consecutive_subjects": [""],  # No mandatory consecutive subjects
        "non_consecutive_subjects": [""]  # No mandatory non-consecutive subjects
    }
    
    # Insert courses
    for course in courses:
        result = await courses_collection.insert_one(course)
        print(f"Inserted course: {course['name']} with ID: {result.inserted_id}")
    
    # Insert constraint
    result = await constraints_collection.insert_one(constraint)
    print(f"Inserted constraint with ID: {result.inserted_id}")
    
    print("\nSample data added successfully!")
    print("\nCourses added:")
    for course in courses:
        print(f"  - {course['name']}: {course['lectureno']} lectures x {course['duration']} hour(s)")
    
    print("\nConstraints added:")
    print(f"  - Working days: Monday to Friday, 9 AM to 5 PM")
    print(f"  - Total available slots: 20 hours per week (4 slots per day x 5 days)")
    print(f"  - Total required hours: 9 hours per week")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(add_sample_data())
