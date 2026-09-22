import pytest
from .models import PointsTransaction, TeamPointsBalance
from sigma.models import Team


@pytest.mark.django_db
class TestPointsTransaction:
    """Тесты для модели PointsTransaction"""

    def test_transaction_creation(self, team):
        """Тест создания операции"""
        transaction = PointsTransaction.objects.create(
            team=team,
            transaction_type="earn",
            points=100,
            description="Test transaction",
        )
        assert transaction.transaction_type == "earn"
        assert transaction.points == 100

    def test_transaction_str(self, team):
        """Тест строкового представления"""
        transaction = PointsTransaction.objects.create(
            team=team, transaction_type="earn", points=100
        )
        # Используем имя из фикстуры (русское)
        assert "Тестовая команда" in str(transaction)  # ← исправлено
        assert "100" in str(transaction)


@pytest.mark.django_db
class TestTeamPointsBalance:
    """Тесты для модели TeamPointsBalance"""

    def test_balance_creation(self, team):
        """Тест создания баланса"""
        balance = TeamPointsBalance.objects.create(
            team=team, total_earned=1000, total_spent=200, current_balance=800
        )
        assert balance.current_balance == 800

    def test_balance_str(self, team):
        """Тест строкового представления"""
        balance = TeamPointsBalance.objects.create(team=team, current_balance=500)
        assert "500" in str(balance)

    def test_one_to_one_with_team(self, team):
        """Тест связи один-к-одному с Team"""
        TeamPointsBalance.objects.create(team=team)
        with pytest.raises(Exception):
            TeamPointsBalance.objects.create(team=team)
