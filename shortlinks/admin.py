from django.contrib import admin
from .models import ShortLink


@admin.action(description="Удалить выбранные ссылки")
def delete_selected_links(modeladmin, request, queryset):
    """Массовое удаление ссылок"""
    count = queryset.count()
    queryset.delete()
    modeladmin.message_user(request, f"Удалено ссылок: {count}")


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = (
        "short_code",
        "original_url",
        "clicks",
        "is_active",
        "created_at",
        "created_by",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("short_code", "original_url")
    actions = [delete_selected_links]
