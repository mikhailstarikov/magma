from django.urls import path
from . import views

app_name = "boost"

urlpatterns = [
    # Профиль сотрудника с достижениями
    path("profile/", views.employee_profile, name="employee_profile"),
    # Детальная страница ачивки
    path(
        "achievement/<int:award_id>/",
        views.achievement_detail,
        name="achievement_detail",
    ),
    # Командный рейтинг
    path("rating/", views.team_rating, name="team_rating"),
]
