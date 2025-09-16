# Schedule-Based Randomization Factor

This module provides a utility for calculating a randomization factor based on a time-based schedule. It is designed to help systems make probabilistic decisions about whether to perform an action during a given time window, using a normalized factor derived from the schedule.

## Features

- **Schedule Representation**: Define schedules for specific weekdays and time ranges.
- **Randomization Factor Calculation**: Compute a float value representing the likelihood of performing an action, based on the current time and the defined schedule.
- **Configurable Baseline**: Easily adjust minimum and maximum values for the randomization factor.

## How It Works

1. **Schedule Definition**  
   The schedule is represented as a list of `ScheduleEntry` objects, each specifying:
   - `weekday`: Integer (Monday=1, Sunday=7)
   - `start_hour`: Integer (0-23)
   - `end_hour`: Integer (0-23)

2. **Randomization Factor Calculation**  
   The `calculate_randomization_factor` function checks:
   - If a schedule is provided and the schedule check is enabled.
   - If today matches any entry in the schedule.
   - If the current hour is within the scheduled time window.

   If all conditions are met, it calculates the difference between `end_hour` and `start_hour`, normalizes it to a 0-1 scale, and computes the randomization factor using the formula:

   $$
   \text{factor} = \text{BASELINE\_MAX} - (\text{normalized} \times (\text{BASELINE\_MAX} - \text{BASELINE\_MIN}))
   $$

   If any condition fails, the function returns `-1.0` to indicate that no action should be taken.

## Example Usage

```python
from typing import List

class ScheduleEntry:
    def __init__(self, weekday: int, start_hour: int, end_hour: int):
        self.weekday = weekday  # Monday=1, Sunday=7
        self.start_hour = start_hour
        self.end_hour = end_hour

schedule = [
    ScheduleEntry(weekday=1, start_hour=9, end_hour=17),  # Monday, 9am-5pm
    ScheduleEntry(weekday=3, start_hour=8, end_hour=12),  # Wednesday, 8am-12pm
]

factor = calculate_randomization_factor(schedule=schedule, schedule_check=True)
if factor != -1.0:
    print(f"Action allowed. Randomization factor: {factor}")
else:
    print("Action not allowed at this time.")
