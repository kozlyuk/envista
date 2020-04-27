from rest_framework import serializers

from envista.utils import ChoicesField
from purchase.models import Order, OrderLine


class OrderLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderLine
        fields = [
            "diopter",
            "cylinder",
            "quantity",
            "unit_price",
        ]

class OrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(source='orderline_set', many=True)
    status_display = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = [
            "pk",
            "invoice_number",
            "status",
            "status_display",
            "value",
            "lenses_sum",
            "date_created",
            "date_updated",
            "comment",
            "order_lines"
        ]
