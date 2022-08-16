from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    readonly_fields = ['created_at', 'updated_at']
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_active')
    list_filter = ('is_superuser', 'is_active')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2'),
        }),
    )
    search_fields = ('first_name', 'last_name')
    filter_horizontal = ()
    ordering = ('email',)


admin.site.register(get_user_model(), UserAdmin)
# admin.site.register(User)
admin.site.unregister(Group)
