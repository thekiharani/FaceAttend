from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    list_display = ('email', 'is_instructor', 'is_active')
    list_filter = ('is_superuser', 'is_staff', 'is_instructor', 'is_active')
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_instructor', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'email', 'password1', 'password2', 'is_instructor', 'is_active')}
        ),
    )
    search_fields = ('email', 'name')
    ordering = ('email', 'name')


admin.site.register(get_user_model(), CustomUserAdmin)
