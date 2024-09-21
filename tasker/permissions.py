from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAdminUser


class IsOwner(BasePermission):
    """Проверяет, является ли пользователь создателем задачи или менеджером или администратором."""

    def has_object_permission(self, request, view, obj):
        return (
            obj.executors == request.user
            or obj.responsible_manager == request.user
            or IsAdminUser
        )
