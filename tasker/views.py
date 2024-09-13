from django.shortcuts import render
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

from tasker.models import Task
from tasker.paginations import TaskPaginator
from tasker.permissions import IsOwner
from tasker.serializers import TaskSerializer, FreeExecutorsListSerializer, ImportantTaskListSerializer


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
    search_fields = ("executor",)
    ordering_fields = ("deadline", "updated_at",)

    def get_queryset(self):
        return Task.objects.filter(executor=self.request.user.pk).order_by("id")

    def perform_create(self, serializer):
        new_task = serializer.save()
        new_task.user = self.request.user
        new_task.save()


class PublicTaskerListAPIView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(priority=1)
    pagination_class = TaskPaginator


class FreeImportantTaskerListAPIView(generics.ListAPIView):
    """Запрашивает из БД задачи, которые не взяты в работу,
    но от которых зависят другие задачи, взятые в работу."""
    serializer_class = TaskSerializer
    queryset = Task.objects.filter(parent_task=True, executor=None)


class FreeExecutorsListAPIView(generics.ListAPIView):
    """
    Реализует поиск по сотрудникам, которые могут взять такие задачи
    (наименее загруженный сотрудник или сотрудник, выполняющий родительскую задачу,
    если ему назначено максимум на 2 задачи больше, чем у наименее загруженного сотрудника).
    """
    queryset = Task.objects.filter(parent_task=True)
    serializer_class = FreeExecutorsListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ("executor",)
    ordering_fields = ("deadline", "updated_at",)


class ImportantTasksListAPIView(generics.ListAPIView):
    """Возвращает список объектов в формате: `{Важная задача, Срок, [ФИО сотрудника]}`"""
    serializer_class = ImportantTaskListSerializer
    queryset = Task.objects.filter(parent_task=True)
