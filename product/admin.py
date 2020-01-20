""" Admin configuration for Product app """

from django.contrib import admin

from . import models

class ProductAdmin(admin.ModelAdmin):
    """ Admin settings for Product table """
    list_display = [
        "title",
        "brand_name",
    ]
    def has_add_permission(self, request, obj=None):
        return False


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



admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductInstance, ProductInstanceAdmin)
