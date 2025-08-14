from django.contrib import admin
from .models import UserRole

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'is_active_status')
    list_filter = ('role',)

    def is_active_status(self, obj):
        return obj.user.is_active

    is_active_status.boolean = True
    is_active_status.short_description = 'ثبت نام شده؟'