"""
Simple and Fast Timetable Generator - Greedy Algorithm
Replaces slow CSP solver with efficient greedy scheduling
"""
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


def generate(constraints, courses) -> Dict[str, List]:
    """
    Generate timetable using a fast greedy algorithm.
    Simple but effective approach that always produces a result.
    """
    
    # Initialize response with empty lists for each day
    resp_data = {
        'monday': [], 'tuesday': [], 'wednesday': [],
        'thursday': [], 'friday': [], 'saturday': [], 'sunday': []
    }
    
    # Map day names for API response
    day_mapping = {
        'Monday': 'monday',
        'Tuesday': 'tuesday',
       'Wednesday': 'wednesday',
        'Thursday': 'thursday',
        'Friday': 'friday',
        'Saturday': 'saturday',
        'Sunday': 'sunday'
    }
    
    # Calculate hours needed for each subject
    subject_hours = {}
    course_meta = {}
    for course in courses:
        total_hours = course['lectureno'] * course['duration']
        subject_hours[course['name']] = total_hours
        course_meta[course['name']] = {
            'description': course.get('description', ''),
            'instructor_name': course.get('instructor_name', ''),
        }
    
    logger.info(f"Total subjects: {len(subject_hours)}")
    logger.info(f"Total hours needed: {sum(subject_hours.values())}")
    
    # Track scheduled hours
    scheduled_hours = {subject: 0 for subject in subject_hours}
    
    # Build available time slots for each day
    all_slots = []  # (day_key, hour, start_time, end_time)
    day_slots = {k: [] for k in resp_data.keys()}
    
    for day_info in constraints['working_days']:
        day_name = day_info['day']
        day_key = day_mapping.get(day_name, day_name.lower())
        start_hr = int(day_info['start_hr'])
        end_hr = int(day_info['end_hr'])
        
        # Create slots for this day
        for hour in range(start_hr, end_hr):
            start_time = f'2018-02-25T{str(hour).zfill(2)}:00:00'
            end_time = f'2018-02-25T{str(hour+1).zfill(2)}:00:00'
            all_slots.append((day_key, hour, start_time, end_time))
            day_slots[day_key].append((day_key, hour, start_time, end_time))
    
    logger.info(f"Total available slots: {len(all_slots)}")
    
    # Apply day-specific preferred courses first and mark them as highlights.
    preferred_map = constraints.get('day_course_map', {}) or {}
    for raw_day, pref in preferred_map.items():
        day_key = day_mapping.get(raw_day, raw_day.lower())
        if day_key not in day_slots:
            continue
        preferred_subject = (pref.get('name') or '').strip()
        if not preferred_subject:
            continue
        if preferred_subject not in subject_hours:
            continue
        remaining = subject_hours[preferred_subject] - scheduled_hours[preferred_subject]
        if remaining <= 0:
            continue
        if not day_slots[day_key]:
            continue

        _, hour, start_time, end_time = day_slots[day_key].pop(0)
        all_slots = [slot for slot in all_slots if not (slot[0] == day_key and slot[1] == hour)]
        resp_data[day_key].append({
            'id': 1,
            'name': preferred_subject,
            'description': pref.get('description', course_meta.get(preferred_subject, {}).get('description', '')),
            'instructor_name': course_meta.get(preferred_subject, {}).get('instructor_name', ''),
            'type': 'custom',
            'startTime': start_time,
            'endTime': end_time,
            'highlight': True,
            'highlight_reason': f'Preferred course for {raw_day}',
        })
        scheduled_hours[preferred_subject] += 1

    # Greedy scheduling: sort subjects by hours needed (largest first)
    sorted_subjects = sorted(subject_hours.items(), key=lambda x: x[1], reverse=True)
    slot_index = 0
    
    # Assign subjects to slots in round-robin fashion
    for subject, hours_needed in sorted_subjects:
        hours_assigned = 0
        
        # Try to assign all needed hours
        while hours_assigned < hours_needed and slot_index < len(all_slots):
            day_key, hour, start_time, end_time = all_slots[slot_index]
            
            # Add this slot to the schedule
            resp_data[day_key].append({
                'id': 1,
                'name': subject,
                'description': course_meta.get(subject, {}).get('description', ''),
                'instructor_name': course_meta.get(subject, {}).get('instructor_name', ''),
                'type': 'custom',
                'startTime': start_time,
                'endTime': end_time,
                'highlight': False,
                'highlight_reason': '',
            })
            
            scheduled_hours[subject] += 1
            hours_assigned += 1
            slot_index += 1
    
    # Log results
    total_scheduled = sum(len(day) for day in resp_data.values())
    total_needed = sum(subject_hours.values())
    
    logger.info(f"Scheduled {total_scheduled} out of {total_needed} hours")
    
    for subject, needed in subject_hours.items():
        scheduled = scheduled_hours[subject]
        logger.info(f"  {subject}: {scheduled}/{needed} hours")
    
    return resp_data
