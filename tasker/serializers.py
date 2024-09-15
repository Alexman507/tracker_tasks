from dataclasses import field, fields

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from django.db.models import Count, Min, OuterRef
from rest_framework.permissions import IsAdminUser
from users.models import User
from users.serializers import UserSerializer, UserListSerializer
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
    count_tasks = serializers.SerializerMethodField()
    min_tasks = Min(count_tasks)
    max_tasks = min_tasks + 2
    free_executors = PrimaryKeyRelatedField(
        queryset=Task.objects.filter(executors__gte=min_tasks, executors__lte=max_tasks),
        source="executors",
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
    # last_name = PrimaryKeyRelatedField(
    # queryset=User.objects.all(),
    # read_only=True
    # )
    #
    important_task = serializers.CharField(read_only=True, source='name')
    user = UserListSerializer(read_only=True, source="executor")

    class Meta:
        model = Task
        fields = ["important_task", "deadline", "user"]
