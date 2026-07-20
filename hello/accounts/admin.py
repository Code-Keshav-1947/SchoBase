
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# restering custom user
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role Information", {
            "fields": ("role",),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": ("role",),
        }),
    )