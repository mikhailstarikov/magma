import pytest
from .models import ShortLink


@pytest.mark.django_db
class TestShortLinkModel:
    """Тесты для модели ShortLink"""

    def test_short_link_creation(self, user):
        """Тест создания короткой ссылки"""
        link = ShortLink.objects.create(
            original_url="https://example.com/test", created_by=user
        )
        assert link.original_url == "https://example.com/test"
        assert link.short_code is not None
        assert len(link.short_code) > 0

    def test_short_link_unique_code(self, user):
        """Тест уникальности short_code"""
        link1 = ShortLink.objects.create(
            original_url="https://example.com/1", created_by=user, short_code="test123"
        )
        with pytest.raises(Exception):
            ShortLink.objects.create(
                original_url="https://example.com/2",
                created_by=user,
                short_code="test123",
            )

    def test_increment_clicks(self, user):
        """Тест увеличения счётчика переходов"""
        link = ShortLink.objects.create(
            original_url="https://example.com", created_by=user, clicks=0
        )
        link.increment_clicks()
        assert link.clicks == 1
        link.increment_clicks()
        assert link.clicks == 2

    def test_get_short_url(self, user, settings):
        """Тест генерации короткого URL"""
        settings.SITE_URL = "http://testserver"
        link = ShortLink.objects.create(
            original_url="https://example.com", created_by=user, short_code="abc123"
        )
        assert link.get_short_url() == "http://testserver/s/abc123"
