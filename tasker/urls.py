from django.urls import path

from tasker.apps import TaskerConfig
from rest_framework.routers import SimpleRouter

from tasker.views import TaskerViewSet, PublicTaskerListAPIView, \
    FreeImportantTaskerListAPIView, ImportantTasksListAPIView

app_name = TaskerConfig.name

router = SimpleRouter()
router.register("", TaskerViewSet, basename="tasker")

urlpatterns = [
    path("public/", PublicTaskerListAPIView.as_view(), name="public"),
    path("free/", FreeImportantTaskerListAPIView.as_view(), name="free"),
    path("list/", ImportantTasksListAPIView.as_view(), name="list"),
] + router.urls
