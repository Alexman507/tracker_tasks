from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from django.db.models import Count, Min

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


class FreeExecutorsListSerializer(ModelSerializer):
    min_tasks = User.objects.aggregate(Min(Count("parent_task"), default=0))
    max_tasks = min_tasks + 2
    free_executors = PrimaryKeyRelatedField(
        queryset=User.objects.filter(executor_task_count__gte=min_tasks, executor_task_count__lte=max_tasks),
        source="executors",
        read_only=True,
    )

    class Meta:
        model = Task
        fields = ["free_executors"]


class ImportantTaskListSerializer(ModelSerializer):
    important_tasks = Task.objects.filter(parent_task__isnull=False)
    users = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ["important_tasks", "deadline", "full_fio"]

# test commit
# test commit from git hub
