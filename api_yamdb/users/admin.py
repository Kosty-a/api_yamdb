from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


User = get_user_model()


class UserAdmin(BaseUserAdmin):
    model = User

    fieldsets = BaseUserAdmin.fieldsets
    fieldsets[1][1]['fields'] += ('bio', 'role')

    list_display = ('username', 'email', 'is_staff', 'role')
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
