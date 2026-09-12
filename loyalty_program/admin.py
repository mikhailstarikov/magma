from django.contrib import admin
from .models import PointsTransaction, TeamPointsBalance


@admin.register(PointsTransaction)
class PointsTransactionAdmin(admin.ModelAdmin):
    list_display = ("team", "transaction_type", "points", "created_at")
    list_filter = ("transaction_type", "created_at")
    search_fields = ("team__name", "description")


@admin.register(TeamPointsBalance)
class TeamPointsBalanceAdmin(admin.ModelAdmin):
    list_display = ("team", "total_earned", "total_spent", "current_balance")
    search_fields = ("team__name",)
