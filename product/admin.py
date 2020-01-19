from django.contrib import admin
from django import forms
from django.conf import settings

from . import models

admin.site.site_url = settings.SITE_URL
admin.AdminSite.site_header = 'Адміністратор проектів Ітел-Сервіс'
admin.AdminSite.site_title = 'Itel-Service ERP'


class ProductInstanceAdminForm(forms.ModelForm):

    class Meta:
        model = models.ProductInstance
        fields = "__all__"


class ProductInstanceAdmin(admin.ModelAdmin):
    form = ProductInstanceAdminForm
    list_display = [
        "product",
        "cylinder",
        "diopter",
        "price",
        "quantity_in_hand",
    ]


class CylinderAdminForm(forms.ModelForm):

    class Meta:
        model = models.Cylinder
        fields = "__all__"


class CylinderAdmin(admin.ModelAdmin):
    form = CylinderAdminForm
    list_display = [
        "value",
    ]


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = models.Product
        exclude = ['created_by']


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = [
        "date_created",
        "date_updated",
        "brand_name",
        "brand_image",
        "product_image",
        "title",
    ]

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.created_by = request.user
        obj.save()

class DiopterPowerAdminForm(forms.ModelForm):

    class Meta:
        model = models.DiopterPower
        fields = "__all__"


class DiopterPowerAdmin(admin.ModelAdmin):
    form = DiopterPowerAdminForm
    list_display = [
        "value",
    ]


admin.site.register(models.ProductInstance, ProductInstanceAdmin)
admin.site.register(models.Cylinder, CylinderAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.DiopterPower, DiopterPowerAdmin)
