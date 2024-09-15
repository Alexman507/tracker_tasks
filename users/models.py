from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

import tasker.models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """
    Модель сотрудник (пользователь)

    Поля:
        - first_name: Имя
        - last_name: Фамилия
        - patronymic: Отчество
        - position: Должность
        - birthday: Дата рождения
        - email: email
        - avatar: Аватар
        - tg_chat_id: Телеграм chat-id

    """

    username = None
    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    patronymic = models.CharField(verbose_name="Отчество", max_length=50, **NULLABLE)
    position = models.CharField(verbose_name="Должность", max_length=50)
    birthday = models.DateField(verbose_name="Дата рождения", **NULLABLE)
    email = models.EmailField(unique=True, verbose_name="email",
                              validators=[
                                  EmailValidator(message='При регистрации допускается только домен osnova-3d',
                                                 allowlist='osnova-3d.ru')])
    phone = PhoneNumberField(**NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", **NULLABLE
    )

    tg_chat_id = models.CharField(
        max_length=50, verbose_name="Телеграм chat-id", **NULLABLE
    )
    tasks = models.ManyToManyField(to="tasker.Task", related_name="tasks", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    def get_full_fio(self):
        """
        Возвращает Фамилию, Имя и Отчество с пробелом между ними.
        """
        if self.patronymic:
            full_fio = "%s %s %s" % (self.last_name, self.first_name, self.patronymic)
        else:
            full_fio = "%s %s" % (self.last_name, self.first_name)
        return full_fio.strip()

    def __get_i(self):
        """Возвращает первую букву фамилии."""
        short_name = ("%s" % self.first_name)[0]
        return short_name.strip()

    def __get_p(self):
        """Возвращает первую букву отчества."""
        if self.patronymic:
            short_patronymic = ("%s" % self.patronymic)[0]
            return short_patronymic.strip()
        return ""

    def get_short_fio(self):
        """Возвращает фамилию и инициалы сотрудника."""
        if not self.patronymic:
            short_fio = "%s %s." % (self.last_name, self.__get_i())
        else:
            short_fio = "%s %s.%s." % (self.last_name, self.__get_i(), self.__get_p())
        return short_fio.strip()
