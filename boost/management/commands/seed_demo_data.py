from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sigma.models import Team, Activity, Employee
from boost.models import Achievement, AchievementAward, TeamRating
from loyalty_program.models import PointsTransaction, TeamPointsBalance


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми данными для демо"

    def handle(self, *args, **options):
        self.stdout.write("Начинаем заполнение базы данных...")

        # Создаём команды
        team1, _ = Team.objects.get_or_create(name="Команда Альфа")
        team2, _ = Team.objects.get_or_create(name="Команда Бета")
        team3, _ = Team.objects.get_or_create(name="Команда Гамма")

        # Создаём активности
        activity1, _ = Activity.objects.get_or_create(
            name="Стажировка 2026",
            description="Программа стажировки для новых сотрудников",
        )
        activity2, _ = Activity.objects.get_or_create(
            name="Хакатон Осень-2026",
            description="Внутренний хакатон по разработке инноваций",
        )

        # Создаём пользователей и сотрудников
        users_data = [
            ("ivan.petrov", "Иван", "Петров", team1, activity1),
            ("maria.sidorova", "Мария", "Сидорова", team1, activity1),
            ("alex.smith", "Алекс", "Смит", team2, activity1),
            ("elena.jones", "Елена", "Джонс", team2, activity2),
            ("dmitry.lee", "Дмитрий", "Ли", team3, activity2),
        ]

        employees = []
        for username, first_name, last_name, team, activity in users_data:
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": f"{username}@sigma.com",
                },
            )
            employee, _ = Employee.objects.get_or_create(
                user=user, defaults={"team": team, "activity": activity}
            )
            employees.append(employee)

        # Создаём ачивки
        achievement1, _ = Achievement.objects.get_or_create(
            name="Первые шаги",
            description="За успешное завершение первого месяца стажировки",
        )
        achievement2, _ = Achievement.objects.get_or_create(
            name="Мастер кода", description="За написание 1000 строк качественного кода"
        )
        achievement3, _ = Achievement.objects.get_or_create(
            name="Командный игрок", description="За отличный вклад в командную работу"
        )
        achievement4, _ = Achievement.objects.get_or_create(
            name="Инноватор",
            description="За предложение и реализацию инновационной идеи",
        )

        # Выдаём ачивки сотрудникам
        admin_user = User.objects.get(username="admin")

        AchievementAward.objects.get_or_create(
            achievement=achievement1,
            employee=employees[0],
            defaults={
                "awarded_by": admin_user,
                "reason": "Успешное завершение испытательного срока",
            },
        )
        AchievementAward.objects.get_or_create(
            achievement=achievement2,
            employee=employees[0],
            defaults={"awarded_by": admin_user, "reason": "Превышение плана по коду"},
        )
        AchievementAward.objects.get_or_create(
            achievement=achievement3,
            employee=employees[1],
            defaults={
                "awarded_by": admin_user,
                "reason": "Помощь коллегам и менторство",
            },
        )
        AchievementAward.objects.get_or_create(
            achievement=achievement4,
            employee=employees[2],
            defaults={
                "awarded_by": admin_user,
                "reason": "Предложение новой архитектуры",
            },
        )

        # Создаём рейтинги команд
        TeamRating.objects.get_or_create(
            team=team1, activity=activity1, defaults={"points": 1500, "position": 1}
        )
        TeamRating.objects.get_or_create(
            team=team2, activity=activity1, defaults={"points": 1200, "position": 2}
        )
        TeamRating.objects.get_or_create(
            team=team3, activity=activity2, defaults={"points": 900, "position": 1}
        )

        # Создаём операции с баллами и балансы
        for team in [team1, team2, team3]:
            PointsTransaction.objects.get_or_create(
                team=team,
                transaction_type="earn",
                points=1000,
                description="Начальные баллы за участие",
            )
            TeamPointsBalance.objects.get_or_create(
                team=team,
                defaults={
                    "total_earned": 1000,
                    "total_spent": 0,
                    "current_balance": 1000,
                },
            )

        self.stdout.write(
            self.style.SUCCESS("База данных успешно заполнена тестовыми данными!")
        )
