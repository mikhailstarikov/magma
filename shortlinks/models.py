from django.db import models
from django.contrib.auth.models import User
import string
import random


def generate_short_code(length=6):
    """Генерирует случайный короткий код"""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


class ShortLink(models.Model):
    """Модель короткой ссылки"""

    original_url = models.URLField(max_length=2048, verbose_name="Исходный URL")
    short_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Короткий код",
        default=generate_short_code,
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Создал"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    clicks = models.IntegerField(default=0, verbose_name="Количество переходов")
    is_active = models.BooleanField(default=True, verbose_name="Активна")

    class Meta:
        verbose_name = "Короткая ссылка"
        verbose_name_plural = "Короткие ссылки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_code} → {self.original_url[:50]}"

    def get_short_url(self):
        """Возвращает полный короткий URL"""
        from django.conf import settings

        return f"{settings.SITE_URL}/s/{self.short_code}"

    def increment_clicks(self):
        """Увеличивает счётчик переходов"""
        self.clicks += 1
        self.save(update_fields=["clicks"])
