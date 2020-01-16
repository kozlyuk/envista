from django.contrib import admin
from django import forms

from . import models


class PurchaseLineAdminForm(forms.ModelForm):

    class Meta:
        model = models.PurchaseLine
        fields = "__all__"


class PurchaseLineAdmin(admin.ModelAdmin):
    form = PurchaseLineAdminForm
    list_display = [
        "quantity",
        "unit_price",
    ]
    readonly_fields = [
        "quantity",
        "unit_price",
    ]


class OrderLineAdminForm(forms.ModelForm):

    class Meta:
        model = models.OrderLine
        fields = "__all__"


class OrderLineAdmin(admin.ModelAdmin):
    form = OrderLineAdminForm
    list_display = [
        "unit_price",
        "quantity",
    ]
    readonly_fields = [
        "unit_price",
        "quantity",
    ]


class OrderAdminForm(forms.ModelForm):

    class Meta:
        model = models.Order
        fields = "__all__"


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = [
        "invoice_date",
        "date_created",
        "date_updated",
        "invoice_file",
        "comment",
        "value",
        "invoice_number",
        "status",
    ]
    readonly_fields = [
        "invoice_date",
        "date_created",
        "date_updated",
        "invoice_file",
        "comment",
        "value",
        "invoice_number",
        "status",
    ]


class PurchaseAdminForm(forms.ModelForm):

    class Meta:
        model = models.Purchase
        fields = "__all__"


class PurchaseAdmin(admin.ModelAdmin):
    form = PurchaseAdminForm
    list_display = [
        "comment",
        "invoice_number",
        "invoice_date",
        "date_created",
        "date_updated",
    ]
    readonly_fields = [
        "comment",
        "invoice_number",
        "invoice_date",
        "date_created",
        "date_updated",
    ]


admin.site.register(models.PurchaseLine, PurchaseLineAdmin)
admin.site.register(models.OrderLine, OrderLineAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
