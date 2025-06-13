from rest_framework.routers import SimpleRouter
from .views import WeeklyScheduleViewSet

app_name = "schedules"
router = SimpleRouter()

router.register(r"schedules", WeeklyScheduleViewSet, basename="users")


urlpatterns = []
urlpatterns += router.urls
