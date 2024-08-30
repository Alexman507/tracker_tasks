from django.db import models

from users.models import User

# - Наименование
# - Ссылка на родительскую задачу (если есть зависимость)
# - Исполнитель
# - Срок
# - Статус
# - Ответственный за выполнение
# - Ответственный за выполнение

NULLABLE = {"null": True, "blank": True}


class Task(models.Model):
    name = models.CharField(max_length=255)
    parent_task = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    executor = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=100)
    responsible_manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Ответственный за выполнение",
    )

