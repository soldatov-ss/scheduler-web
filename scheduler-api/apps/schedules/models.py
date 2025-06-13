from django.contrib.postgres.fields import ArrayField
from django.db import models
from model_utils.models import TimeStampedModel
from rest_framework.exceptions import ValidationError


class Schedule(TimeStampedModel):
    name = models.CharField(max_length=100, help_text="Name/description of the schedule")
    description = models.TextField(blank=True, help_text="Optional description")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'schedules'
        ordering = ['-created']

    def __str__(self):
        return f"Schedule({self.id}): {self.name}"


class TimeSlot(TimeStampedModel):
    WEEKDAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='time_slots'
    )
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField(help_text="Start time for this slot")
    end_time = models.TimeField(help_text="End time for this slot")
    ids = ArrayField(
        models.IntegerField(),
        size=None,
        default=list,
        help_text="Array of IDs associated with this time slot"
    )

    class Meta:
        db_table = 'time_slots'
        ordering = ['weekday', 'start_time']

    def __str__(self):
        weekday_name = dict(self.WEEKDAYS)[self.weekday]
        return f"{weekday_name}: {self.start_time}-{self.end_time}"

    def clean(self):
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("Start time must be before end time")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @property
    def weekday_name(self):
        return dict(self.WEEKDAYS)[self.weekday].lower()



class TimeSlotSeries(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=TimeSlot.WEEKDAYS)
    time_point = models.TimeField()
    ids = ArrayField(models.IntegerField(), default=list)

    class Meta:
        db_table = 'time_slot_series'
        unique_together = ['schedule', 'weekday', 'time_point']
