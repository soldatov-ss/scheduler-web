from .services import schedule_service
from django.db import transaction
from rest_framework import serializers
from .models import Schedule


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
        try:
            schedule_service.validate_time_slot(data['start'], data['stop'])
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return data


class WeeklyScheduleSerializer(serializers.ModelSerializer):
    schedule = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['id', 'name', 'description', 'schedule', 'created', 'modified', 'is_active']
        read_only_fields = ['id', 'created', 'modified']

    def get_schedule(self, obj):
        return schedule_service.get_schedule_dict(obj)


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
        try:
            schedule_service.validate_schedule_structure(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return value

    @transaction.atomic
    def create(self, validated_data):
        schedule_data = validated_data.pop('schedule')
        schedule = Schedule.objects.create(**validated_data)

        schedule_service.create_time_slots_for_schedule(schedule, schedule_data)
        return schedule

    @transaction.atomic
    def update(self, instance, validated_data):
        schedule_data = validated_data.pop('schedule', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if schedule_data is not None:
            instance.time_slots.all().delete()
            schedule_service.create_time_slots_for_schedule(instance, schedule_data)
        return instance

    def to_representation(self, instance):
        return WeeklyScheduleSerializer(instance, context=self.context).data
