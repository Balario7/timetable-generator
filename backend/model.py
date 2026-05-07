from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class WorkingDay(BaseModel):
    day: str
    start_hr: str
    end_hr: str
    total_hours: str

class CreateCourse(BaseModel):
    name: str
    lectureno: int
    duration: int
    instructor_name: str
    start_hr: str = "09"
    end_hr: str = "17"

class Course(CreateCourse):
    id: int

class DayCourseMapEntry(BaseModel):
    name: str
    description: str = ""

class CreateConstraint(BaseModel):
    working_days: List[WorkingDay]
    consecutive_subjects: List[str]
    non_consecutive_subjects: List[str]
    day_course_map: Optional[Dict[str, DayCourseMapEntry]] = None

class Constraint(CreateConstraint):
    id: int
