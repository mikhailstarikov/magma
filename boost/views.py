from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import AchievementAward, TeamRating
from sigma.models import Employee


@login_required
def employee_profile(request):
    """Профиль сотрудника с блоком достижений"""
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        employee = None

    awards = AchievementAward.objects.filter(employee=employee).select_related(
        "achievement"
    )

    context = {
        "employee": employee,
        "awards": awards,
    }
    return render(request, "boost/profile.html", context)


@login_required
def achievement_detail(request, award_id):
    """Детальная страница конкретной ачивки"""
    award = get_object_or_404(
        AchievementAward.objects.select_related("achievement", "employee__user"),
        id=award_id,
        employee__user=request.user,
    )

    context = {
        "award": award,
    }
    return render(request, "boost/achievement_detail.html", context)


@login_required
def team_rating(request):
    """Страница командного рейтинга"""
    # Получаем все рейтинги, отсортированные по позиции (от 1 места)
    ratings = TeamRating.objects.select_related("team", "activity").order_by("position")

    # Пытаемся найти команду текущего пользователя, чтобы подсветить её
    user_team = None
    try:
        user_team = request.user.employee.team
    except (Employee.DoesNotExist, AttributeError):
        pass

    context = {
        "ratings": ratings,
        "user_team": user_team,
    }
    return render(request, "boost/team_rating.html", context)
