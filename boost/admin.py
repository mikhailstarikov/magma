from django.contrib import admin
from .models import Achievement, AchievementAward, TeamRating


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name", "description")


@admin.register(AchievementAward)
class AchievementAwardAdmin(admin.ModelAdmin):
    list_display = ("achievement", "employee", "awarded_by", "awarded_at")
    list_filter = ("achievement", "awarded_at")
    search_fields = ("employee__user__username", "achievement__name")
    readonly_fields = ("awarded_at",)


@admin.register(TeamRating)
class TeamRatingAdmin(admin.ModelAdmin):
    list_display = ("team", "activity", "points", "position")
    list_filter = ("activity",)
    search_fields = ("team__name", "activity__name")
