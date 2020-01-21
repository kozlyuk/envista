""" Admin configuration for Accounts app """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.conf import settings

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """ Admin settings for CustomUser table """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'mobile_number', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'mobile_number', 'email', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'mobile_number',)
    ordering = ('-is_staff', '-is_active', 'last_name',)


admin.site.site_url = settings.SITE_URL
admin.AdminSite.site_header = settings.SITE_HEADER
admin.AdminSite.site_title = settings.SITE_TITLE
admin.AdminSite.index_title = settings.INDEX_TITLE
admin.site.disable_action('delete_selected')
