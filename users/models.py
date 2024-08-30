from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    first_name = models.CharField(verbose_name="Имя", max_length=50)
    last_name = models.CharField(verbose_name="Фамилия", max_length=50)
    patronymic = models.CharField(verbose_name="Отчество", max_length=50, **NULLABLE)
    birthday = models.DateField(verbose_name="Дата рождения", **NULLABLE)


    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="Аватар", **NULLABLE
    )

    tg_chat_id = models.CharField(
        max_length=50, verbose_name="Телеграм chat-id", **NULLABLE
    )

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
        full_fio = "%s %s %s" % (self.last_name, self.first_name, self.patronymic)
        return full_fio.strip()

    def __get_i(self):
        """Возвращает первую букву фамилии."""
        short_name = ("%s" % self.first_name)[0]
        return short_name.strip()

    def __get_p(self):
        """Возвращает первую букву отчества."""
        short_patronymic = ("%s" % self.patronymic)[0]
        return short_patronymic.strip()

    def get_short_fio(self):
        """Возвращает фамилию и инициалы сотрудника."""
        full_fio = "%s %s.%s." % (self.last_name, self.__get_i(), self.__get_p())
        return full_fio.strip()
