from django.db import models
from users.models import User

import pghistory

NULLABLE = {"null": True, "blank": True}


@pghistory.track()
class Task(models.Model):
    """
    Модель Задача

    Поля
        - name: Наименование
        - tag: Тэг (тип) задачи (список)
        - parent_task: Ссылка на родительскую задачу (если есть зависимость)
        - executor: Исполнитель
        - deadline: Срок
        - status: Статус (список)
        - responsible_manager: Ответственный за выполнение
        - priority: Приоритет
        - is_active: Boolean (default=false)
        - notes: Примечание
        - updated_at: Дата обновления
        - is_important: Boolean (if parent_task)
    """
    TAG_CHOICES = [
        ("purchase", "Закупка"),
        ("spare parts", "Запчасти"),
        ("modification", "Модификация"),
        ("service", "Обслуживание"),
        ("education", "Обучение"),
        ("offer", "Предложение"),
        ("development", "Разработка"),
    ]

    STATUS_CHOICES = [
        ("open", "Открыто"),
        ("in progress", "В процессе"),
        ("closed", "Закрыто"),
        ("delayed", "Задержано"),
    ]

    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, **NULLABLE)
    parent_task = models.ForeignKey(
        "self", on_delete=models.CASCADE, **NULLABLE
    )
    executor = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, related_name="executors")
    deadline = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    responsible_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Ответственный за выполнение",
        related_name="responsibles"
    )
    priority = models.PositiveSmallIntegerField(default=3)
    is_active = models.BooleanField(default=False)
    notes = models.TextField(**NULLABLE)
    updated_at = models.DateTimeField(auto_now=True)
    is_important = models.BooleanField(default=False, )
