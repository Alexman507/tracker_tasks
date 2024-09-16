from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from tasker.views import FreeExecutorsAPIView
from users.apps import UsersConfig
from users.views import UserViewSet, BusyUserListAPIView

app_name = UsersConfig.name
router = SimpleRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
                  path(
                      "login/",
                      TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
                      name="login",
                  ),
                  path(
                      "token/refresh/",
                      TokenRefreshView.as_view(permission_classes=(AllowAny,)),
                      name="token_refresh",
                  ),
                  path("busy/", BusyUserListAPIView.as_view(), name="busy_executors",),
                  path("free/<int:pk>/", FreeExecutorsAPIView.as_view(), name="free_executors",),

              ] + router.urls
