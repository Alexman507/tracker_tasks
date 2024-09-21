from rest_framework import serializers
from rest_framework.permissions import IsAdminUser

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
        permission_classes = [IsAdminUser]


class UserListSerializer(serializers.ModelSerializer):
    # full_fio = serializers.CharField(source='get_full_fio')
    full_name = serializers.CharField(source='get_short_fio')

    class Meta:
        model = User
        fields = ["full_name", "email"]
        permission_classes = [IsAdminUser]

