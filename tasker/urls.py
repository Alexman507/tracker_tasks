from django.urls import path

from tasker.apps import TaskerConfig
from rest_framework.routers import SimpleRouter

from tasker.views import TaskerViewSet, PublicTaskerListAPIView, FreeExecutorsListAPIView

app_name = TaskerConfig.name

router = SimpleRouter()
router.register("", TaskerViewSet, basename="tasker")

urlpatterns = [
    path("public/", PublicTaskerListAPIView.as_view(), name="public"),
    path("free/", FreeExecutorsListAPIView.as_view(), name="public"),
] + router.urls
