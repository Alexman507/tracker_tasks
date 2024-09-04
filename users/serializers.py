from rest_framework import serializers
from rest_framework.permissions import IsAdminUser

from tasker.serializers import TaskSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class BusyUserSerializer(serializers.ModelSerializer):
    short_fio = serializers.CharField(source='short_fio',)
    task = TaskSerializer(read_only=True)
    executor_task_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["short_fio", "task"]
        permission_classes = [IsAdminUser]

    def get_executor_task_count(self, obj):
        return obj.task_set.count()
