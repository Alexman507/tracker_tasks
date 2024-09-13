from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from users.models import User
from users.serializers import UserSerializer
from tasker.serializers import BusyUserSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class BusyUserListAPIView(ListAPIView):
    """Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач."""
    queryset = User.objects.all()
    serializer_class = BusyUserSerializer
    # filter_backends = [OrderingFilter]
    # ordering_fields = ["executor_task_count"]
