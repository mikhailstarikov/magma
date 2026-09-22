import pytest
from django.urls import reverse
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestViews:
    """Тесты для views (страниц)"""

    def test_home_page(self, client):
        """Тест главной страницы"""
        response = client.get(reverse("home"))
        assert response.status_code == 200
        assert b"Magma" in response.content

    def test_profile_page_requires_login(self, client):
        """Тест что профиль требует авторизации"""
        response = client.get(reverse("boost:employee_profile"))
        assert response.status_code == 302  # Редирект на login

    def test_profile_page_authenticated(self, client, user):
        """Тест профиля для авторизованного пользователя"""
        client.force_login(user)
        response = client.get(reverse("boost:employee_profile"))
        assert response.status_code == 200

    def test_team_rating_page(self, client, user):
        """Тест страницы рейтинга"""
        client.force_login(user)
        response = client.get(reverse("boost:team_rating"))
        assert response.status_code == 200

    def test_balance_page(self, client, user):
        """Тест страницы балансов"""
        client.force_login(user)
        response = client.get(reverse("loyalty:team_balance"))
        assert response.status_code == 200

    def test_transactions_page(self, client, user):
        """Тест страницы операций"""
        client.force_login(user)
        response = client.get(reverse("loyalty:transactions"))
        assert response.status_code == 200

    def test_shortlinks_create_page(self, client, user):
        """Тест страницы создания ссылки"""
        client.force_login(user)
        response = client.get(reverse("shortlinks:create"))
        assert response.status_code == 200

    def test_shortlinks_my_links_page(self, client, user):
        """Тест страницы моих ссылок"""
        client.force_login(user)
        response = client.get(reverse("shortlinks:my_links"))
        assert response.status_code == 200

    def test_shortlink_redirect(self, client, short_link):
        """Тест редиректа короткой ссылки"""
        response = client.get(
            reverse("redirect", kwargs={"short_code": short_link.short_code})
        )
        assert response.status_code == 302
        assert response.url == short_link.original_url

    def test_shortlink_redirect_increments_clicks(self, client, short_link):
        """Тест что редирект увеличивает счётчик"""
        initial_clicks = short_link.clicks
        client.get(reverse("redirect", kwargs={"short_code": short_link.short_code}))
        short_link.refresh_from_db()
        assert short_link.clicks == initial_clicks + 1

    def test_achievement_detail_page(self, client, user, achievement_award):
        """Тест детальной страницы ачивки"""
        # Привяжем ачивку к пользователю
        achievement_award.employee.user = user
        achievement_award.employee.save()

        client.force_login(user)
        response = client.get(
            reverse(
                "boost:achievement_detail", kwargs={"award_id": achievement_award.id}
            )
        )
        assert response.status_code == 200

    def test_admin_page_requires_login(self, client, user):
        """Тест что админка требует авторизации"""
        client.force_login(user)  # Обычный пользователь (не staff)
        response = client.get("/admin/")
        # Django перенаправляет на страницу логина, а не возвращает 403
        assert response.status_code == 302
        assert "/admin/login/" in response.url

    def test_admin_page_for_admin(self, client, admin_user):
        """Тест админки для администратора"""
        client.force_login(admin_user)
        response = client.get("/admin/")
        assert response.status_code == 200
