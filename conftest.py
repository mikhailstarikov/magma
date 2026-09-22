import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from sigma.models import Team, Activity, Employee
from boost.models import Achievement, AchievementAward
from loyalty_program.models import TeamPointsBalance, PointsTransaction
from shortlinks.models import ShortLink


@pytest.fixture
def db_setup(db):
    """Базовая настройка БД для тестов"""
    pass


@pytest.fixture
def user(db):
    """Создание тестового пользователя"""
    return User.objects.create_user(
        username="testuser",
        password="testpass123",
        email="test@example.com",
        first_name="Test",
        last_name="User",
    )


@pytest.fixture
def admin_user(db):
    """Создание администратора"""
    return User.objects.create_superuser(
        username="testadmin", password="adminpass123", email="admin@example.com"
    )


@pytest.fixture
def team(db):
    """Создание тестовой команды"""
    return Team.objects.create(name="Тестовая команда")


@pytest.fixture
def activity(db):
    """Создание тестовой активности"""
    return Activity.objects.create(
        name="Тестовая активность", description="Описание для теста"
    )


@pytest.fixture
def employee(db, user, team, activity):
    """Создание тестового сотрудника"""
    return Employee.objects.create(user=user, team=team, activity=activity)


@pytest.fixture
def achievement(db):
    """Создание тестовой ачивки"""
    return Achievement.objects.create(
        name="Тестовая ачивка", description="Описание тестовой ачивки"
    )


@pytest.fixture
def achievement_award(db, employee, achievement, admin_user):
    """Создание выдачи ачивки"""
    return AchievementAward.objects.create(
        employee=employee,
        achievement=achievement,
        awarded_by=admin_user,
        reason="Тестовая причина",
    )


@pytest.fixture
def short_link(db, user):
    """Создание тестовой короткой ссылки"""
    return ShortLink.objects.create(
        original_url="https://www.example.com/very/long/url", created_by=user
    )
