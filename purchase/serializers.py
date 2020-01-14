from rest_framework import serializers

from . import models


class PurchaseLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PurchaseLine
        fields = [
            "quantity",
            "unit_price",
        ]

class OrderLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OrderLine
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
