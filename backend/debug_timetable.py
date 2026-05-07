import asyncio
import motor.motor_asyncio
from model import Constraint, Course
from csp import generate

async def test():
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017/timetable')
    database = client.timetable
    courses_collection = database.courses
    constraints_collection = database.constraints
    
    # Get courses
    courses = []
    cursor = courses_collection.find({})
    async for doc in cursor:
        courses.append(Course(**doc).dict())
    
    # Get constraints
    constraints = []
    cursor = constraints_collection.find({})
    async for doc in cursor:
        constraints.append(Constraint(**doc).dict())
    
    if not courses or not constraints:
        print('NO courses or constraints found')
        return
    
    print(f'Found {len(courses)} courses')
    print(f'Found {len(constraints)} constraint sets')
    print()
    print('Courses Data:')
    total_hours_needed = 0
    for course in courses:
        hours = course["lectureno"] * course["duration"]
        total_hours_needed += hours
        print(f'  - {course["name"]}: {course["lectureno"]} lectures x {course["duration"]} hour = {hours} hours')
    
    print()
    print('Constraints Data:')
    constraint = constraints[-1]
    hours_per_day = sum(int(day['total_hours']) for day in constraint['working_days'])
    total_slots = hours_per_day * len(constraint['working_days'])
    
    print(f'  Working Days: {len(constraint["working_days"])} days')
    print(f'  Total hours/week: {hours_per_day}')
    print(f'  Total slots available: {total_slots - len(constraint["working_days"])}')  # Subtract 1 per day
    print(f'  Total hours needed: {total_hours_needed}')
    print(f'  Consecutive subjects: {constraint["consecutive_subjects"]}')
    print(f'  Non-consecutive subjects: {constraint["non_consecutive_subjects"]}')
    
    print()
    print('Attempting to generate timetable...')
    try:
        result = generate(constraint, courses)
        total_classes = sum(len(day) for day in result.values())
        print(f'SUCCESS! Timetable generated with {total_classes} classes')
        print()
        print('Generated Schedule:')
        for day, classes in result.items():
            print(f'  {day.capitalize()}: {len(classes)} classes')
    except Exception as e:
        print(f'ERROR: {str(e)}')
        import traceback
        traceback.print_exc()

print('=' * 60)
print('TIMETABLE GENERATION DEBUG TEST')
print('=' * 60)
asyncio.run(test())
