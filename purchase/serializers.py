from rest_framework import serializers

from . import models


class PurchaseInvoiceLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PurchaseInvoiceLine
        fields = [
            "quantity",
            "unit_price",
        ]

class OrderInvoiceLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderInvoiceLine
        fields = [
            "unit_price",
            "quantity",
        ]

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = [
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

class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Purchase
        fields = [
            "comment",
            "invoice_number",
            "invoice_date",
            "date_created",
            "date_updated",
        ]
