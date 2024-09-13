from dataclasses import field

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from django.db.models import Count, Min
from rest_framework.permissions import IsAdminUser
from users.models import User
from users.serializers import UserSerializer
from tasker.models import Task
from tasker.validators import DeadlineDateValidator


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        validators = [
            DeadlineDateValidator(field="deadline"),

        ]


class BusyUserSerializer(serializers.ModelSerializer):
    """Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач"""
    short_fio = serializers.CharField(source='get_short_fio')
    tasks = TaskSerializer(read_only=True, many=True, source='executors')
    executor_task_count = serializers.SerializerMethodField()

    def get_executor_task_count(self, obj):
        count_ = 0
        if obj.parent_task:
            count_ += len(obj.parent_task)
        return count_

    class Meta:
        model = User
        fields = ["short_fio", "tasks", "executor_task_count"]
        permission_classes = [IsAdminUser]




class FreeExecutorsListSerializer(ModelSerializer):
    count_tasks = serializers.SerializerMethodField()
    min_tasks = Min(count_tasks)
    max_tasks = min_tasks + 2
    free_executors = PrimaryKeyRelatedField(
        queryset=Task.objects.filter(executor__gte=min_tasks, executor__lte=max_tasks),
        source="executor",
        read_only=False,
    )

    class Meta:
        model = Task
        fields = ["free_executors"]
        queryset = Task.objects.all()

    def get_count_tasks(self, obj):
        count_ = 0
        if obj.parent_task:
            count_ += len(obj.parent_task)
        return count_


class ImportantTaskListSerializer(ModelSerializer):
    important_tasks = TaskSerializer(read_only=True, many=True, source="parent_task", allow_null=False)
    users = UserSerializer(read_only=True)
    full_fio = serializers.CharField(source='get_full_fio')


    class Meta:
        model = Task
        fields = ["important_tasks", "deadline", "full_fio"]
