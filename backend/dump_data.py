import pymongo

def dump():
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.timetable
    courses = list(db.courses.find())
    constraints = list(db.constraints.find())
    
    print("\n--- COURSES ---")
    for c in courses:
        print(f"Name: {c.get('name')}, Duration: {c.get('duration')}, Start: {c.get('start_hr')}, End: {c.get('end_hr')}")
    
    print("\n--- CONSTRAINTS ---")
    if constraints:
        con = constraints[-1]
        print(f"Working Days: {[d['day'] for d in con['working_days']]}")
        print(f"Working Hours: {[(d['day'], d['start_time'], d['end_time']) for d in con['working_days']]}")

if __name__ == "__main__":
    dump()
