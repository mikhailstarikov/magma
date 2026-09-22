import pytest
from django.contrib.auth.models import User
from .models import EmailNotification


@pytest.mark.django_db
class TestEmailNotification:
    """Тесты для модели EmailNotification"""

    def test_notification_creation(self):
        """Тест создания уведомления"""
        user = User.objects.create_user(username="testuser", email="test@example.com")
        notification = EmailNotification.objects.create(
            recipient=user, subject="Test Subject", body="Test body", is_sent=True
        )
        assert notification.recipient == user
        assert notification.subject == "Test Subject"
        assert notification.is_sent is True

    def test_notification_str(self):
        """Тест строкового представления"""
        user = User.objects.create_user(username="testuser", email="test@example.com")
        notification = EmailNotification.objects.create(
            recipient=user, subject="Test Subject", body="Test body"
        )
        assert "test@example.com" in str(notification)
        assert "Test Subject" in str(notification)
