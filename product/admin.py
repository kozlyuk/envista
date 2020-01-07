from django.contrib import admin
from django import forms

from . import models


class ProductInstanceAdminForm(forms.ModelForm):

    class Meta:
        model = models.ProductInstance
        fields = "__all__"


class ProductInstanceAdmin(admin.ModelAdmin):
    form = ProductInstanceAdminForm
    list_display = [
        "date_updated",
        "date_created",
        "price",
    ]
    readonly_fields = [
        "date_updated",
        "date_created",
        "price",
    ]


class StockAdminForm(forms.ModelForm):

    class Meta:
        model = models.Stock
        fields = "__all__"


class StockAdmin(admin.ModelAdmin):
    form = StockAdminForm
    list_display = [
        "quantity_in_hand",
    ]
    readonly_fields = [
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
    readonly_fields = [
        "value",
    ]


class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = models.Product
        fields = "__all__"


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = [
        "date_created",
        "date_updated",
        "brand_name",
        "brand_image",
        "short_description",
        "long_description",
        "product_image",
        "title",
    ]
    readonly_fields = [
        "date_created",
        "date_updated",
        "brand_name",
        "brand_image",
        "short_description",
        "long_description",
        "product_image",
        "title",
    ]


class DiopterPowerAdminForm(forms.ModelForm):

    class Meta:
        model = models.DiopterPower
        fields = "__all__"


class DiopterPowerAdmin(admin.ModelAdmin):
    form = DiopterPowerAdminForm
    list_display = [
        "value",
    ]
    readonly_fields = [
        "value",
    ]


admin.site.register(models.ProductInstance, ProductInstanceAdmin)
admin.site.register(models.Stock, StockAdmin)
admin.site.register(models.Cylinder, CylinderAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.DiopterPower, DiopterPowerAdmin)
