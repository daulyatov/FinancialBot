from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import TelegramUser, TelegramExpense, TelegramIncome, TelegramSupport

admin.site.register(TelegramExpense)
admin.site.register(TelegramIncome)
admin.site.register(TelegramSupport)

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("get_formatted_info", "user_id", "created_at")
    list_filter = ("is_bot", "created_at")
    search_fields = ("user_id", "username", "first_name", "last_name")

    fieldsets = (
        (
            None,
            {
                "fields": ("user_id", "is_bot", "language_code"),
            },
        ),
        (
            "Информация пользователя",
            {
                "fields": ("username", "first_name", "last_name", "balance"),
                "classes": ("collapse",),
            },
        ),
    )

    def get_formatted_info(self, obj):
        info = (
            f"<div style='background-color: #f8f9fa; padding: 10px; border-radius: 5px; "
            f"box-shadow: 0 0 30px rgba(0, 0, 0, 0.1);'>"
        )
        info += f"<strong style='color: #000000;'>Username:</strong> {obj.username}<br>"
        info += (
            f"<strong style='color: #000000;'>First Name:</strong> {obj.first_name}<br>"
        )
        info += (
            f"<strong style='color: #000000;'>Last Name:</strong> {obj.last_name}<br>"
        )
        info += f"<strong style='color: #000000;'>Is Bot:</strong> {obj.is_bot}<br>"
        info += f"<strong style='color: #000000;'>Language Code:</strong> {obj.language_code}<br>"
        info += "</div>"
        return mark_safe(info)

    get_formatted_info.short_description = "Информация пользователя"
