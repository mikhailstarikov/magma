import pytest
from django.contrib.auth.models import User
from .models import Achievement, AchievementAward, TeamRating
from sigma.models import Team, Activity


@pytest.mark.django_db
class TestAchievementModel:
    """Тесты для модели Achievement"""

    def test_achievement_creation(self):
        """Тест создания ачивки"""
        achievement = Achievement.objects.create(
            name="Test Achievement", description="Test description"
        )
        assert achievement.name == "Test Achievement"
        assert str(achievement) == "Test Achievement"

    def test_achievement_optional_image(self):
        """Тест что изображение необязательно"""
        achievement = Achievement.objects.create(name="Test")
        # ImageField возвращает пустой объект, а не None
        assert not achievement.image  # ← исправлено


@pytest.mark.django_db
class TestAchievementAwardModel:
    """Тесты для модели AchievementAward"""

    def test_award_creation(self, employee, achievement, admin_user):
        """Тест создания выдачи ачивки"""
        award = AchievementAward.objects.create(
            employee=employee,
            achievement=achievement,
            awarded_by=admin_user,
            reason="Test reason",
        )
        assert award.employee == employee
        assert award.achievement == achievement
        assert award.awarded_by == admin_user

    def test_award_str(self, employee, achievement, admin_user):
        """Тест строкового представления"""
        award = AchievementAward.objects.create(
            employee=employee, achievement=achievement, awarded_by=admin_user
        )
        # Используем имя из фикстуры (русское)
        assert "Тестовая ачивка" in str(award)  # ← исправлено
        assert "Test User" in str(award)


@pytest.mark.django_db
class TestTeamRatingModel:
    """Тесты для модели TeamRating"""

    def test_rating_creation(self, team, activity):
        """Тест создания рейтинга"""
        rating = TeamRating.objects.create(
            team=team, activity=activity, points=100, position=1
        )
        assert rating.points == 100
        assert rating.position == 1

    def test_rating_str(self, team, activity):
        """Тест строкового представления"""
        rating = TeamRating.objects.create(
            team=team, activity=activity, points=1500, position=2
        )
        assert "1500" in str(rating)
        assert "2" in str(rating)

    def test_unique_together(self, team, activity):
        """Тест уникальности (team, activity)"""
        TeamRating.objects.create(team=team, activity=activity, points=100)
        with pytest.raises(Exception):
            TeamRating.objects.create(team=team, activity=activity, points=200)
