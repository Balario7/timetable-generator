from app import initialize_database, get_conn
from psycopg2.extras import Json


def seed_cs_mock_data():
    initialize_database()

    courses = [
        {
            "name": "Data Structures",
            "description": "Core concepts of arrays, linked lists, stacks, queues, trees, and hashing.",
            "lectureno": 3,
            "duration": 1,
            "instructor_name": "Dr. Meena",
            "start_hr": "09",
            "end_hr": "16",
        },
        {
            "name": "Algorithms",
            "description": "Greedy, divide-and-conquer, dynamic programming, and graph algorithms.",
            "lectureno": 3,
            "duration": 1,
            "instructor_name": "Prof. Arjun",
            "start_hr": "09",
            "end_hr": "16",
        },
        {
            "name": "Database Systems",
            "description": "Relational algebra, SQL, normalization, indexing, and transaction basics.",
            "lectureno": 2,
            "duration": 1,
            "instructor_name": "Dr. Kavya",
            "start_hr": "09",
            "end_hr": "16",
        },
        {
            "name": "Operating Systems",
            "description": "Processes, threads, scheduling, synchronization, and memory management.",
            "lectureno": 2,
            "duration": 1,
            "instructor_name": "Prof. Raghav",
            "start_hr": "09",
            "end_hr": "16",
        },
        {
            "name": "Computer Networks",
            "description": "OSI/TCP-IP layers, routing, switching, transport protocols, and network security.",
            "lectureno": 2,
            "duration": 1,
            "instructor_name": "Dr. Priya",
            "start_hr": "09",
            "end_hr": "16",
        },
        {
            "name": "Software Engineering",
            "description": "SDLC, requirements, design patterns, testing, and agile development practices.",
            "lectureno": 2,
            "duration": 1,
            "instructor_name": "Prof. Nitin",
            "start_hr": "09",
            "end_hr": "16",
        },
    ]

    constraints = {
        "working_days": [
            {"day": "Monday", "start_hr": "09", "end_hr": "16", "total_hours": "7"},
            {"day": "Tuesday", "start_hr": "09", "end_hr": "16", "total_hours": "7"},
            {"day": "Wednesday", "start_hr": "09", "end_hr": "16", "total_hours": "7"},
            {"day": "Thursday", "start_hr": "09", "end_hr": "16", "total_hours": "7"},
            {"day": "Friday", "start_hr": "09", "end_hr": "16", "total_hours": "7"},
        ],
        "consecutive_subjects": ["Data Structures", "Algorithms"],
        "non_consecutive_subjects": ["Operating Systems", "Computer Networks"],
        "day_course_map": {
            "Monday": {"name": "Data Structures", "description": "Weekly focus day for core DS concepts."},
            "Tuesday": {"name": "Algorithms", "description": "Problem-solving intensive day."},
        },
    }

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM courses;")
            cur.execute("DELETE FROM constraints;")

            for course in courses:
                cur.execute(
                    """
                    INSERT INTO courses (name, description, lectureno, duration, instructor_name, start_hr, end_hr)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        course["name"],
                        course["description"],
                        course["lectureno"],
                        course["duration"],
                        course["instructor_name"],
                        course["start_hr"],
                        course["end_hr"],
                    ),
                )

            cur.execute(
                """
                INSERT INTO constraints (working_days, consecutive_subjects, non_consecutive_subjects, day_course_map)
                VALUES (%s, %s, %s, %s);
                """,
                (
                    Json(constraints["working_days"]),
                    Json(constraints["consecutive_subjects"]),
                    Json(constraints["non_consecutive_subjects"]),
                    Json(constraints["day_course_map"]),
                ),
            )
        conn.commit()

    print("Seeded CS mock timetable data into PostgreSQL.")
    print(f"Courses inserted: {len(courses)}")
    print("Constraints inserted: 1")


if __name__ == "__main__":
    seed_cs_mock_data()
