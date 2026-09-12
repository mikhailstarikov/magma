from django.db import models
from sigma.models import Employee, Team


class PointsTransaction(models.Model):
    """Операция с баллами (начисление или списание)"""

    TRANSACTION_TYPES = [
        ("earn", "Начисление"),
        ("spend", "Списание"),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Команда")
    transaction_type = models.CharField(
        max_length=10, choices=TRANSACTION_TYPES, verbose_name="Тип операции"
    )
    points = models.IntegerField(verbose_name="Количество баллов")
    description = models.TextField(blank=True, verbose_name="Описание операции")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата операции")

    def __str__(self):
        return f"{self.team.name} — {'+' if self.transaction_type == 'earn' else '-'}{self.points}"

    class Meta:
        verbose_name = "Операция с баллами"
        verbose_name_plural = "Операции с баллами"
        ordering = ["-created_at"]


class TeamPointsBalance(models.Model):
    """Текущий баланс баллов команды"""

    team = models.OneToOneField(
        Team, on_delete=models.CASCADE, verbose_name="Команда", unique=True
    )
    total_earned = models.IntegerField(default=0, verbose_name="Всего заработано")
    total_spent = models.IntegerField(default=0, verbose_name="Всего потрачено")
    current_balance = models.IntegerField(default=0, verbose_name="Текущий баланс")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )

    def __str__(self):
        return f"{self.team.name} — {self.current_balance} баллов"

    class Meta:
        verbose_name = "Баланс команды"
        verbose_name_plural = "Балансы команд"
