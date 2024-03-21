from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import UserAccount


@register(UserAccount)
class UserAccountAdmin(UserAdmin):
    """
    Custom admin interface for managing UserAccount instances.
    Inherits from django's UserAdmin.
    """
    list_display = [
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
    ]  # Specifies the fields to display in the admin list view

    search_fields = ['email', 'first_name', 'last_name']  # Adds search functionality for specified fields

    list_filter = [
        'is_staff',
        'is_superuser',
    ]  # Adds filtering options for specified fields

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {
                'fields': (
                    'first_name',
                    'last_name',
                )
            },
        ),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )  # Defines the layout and organization of fields in the admin detail view

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )  # Defines the layout and organization of fields in the admin add view

    ordering = ('email',)  # Specifies the default ordering for instances in the admin interface
