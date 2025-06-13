from collections import defaultdict
from datetime import datetime

from django.db import transaction
from rest_framework import serializers
from .models import TimeSlot, Schedule


class TimeSlotCreateSerializer(serializers.Serializer):
    start = serializers.RegexField(
        regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',
        help_text="Start time in HH:MM format"
    )
    stop = serializers.RegexField(
        regex=r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',
        help_text="Stop time in HH:MM format"
    )
    ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of integer IDs"
    )

    def validate(self, data):
        start_str = data['start']
        stop_str = data['stop']

        start_time = datetime.strptime(start_str, '%H:%M').time()
        stop_time = datetime.strptime(stop_str, '%H:%M').time()

        if start_time >= stop_time:
            raise serializers.ValidationError("Start time must be before stop time")

        return data


class WeeklyScheduleSerializer(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'schedule', 'created', 'modified', 'is_active']
        read_only_fields = ['id', 'created', 'modified']

    def get_schedule(self, obj):
        weekdays_map = {
            0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday',
            4: 'friday', 5: 'saturday', 6: 'sunday'
        }

        schedule_dict = defaultdict(list)
        time_slots = obj.time_slots.order_by('weekday', 'start_time').all()

        for slot in time_slots:
            weekday_name = weekdays_map[slot.weekday]
            schedule_dict[weekday_name].append({
                'start': slot.start_time.strftime('%H:%M'),
                'stop': slot.end_time.strftime('%H:%M'),
                'ids': slot.ids
            })

        return schedule_dict



class WeeklyScheduleCreateUpdateSerializer(serializers.ModelSerializer):
    schedule = serializers.DictField(
        child=serializers.ListField(
            child=TimeSlotCreateSerializer()
        ),
        help_text="Weekly schedule with time slots for each day"
    )

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'schedule', 'is_active']
        read_only_fields = ['id']

    def validate_schedule(self, value):
        """Validate the schedule structure"""
        valid_weekdays = ['monday', 'tuesday', 'wednesday', 'thursday',
                          'friday', 'saturday', 'sunday']

        for weekday, slots in value.items():
            if weekday.lower() not in valid_weekdays:
                raise serializers.ValidationError(
                    f"Invalid weekday '{weekday}'. Must be one of: {valid_weekdays}"
                )

            if not isinstance(slots, list):
                raise serializers.ValidationError(
                    f"Slots for {weekday} must be a list"
                )

            # Validate no overlapping time slots for the same day
            sorted_slots = sorted(slots, key=lambda x: x['start'])
            for i in range(len(sorted_slots) - 1):
                current_stop = datetime.strptime(sorted_slots[i]['stop'], '%H:%M').time()
                next_start = datetime.strptime(sorted_slots[i + 1]['start'], '%H:%M').time()

                if current_stop > next_start:
                    raise serializers.ValidationError(
                        f"Overlapping time slots found on {weekday}: "
                        f"{sorted_slots[i]['start']}-{sorted_slots[i]['stop']} and "
                        f"{sorted_slots[i + 1]['start']}-{sorted_slots[i + 1]['stop']}"
                    )

        return value

    @transaction.atomic
    def create(self, validated_data):
        schedule_data = validated_data.pop('schedule')
        schedule = Schedule.objects.create(**validated_data)

        self._create_time_slots_with_series(schedule, schedule_data)
        return schedule

    @transaction.atomic
    def update(self, instance, validated_data):
        schedule_data = validated_data.pop('schedule', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if schedule_data is not None:
            instance.time_slots.all().delete()
            self._create_time_slots_with_series(instance, schedule_data)
        return instance

    def _create_time_slots_with_series(self, schedule, schedule_data):
        weekday_mapping = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }

        time_slots_to_create = []

        for weekday_name, slots in schedule_data.items():
            weekday_num = weekday_mapping[weekday_name.lower()]

            for slot_data in slots:
                start_time = datetime.strptime(slot_data['start'], '%H:%M').time()
                end_time = datetime.strptime(slot_data['stop'], '%H:%M').time()

                time_slots_to_create.append(TimeSlot(
                    schedule=schedule,
                    weekday=weekday_num,
                    start_time=start_time,
                    end_time=end_time,
                    ids=slot_data['ids']
                ))
        TimeSlot.objects.bulk_create(time_slots_to_create)

    def to_representation(self, instance):
        return WeeklyScheduleSerializer(instance, context=self.context).data
