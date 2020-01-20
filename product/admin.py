""" Admin configuration for Product app """

from django.contrib import admin

from product.models import Product, ProductInstance, Cylinder, DiopterPower

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin settings for Product table """
    list_display = [
        "title",
        "brand_name",
    ]
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


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

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Cylinder)
class CylinderAdmin(admin.ModelAdmin):
    search_fields = ['value']

    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(DiopterPower)
class DiopterPowerAdmin(admin.ModelAdmin):
    search_fields = ['value']

    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
