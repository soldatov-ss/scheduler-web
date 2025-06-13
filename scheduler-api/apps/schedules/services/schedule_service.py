from collections import defaultdict
from datetime import datetime
from typing import Any, DefaultDict
from ..enums import WeekdayEnum
from ..models import Schedule, TimeSlot

class ScheduleService:

    @staticmethod
    def validate_time_slot(start_str: str, stop_str: str) -> None:
        """Validate that start time is before stop time."""
        start_time = datetime.strptime(start_str, '%H:%M').time()
        stop_time = datetime.strptime(stop_str, '%H:%M').time()

        if start_time >= stop_time:
            raise ValueError("Start time must be before stop time")

    @staticmethod
    def validate_schedule_structure(schedule_data: dict[str, list[dict[str, Any]]]) -> None:
        """Validate the structure of the schedule data."""
        valid_weekdays = {day.value for day in WeekdayEnum}

        for weekday, slots in schedule_data.items():
            if weekday.lower() not in valid_weekdays:
                raise ValueError(
                    f"Invalid weekday '{weekday}'. Must be one of: {sorted(valid_weekdays)}"
                )

            if not isinstance(slots, list):
                raise ValueError(f"Slots for {weekday} must be a list")

            # Validate no overlapping time slots for the same day
            sorted_slots = sorted(slots, key=lambda x: x['start'])
            for i in range(len(sorted_slots) - 1):
                current_stop = datetime.strptime(sorted_slots[i]['stop'], '%H:%M').time()
                next_start = datetime.strptime(sorted_slots[i + 1]['start'], '%H:%M').time()

                if current_stop > next_start:
                    raise ValueError(
                        f"Overlapping time slots found on {weekday}: "
                        f"{sorted_slots[i]['start']}-{sorted_slots[i]['stop']} and "
                        f"{sorted_slots[i + 1]['start']}-{sorted_slots[i + 1]['stop']}"
                    )

    @staticmethod
    def create_time_slots_for_schedule(schedule: Schedule, schedule_data: dict[str, list[dict[str, Any]]]) -> None:
        """Create time slots for a schedule from the given data."""
        time_slots_to_create: list[TimeSlot] = []

        for weekday_name, slots in schedule_data.items():
            weekday = WeekdayEnum(weekday_name.lower())
            weekday_num = weekday.number

            for slot_data in slots:
                start_time = datetime.strptime(slot_data["start"], "%H:%M").time()
                end_time = datetime.strptime(slot_data["stop"], "%H:%M").time()

                time_slots_to_create.append(
                    TimeSlot(
                        schedule=schedule,
                        weekday=weekday_num,
                        start_time=start_time,
                        end_time=end_time,
                        ids=slot_data["ids"],
                    )
                )

        TimeSlot.objects.bulk_create(time_slots_to_create)


    @staticmethod
    def get_schedule_dict(schedule: Schedule) -> defaultdict[str, list[dict[str, Any]]]:
        """Convert a Schedule object to a dictionary representation."""
        schedule_dict = defaultdict(list)
        time_slots = schedule.time_slots.order_by('weekday', 'start_time').all()

        for slot in time_slots:
            weekday = WeekdayEnum.from_number(slot.weekday)
            schedule_dict[weekday.value].append({
                'start': slot.start_time.strftime('%H:%M'),
                'stop': slot.end_time.strftime('%H:%M'),
                'ids': slot.ids
            })

        return schedule_dict

schedule_service = ScheduleService()
