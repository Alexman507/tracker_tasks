from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from tasker.models import Task
from tasker.paginations import TaskPaginator
from tasker.permissions import IsOwner
from tasker.serializers import TaskSerializer, FreeExecutorsListSerializer, ImportantTaskListSerializer
from users.models import User


# TaskerViewSet, PublicTaskerListAPIView
@method_decorator(
    name="list", decorator=swagger_auto_schema(operation_description="Список задач")
)
class TaskerViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = TaskPaginator
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ("executors",)
    ordering_fields = ("deadline", "updated_at",)

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.user = self.request.user
        new_task.save()



class PublicTaskerListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(priority=1)
    pagination_class = TaskPaginator

    def get_queryset(self):
        return Task.objects.filter(executors=self.request.user.pk).order_by("id")


class FreeImportantTaskerListAPIView(generics.ListAPIView):
    """Запрашивает из БД задачи, которые не взяты в работу,
    но от которых зависят другие задачи, взятые в работу."""
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(parent_task__isnull=False, executors=None)


class FreeExecutorsAPIView(generics.ListAPIView):
    """
    Реализует поиск по сотрудникам, которые могут взять такие задачи
    (наименее загруженный сотрудник или сотрудник, выполняющий родительскую задачу,
    если ему назначено максимум на 2 задачи больше, чем у наименее загруженного сотрудника).
    """
    serializer_class = FreeExecutorsListSerializer

    def get_queryset(self):
        user_min_task = User.objects.all().annotate(task_count=Count('tasks')).order_by('task_count').first()
        task_parent = Task.objects.filter(parent_task__isnull=False, executors=None).first()
        user_task_parent = User.objects.filter(tasks__id=task_parent.id).first()
        count_user_task_parent = len(list(user_task_parent.tasks.all()))
        count_user_min_task = len(list(user_min_task.tasks.all()))
        if count_user_task_parent - count_user_min_task <= 2:
            queryset = User.objects.filter(pk=user_task_parent.pk)
        else:
            queryset = User.objects.filter(pk=user_min_task.pk)

        return queryset


class ImportantTasksListAPIView(generics.ListAPIView):
    """Возвращает список объектов в формате: `{Важная задача, Срок, [ФИО сотрудника]}`"""
    serializer_class = ImportantTaskListSerializer
    queryset = Task.objects.filter(parent_task__isnull=False)

