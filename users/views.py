from django.db.models import Count
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tasker.models import Task
from users.models import User
from users.serializers import UserSerializer, BusyUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class BusyUserListAPIView(APIView):
    """Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач."""
    # filter_backends = [OrderingFilter]
    # ordering_fields = ["executor_task_count"]

    def get(self, request, pk):
        user_min_task = User.objects.all().annotate(task_count=Count('tasks')).order_by('task_count').first()
        task_parent = Task.objects.get(pk=pk).parent_task
        user_task_parent = User.objects.filter(tasks__id=task_parent.id).first()

        count_user_task_parent = len(list(user_task_parent.tasks.all()))
        count_user_min_task = len(list(user_min_task.tasks.all()))
        if count_user_task_parent - count_user_min_task <= 2:
            queryset = User.objects.filter(pk=user_task_parent.pk)
        else:
            queryset = User.objects.filter(pk=user_min_task.pk)

        serializer = BusyUserSerializer(queryset, many=True)

        return Response(serializer.data)
