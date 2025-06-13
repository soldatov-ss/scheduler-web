from django.contrib import admin
from .models import Schedule, TimeSlot


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'is_active', 'created']
    list_filter = ['is_active', 'created']
    search_fields = ['name', 'description']


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['schedule', 'start_time', 'end_time', 'ids']
    list_filter = ['weekday', 'schedule']
    search_fields = ['schedule__name']

