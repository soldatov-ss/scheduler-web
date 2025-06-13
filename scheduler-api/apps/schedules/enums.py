from enum import Enum, unique

@unique
class WeekdayEnum(Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

    @property
    def number(self) -> int:
        mapping = {
            WeekdayEnum.MONDAY: 0,
            WeekdayEnum.TUESDAY: 1,
            WeekdayEnum.WEDNESDAY: 2,
            WeekdayEnum.THURSDAY: 3,
            WeekdayEnum.FRIDAY: 4,
            WeekdayEnum.SATURDAY: 5,
            WeekdayEnum.SUNDAY: 6,
        }
        return mapping[self]

    @classmethod
    def from_number(cls, number: int) -> 'WeekdayEnum':
        mapping = {
            0: WeekdayEnum.MONDAY,
            1: WeekdayEnum.TUESDAY,
            2: WeekdayEnum.WEDNESDAY,
            3: WeekdayEnum.THURSDAY,
            4: WeekdayEnum.FRIDAY,
            5: WeekdayEnum.SATURDAY,
            6: WeekdayEnum.SUNDAY,
        }
        return mapping[number]
