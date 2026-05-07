import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import psycopg2
from psycopg2.extras import Json
from psycopg2 import sql

MONGO_URI = os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017/")
MONGO_DB = os.getenv("MONGO_DB", "timetable")

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "timetable")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "hi")


def get_pg_conn():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )


def ensure_database_exists():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        dbname="postgres",
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
    )
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (POSTGRES_DB,))
            exists = cur.fetchone()
            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(POSTGRES_DB)))
    finally:
        conn.close()


def ensure_schema(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS courses (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                lectureno INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                instructor_name TEXT NOT NULL,
                start_hr TEXT NOT NULL DEFAULT '09',
                end_hr TEXT NOT NULL DEFAULT '17',
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS constraints (
                id SERIAL PRIMARY KEY,
                working_days JSONB NOT NULL,
                consecutive_subjects JSONB NOT NULL,
                non_consecutive_subjects JSONB NOT NULL,
                day_course_map JSONB NOT NULL DEFAULT '{}'::jsonb,
                created_at TIMESTAMP NOT NULL DEFAULT NOW()
            );
            """
        )
        cur.execute(
            "ALTER TABLE courses ADD COLUMN IF NOT EXISTS description TEXT NOT NULL DEFAULT '';"
        )
        cur.execute(
            "ALTER TABLE constraints ADD COLUMN IF NOT EXISTS day_course_map JSONB NOT NULL DEFAULT '{}'::jsonb;"
        )
    conn.commit()


def migrate():
    ensure_database_exists()
    mongo = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    mongo_db = mongo[MONGO_DB]
    try:
        mongo_courses = list(mongo_db.courses.find())
        mongo_constraints = list(mongo_db.constraints.find())
    except ServerSelectionTimeoutError as exc:
        mongo.close()
        raise RuntimeError(
            f"Cannot connect to MongoDB at {MONGO_URI}. Start MongoDB and rerun migration."
        ) from exc

    with get_pg_conn() as conn:
        ensure_schema(conn)
        with conn.cursor() as cur:
            cur.execute("DELETE FROM courses;")
            cur.execute("DELETE FROM constraints;")

            for course in mongo_courses:
                cur.execute(
                    """
                    INSERT INTO courses (name, description, lectureno, duration, instructor_name, start_hr, end_hr)
                    VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """,
                    (
                        course.get("name", ""),
                        course.get("description", ""),
                        int(course.get("lectureno", 0)),
                        int(course.get("duration", 0)),
                        course.get("instructor_name", ""),
                        str(course.get("start_hr", "09")),
                        str(course.get("end_hr", "17")),
                    ),
                )

            for constraint in mongo_constraints:
                cur.execute(
                    """
                    INSERT INTO constraints (working_days, consecutive_subjects, non_consecutive_subjects, day_course_map)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (
                        Json(constraint.get("working_days", [])),
                        Json(constraint.get("consecutive_subjects", [])),
                        Json(constraint.get("non_consecutive_subjects", [])),
                        Json(constraint.get("day_course_map", {})),
                    ),
                )
        conn.commit()

    mongo.close()
    print(f"Migrated {len(mongo_courses)} courses and {len(mongo_constraints)} constraints to PostgreSQL.")


if __name__ == "__main__":
    migrate()
