from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

from django.conf import settings
from rest_framework import renderers, serializers
from phonenumber_field.serializerfields import PhoneNumberField

class PhoneNumberSerializer(serializers.Serializer):
    number = PhoneNumberField(region="RU")