from django.contrib import admin
from django import forms

from . import models


class PurchaseInvoiceLineAdminForm(forms.ModelForm):

    class Meta:
        model = models.PurchaseInvoiceLine
        fields = "__all__"


class PurchaseInvoiceLineAdmin(admin.ModelAdmin):
    form = PurchaseInvoiceLineAdminForm
    list_display = [
        "quantity",
        "unit_price",
    ]
    readonly_fields = [
        "quantity",
        "unit_price",
    ]


class OrderInvoiceLineAdminForm(forms.ModelForm):

    class Meta:
        model = models.OrderInvoiceLine
        fields = "__all__"


class OrderInvoiceLineAdmin(admin.ModelAdmin):
    form = OrderInvoiceLineAdminForm
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
        "pay_status",
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
        "pay_status",
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


admin.site.register(models.PurchaseInvoiceLine, PurchaseInvoiceLineAdmin)
admin.site.register(models.OrderInvoiceLine, OrderInvoiceLineAdmin)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Purchase, PurchaseAdmin)
