from django.contrib import admin
from .models import Team, Activity, Employee


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name", "description")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "activity")
    list_filter = ("team", "activity")
    search_fields = ("user__username", "user__first_name", "user__last_name")
