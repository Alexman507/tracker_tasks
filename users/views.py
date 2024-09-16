from django.db.models import Count
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from tasker.serializers import BusyUserSerializer
from users.models import User
from users.serializers import UserSerializer


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
    serializer_class = BusyUserSerializer
    queryset = User.objects.filter(tasks__id__isnull=False).annotate(task_count=Count('tasks')).order_by(
        'task_count').distinct()

