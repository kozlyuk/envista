""" Admin configuration for Product app """

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from product.models import Product, ProductInstance, Cylinder, DiopterPower

@admin.register(Product)
class ProductAdmin(SummernoteModelAdmin):
    """ Admin settings for Product table """
    list_display = [
        "title",
        "brand_name",
    ]
    summernote_fields = '__all__'


@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    """ Admin settings for ProductInstance table """
    list_display = [
        "product",
        "cylinder",
        "diopter",
        "price",
        "quantity_in_hand",
    ]
    fieldsets = [
        (None, {'fields': ['product',
                           'cylinder',
                           'diopter',
                           'price',
                           'quantity_in_hand',
                           ]})
    ]
    readonly_fields = [
        "product",
        "cylinder",
        "diopter",
        "quantity_in_hand",
    ]
    list_filter = ('cylinder', 'diopter',)
    ordering = ('pk',)


@admin.register(Cylinder)
class CylinderAdmin(admin.ModelAdmin):
    search_fields = ['value']


@admin.register(DiopterPower)
class DiopterPowerAdmin(admin.ModelAdmin):
    search_fields = ['value']
