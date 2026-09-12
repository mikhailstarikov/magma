from django.db import models
from django.contrib.auth.models import User
from sigma.models import Employee, Team, Activity
from django.db.models.signals import post_save
from django.dispatch import receiver


class Achievement(models.Model):
    """Шаблон ачивки — само достижение (как медаль в библиотеке)"""

    name = models.CharField(max_length=150, verbose_name="Название ачивки")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="achievements/", blank=True, null=True, verbose_name="Изображение"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ачивка"
        verbose_name_plural = "Ачивки"


class AchievementAward(models.Model):
    """Факт выдачи ачивки конкретному сотруднику"""

    achievement = models.ForeignKey(
        Achievement, on_delete=models.CASCADE, verbose_name="Ачивка"
    )
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, verbose_name="Сотрудник"
    )
    awarded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="awards_given",
        verbose_name="Кто выдал",
    )
    reason = models.TextField(blank=True, verbose_name="Основание выдачи")
    awarded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")

    def __str__(self):
        return f"{self.achievement.name} → {self.employee}"

    class Meta:
        verbose_name = "Выдача ачивки"
        verbose_name_plural = "Выдачи ачивок"
        ordering = ["-awarded_at"]


class TeamRating(models.Model):
    """Рейтинг команды в рамках конкретной активности"""

    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Команда")
    activity = models.ForeignKey(
        Activity, on_delete=models.CASCADE, verbose_name="Активность"
    )
    points = models.IntegerField(default=0, verbose_name="Баллы")
    position = models.IntegerField(default=0, verbose_name="Позиция в рейтинге")

    def __str__(self):
        return f"{self.team.name} — {self.points} баллов ({self.position} место)"

    class Meta:
        verbose_name = "Рейтинг команды"
        verbose_name_plural = "Рейтинги команд"
        unique_together = ["team", "activity"]
        ordering = ["position"]


# Сигнал для отправки email при выдаче ачивки
@receiver(post_save, sender=AchievementAward)
def send_achievement_notification(sender, instance, created, **kwargs):
    """
    Автоматически отправляет email при создании новой выдачи ачивки
    """
    if created:  # Только при создании (не при обновлении)
        try:
            from cherry.utils import send_achievement_email

            send_achievement_email(instance)
        except Exception as e:
            print(f"Ошибка при отправке уведомления: {e}")
