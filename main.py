from typing import List, Optional
import datetime

BASELINE_MIN = 0.1
BASELINE_MAX = 0.5

class ScheduleEntry:
    def __init__(self, weekday: int, start_hour: int, end_hour: int):
        self.weekday = weekday  # Monday=1, Sunday=7
        self.start_hour = start_hour
        self.end_hour = end_hour

def calculate_randomization_factor(
    schedule: Optional[List[ScheduleEntry]] = None,
    schedule_check: Optional[bool] = False
) -> float:
    if schedule is None or len(schedule) == 0 or not schedule_check:
        return -1.0

    today = datetime.datetime.today().isoweekday()
    current_hour = datetime.datetime.now().hour
    match = next((s for s in schedule if s.weekday == today), None)

    if match is None:
        return -1.0

    if match.start_hour > current_hour or match.end_hour < current_hour:
        return -1.0

    difference = match.end_hour - match.start_hour
    normalized = min(max(difference / 24, 0), 1)
    return (BASELINE_MAX - (normalized * (BASELINE_MAX - BASELINE_MIN))).__round__(2)
