import pytest
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Team, Activity, Employee


@pytest.mark.django_db
class TestTeamModel:
    """Тесты для модели Team"""

    def test_team_creation(self):
        """Тест создания команды"""
        team = Team.objects.create(name="Test Team")
        assert team.name == "Test Team"
        assert str(team) == "Test Team"

    def test_team_max_length_validation(self):
        """Тест валидации максимальной длины названия"""
        long_name = "A" * 101
        team = Team(name=long_name)
        with pytest.raises(ValidationError):
            team.full_clean()  # ← Явный вызов валидации


@pytest.mark.django_db
class TestActivityModel:
    """Тесты для модели Activity"""

    def test_activity_creation(self):
        """Тест создания активности"""
        activity = Activity.objects.create(
            name="Test Activity", description="Test description"
        )
        assert activity.name == "Test Activity"
        assert str(activity) == "Test Activity"

    def test_activity_optional_description(self):
        """Тест что описание необязательно"""
        activity = Activity.objects.create(name="Test Activity")
        assert activity.description == ""


@pytest.mark.django_db
class TestEmployeeModel:
    """Тесты для модели Employee"""

    def test_employee_creation(self, user, team, activity):
        """Тест создания сотрудника"""
        employee = Employee.objects.create(user=user, team=team, activity=activity)
        assert employee.user == user
        assert employee.team == team
        assert employee.activity == activity

    def test_employee_str(self, user, team, activity):
        """Тест строкового представления"""
        employee = Employee.objects.create(user=user, team=team, activity=activity)
        assert str(employee) == "Test User"

    def test_employee_optional_team_activity(self, user):
        """Тест что команда и активность необязательны"""
        employee = Employee.objects.create(user=user)
        assert employee.team is None
        assert employee.activity is None
