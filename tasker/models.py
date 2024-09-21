import pghistory
from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}


@pghistory.track(exclude=["executors", "responsible_manager"])
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

    name = models.CharField(max_length=100, verbose_name="наименование")
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, **NULLABLE, verbose_name="тэг")
    parent_task = models.ForeignKey("self", on_delete=models.CASCADE, **NULLABLE)
    executors = models.ManyToManyField(
        to="users.User", verbose_name="исполнители", related_name="my_tasks", blank=True
    )
    deadline = models.DateTimeField(**NULLABLE, verbose_name="срок")
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, verbose_name="статус")
    responsible_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Ответственный за выполнение",
        related_name="responsibles"
    )
    priority = models.PositiveSmallIntegerField(default=3, verbose_name="приоритет")
    is_active = models.BooleanField(default=False, verbose_name="активная")
    notes = models.TextField(**NULLABLE, verbose_name="примечание")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="дата обновления")

    def __str__(self):
        return self.name
