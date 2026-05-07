import pymongo

def cleanup():
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    db = client.timetable
    res1 = db.courses.delete_many({})
    res2 = db.constraints.delete_many({})
    print(f"Deleted {res1.deleted_count} courses and {res2.deleted_count} constraints.")

if __name__ == "__main__":
    cleanup()
