from django.shortcuts import render
from sigma.models import Team, Employee
from boost.models import AchievementAward


def index(request):
    """Главная страница с общей статистикой"""
    context = {
        "teams_count": Team.objects.count(),
        "employees_count": Employee.objects.count(),
        "achievements_count": AchievementAward.objects.count(),
    }
    return render(request, "index.html", context)
