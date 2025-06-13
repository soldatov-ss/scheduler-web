from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Schedule
from .serializers import (
    WeeklyScheduleSerializer,
    WeeklyScheduleCreateUpdateSerializer
)


class WeeklyScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().prefetch_related('time_slots')
    serializer_class = WeeklyScheduleSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'is_active', 'created']
    search_fields = ['name', ]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return WeeklyScheduleCreateUpdateSerializer
        return WeeklyScheduleSerializer
