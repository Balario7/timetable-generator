import asyncio
import motor.motor_asyncio

async def clear_and_add_data():
    # Connect to MongoDB
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/timetable')
    database = client.timetable
    courses_collection = database.courses
    constraints_collection = database.constraints
    
    # Clear existing data
    await courses_collection.delete_many({})
    await constraints_collection.delete_many({})
    print("✓ Cleared old data")
    
    # Add simple test courses
    courses = [
        {
            "name": "Math",
            "lectureno": 2,
            "duration": 1,
            "instructor_name": "Dr. A",
            "start_hr": "9",
            "end_hr": "17"
        },
        {
            "name": "Physics",
            "lectureno": 2,
            "duration": 1,
            "instructor_name": "Dr. B",
            "start_hr": "9",
            "end_hr": "17"
        },
        {
            "name": "Chemistry",
            "lectureno": 2,
            "duration": 1,
            "instructor_name": "Dr. C",
            "start_hr": "9",
            "end_hr": "17"
        }
    ]
    
    # Insert courses
    for course in courses:
        await courses_collection.insert_one(course)
    print("✓ Added 3 test courses (2 hours each = 6 hours total)")
    
    # Add constraints
    constraint = {
        "working_days": [
            {"day": "Monday", "start_hr": "9", "end_hr": "17", "total_hours": "4"},
            {"day": "Tuesday", "start_hr": "9", "end_hr": "17", "total_hours": "4"}
        ],
        "consecutive_subjects": [""],
        "non_consecutive_subjects": [""]
    }
    
    await constraints_collection.insert_one(constraint)
    print("✓ Added constraints (2 days × 4 hours = 8 hours available)")
    print("\n✓ Database ready! Total hours: 6 needed vs 8 available")
    print("\nNow go to browser and click 'Generate Time Table'")
    
    client.close()

asyncio.run(clear_and_add_data())
