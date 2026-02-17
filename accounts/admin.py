from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# -------------------------------
# User Admin
# -------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("full_name", "phone_number", "email", "is_active", "is_staff", "is_owner")
    search_fields = ("first_name", "last_name", "phone_number", "email", "telegram_id")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "phone_number", "email", "telegram_id", "password", "image", "bio")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_owner", "groups", "user_permissions")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("first_name", "last_name", "phone_number", "email", "telegram_id", "password1", "password2", "is_active", "is_staff"),
        }),
    )

