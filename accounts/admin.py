from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'mobile_number', 'is_staff', 'is_active',)
    list_filter = ('email', 'mobile_number', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'mobile_number', 'email')}),
        ('Permissions', {'fields': ('user_permissions', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active',
                       'mobile_number')
        }),
    )
    search_fields = ('email', 'mobile_number',)
    ordering = ('-date_joined',)


admin.site.register(User, CustomUserAdmin)
