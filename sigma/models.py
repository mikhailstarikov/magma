from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название команды")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"


class Activity(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название активности")
    description = models.TextField(blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Активность"
        verbose_name_plural = "Активности"


class Employee(models.Model):
    # Связываем нашего сотрудника со стандартным пользователем Django (для логина/админки)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Команда"
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Активность",
    )

    def __str__(self):
        # Показываем имя и фамилию, если они есть, иначе логин
        return self.user.get_full_name() or self.user.username

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
