from django.db import models
from django.contrib.auth.models import User


class EmailNotification(models.Model):
    """История отправленных email-уведомлений"""

    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Получатель"
    )
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Текст письма")
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")
    is_sent = models.BooleanField(default=False, verbose_name="Отправлено")

    class Meta:
        verbose_name = "Email уведомление"
        verbose_name_plural = "Email уведомления"
        ordering = ["-sent_at"]

    def __str__(self):
        return f"{self.recipient.email} - {self.subject}"
