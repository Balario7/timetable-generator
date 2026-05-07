from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from starlette.responses import HTMLResponse
from csp import generate
from model import Constraint, Course, CreateConstraint, CreateCourse
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import os
import uvicorn
import logging
from contextlib import contextmanager
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# PostgreSQL Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "database": os.getenv("DB_NAME", "timetable_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "hi"),
}

@contextmanager
def get_conn():
    """Get a PostgreSQL connection context manager"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def initialize_database():
    """Initialize database schema"""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS courses (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    lectureno INTEGER NOT NULL,
                    duration INTEGER NOT NULL,
                    instructor_name TEXT NOT NULL,
                    start_hr TEXT NOT NULL DEFAULT '09',
                    end_hr TEXT NOT NULL DEFAULT '17',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS constraints (
                    id SERIAL PRIMARY KEY,
                    working_days TEXT NOT NULL,
                    consecutive_subjects TEXT NOT NULL,
                    non_consecutive_subjects TEXT NOT NULL,
                    day_course_map TEXT NOT NULL DEFAULT '{}',
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
        conn.commit()

# Initialize database on startup
initialize_database()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
    "http://127.0.0.1:3003",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    # Use 127.0.0.1 instead of localhost for better Windows compatibility
    uvicorn.run("app:app", host="127.0.0.1",
                port=8000, reload=True)


@app.get("/get-courses")
async def get_courses():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, lectureno, duration, instructor_name, start_hr, end_hr FROM courses ORDER BY id;")
            rows = cur.fetchall()
            courses = [
                Course(
                    id=row[0],
                    name=row[1],
                    lectureno=row[2],
                    duration=row[3],
                    instructor_name=row[4],
                    start_hr=row[5],
                    end_hr=row[6],
                )
                for row in rows
            ]
    return courses


@app.get("/get-constraints")
async def get_constraints():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, working_days, consecutive_subjects, non_consecutive_subjects, day_course_map FROM constraints ORDER BY id DESC LIMIT 1;")
            row = cur.fetchone()
            if row:
                constraint = Constraint(
                    id=row[0],
                    working_days=json.loads(row[1]) if isinstance(row[1], str) else row[1],
                    consecutive_subjects=json.loads(row[2]) if isinstance(row[2], str) else row[2],
                    non_consecutive_subjects=json.loads(row[3]) if isinstance(row[3], str) else row[3],
                    day_course_map=json.loads(row[4]) if isinstance(row[4], str) else row[4],
                )
                return [constraint]
    return []


@app.post("/add-course", response_model=Course)
async def post_course(course: CreateCourse):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO courses (name, lectureno, duration, instructor_name, start_hr, end_hr)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (
                    course.name,
                    course.lectureno,
                    course.duration,
                    course.instructor_name,
                    course.start_hr,
                    course.end_hr,
                ),
            )
            course_id = cur.fetchone()[0]
        conn.commit()
    return Course(
        id=course_id,
        name=course.name,
        lectureno=course.lectureno,
        duration=course.duration,
        instructor_name=course.instructor_name,
        start_hr=course.start_hr,
        end_hr=course.end_hr,
    )


@app.post("/add-constraints", response_model=Constraint)
async def post_constraints(constraint: CreateConstraint):
    with get_conn() as conn:
        with conn.cursor() as cur:
            # Delete all existing constraints and add the new one
            cur.execute("DELETE FROM constraints;")
            cur.execute(
                """
                INSERT INTO constraints (working_days, consecutive_subjects, non_consecutive_subjects, day_course_map)
                VALUES (%s, %s, %s, %s)
                RETURNING id
                """,
                (
                    json.dumps([wd.dict() for wd in constraint.working_days]),
                    json.dumps(constraint.consecutive_subjects),
                    json.dumps(constraint.non_consecutive_subjects),
                    json.dumps({k: v.dict() for k, v in (constraint.day_course_map or {}).items()}),
                ),
            )
            constraint_id = cur.fetchone()[0]
        conn.commit()
    return Constraint(
        id=constraint_id,
        working_days=json.loads(json.dumps([wd.dict() for wd in constraint.working_days])),
        consecutive_subjects=constraint.consecutive_subjects,
        non_consecutive_subjects=constraint.non_consecutive_subjects,
        day_course_map={k: v.dict() for k, v in (constraint.day_course_map or {}).items()} if constraint.day_course_map else {},
    )


@app.get("/generate-timetable")
async def generate_timetable():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, working_days, consecutive_subjects, non_consecutive_subjects, day_course_map FROM constraints ORDER BY id DESC LIMIT 1;")
            constraint_row = cur.fetchone()
            
            cur.execute("SELECT id, name, lectureno, duration, instructor_name, start_hr, end_hr FROM courses;")
            course_rows = cur.fetchall()

    if not constraint_row or not course_rows:
        raise HTTPException(
            status_code=400,
            detail="Please add both courses and constraints before generating the timetable."
        )

    constraints = Constraint(
        id=constraint_row[0],
        working_days=json.loads(constraint_row[1]) if isinstance(constraint_row[1], str) else constraint_row[1],
        consecutive_subjects=json.loads(constraint_row[2]) if isinstance(constraint_row[2], str) else constraint_row[2],
        non_consecutive_subjects=json.loads(constraint_row[3]) if isinstance(constraint_row[3], str) else constraint_row[3],
        day_course_map=json.loads(constraint_row[4]) if isinstance(constraint_row[4], str) else constraint_row[4],
    )

    courses = [
        Course(
            id=row[0],
            name=row[1],
            lectureno=row[2],
            duration=row[3],
            instructor_name=row[4],
            start_hr=row[5],
            end_hr=row[6],
        )
        for row in course_rows
    ]

    try:
        courses_dict = [item.dict() for item in courses]
        data = generate(constraints.dict(), courses_dict)
        return data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating timetable: {str(e)}"
        )
