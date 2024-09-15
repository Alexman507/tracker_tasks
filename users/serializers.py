from rest_framework import serializers
from rest_framework.permissions import IsAdminUser

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
        permission_classes = [IsAdminUser]

class BusyUserSerializer(serializers.ModelSerializer):
    """Запрашивает из БД список сотрудников и их задачи, отсортированный по количеству активных задач"""
    short_fio = serializers.CharField(source='get_short_fio')

    class Meta:
        model = User
        fields = ["short_fio", "position", "email", "tasks"]
        permission_classes = [IsAdminUser]



class UserListSerializer(serializers.ModelSerializer):
    # full_fio = serializers.CharField(source='get_full_fio')
    short_fio = serializers.CharField(source='get_short_fio')

    class Meta:
        model = User
        fields = ["short_fio", "email"]
        permission_classes = [IsAdminUser]

