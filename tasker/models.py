from django.db import models
from users.models import User

import pghistory

NULLABLE = {"null": True, "blank": True}


@pghistory.track(
    pghistory.Event('user.create'),
    fields=['username']
)
class Task(models.Model):
    """
    Модель Задача

    Поля
        - name: Наименование
        - tag: Тэг (тип) задачи
        - parent_task: Ссылка на родительскую задачу (если есть зависимость)
        - executor: Исполнитель
        - deadline: Срок
        - status: Статус
        - responsible_manager: Ответственный за выполнение
        - priority: Приоритет
        - notes: Примечание
        - version: Версия
        - updated_at: Дата обновления
    """
    name = models.CharField(max_length=255)
    parent_task = models.ForeignKey(
        "self", on_delete=models.SET_NULL, **NULLABLE
    )
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=100)
    responsible_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Ответственный за выполнение",
    )
    priority = models.PositiveSmallIntegerField(default=3)
    notes = models.TextField(**NULLABLE)
    version = models.AutoField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
