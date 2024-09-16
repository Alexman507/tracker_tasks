from rest_framework import serializers
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import ModelSerializer
from users.models import User
from users.serializers import UserListSerializer
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
    class Meta:
        model = User
        exclude = ["password", "is_superuser", "is_staff"]
        queryset = User.objects.all()


class ImportantTaskListSerializer(ModelSerializer):
    # last_name = PrimaryKeyRelatedField(
    # queryset=User.objects.all(),
    # read_only=True
    # )
    #
    important_task = serializers.CharField(read_only=True, source='name')
    executors = UserListSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ["important_task", "deadline", "executors"]

class BusyUserSerializer(serializers.ModelSerializer):
    """Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач"""
    short_fio = serializers.CharField(source='get_short_fio')
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ["short_fio", "position", "email", "tasks"]
        permission_classes = [IsAdminUser]