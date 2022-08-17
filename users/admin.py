from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Soft Deletion', {'fields': ('deleted_at', 'is_deleted',)}),
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

    def get_queryset(self, request):
        qs = self.model.all_objects
        # The below is copied from the base implementation in BaseModelAdmin to prevent other changes in behavior
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.hard_delete()


admin.site.register(get_user_model(), UserAdmin)
# admin.site.register(User)
admin.site.unregister(Group)
