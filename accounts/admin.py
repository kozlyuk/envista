""" Admin configuration for Accounts app """

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.conf import settings

from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """ Admin settings for CustomUser table """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'mobile_number', 'is_active', 'custom_group')
    list_filter = ('groups__name', 'is_active')
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'mobile_number', 'is_staff', 'is_active',
                           'email_confirmed', 'address', 'comment', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'mobile_number',)
    ordering = ('is_staff', '-is_active', 'last_name',)

    def custom_group(self, obj):
        """
        get group, separate by comma, and display empty string if user has no group
        """
        return ','.join([g.name for g in obj.groups.all()]) if obj.groups.count() else ''

    def save_model(self, request, obj, form, change):
        """ Automatic add user to group """
        if obj.pk:
            obj.groups.clear()
            if obj.is_staff:
                group = Group.objects.get(name='Менеджери')
            elif obj.is_active:
                group = Group.objects.get(name='Клієнти')
            obj.groups.add(group)
        super().save_model(request, obj, form, change)



admin.site.site_url = settings.SITE_URL
admin.AdminSite.site_header = settings.SITE_HEADER
admin.AdminSite.site_title = settings.SITE_TITLE
admin.AdminSite.index_title = settings.INDEX_TITLE
admin.site.disable_action('delete_selected')
