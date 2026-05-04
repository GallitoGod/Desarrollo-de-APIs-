from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'documento_identidad',
        'domicilio',
        'is_active',
        'is_staff',
        'date_joined',
    )

    search_fields = (
        'username',
        'email',
        'documento_identidad',
        'domicilio',
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'documento_identidad',
                'domicilio',
                'password1',
                'password2',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
    )

