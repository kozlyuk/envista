from rest_framework import serializers

from purchase.models import Order, OrderLine


class OrderLineSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderLine
        fields = [
            "product",
            "quantity",
            "unit_price",
        ]

    def get_product(self, obj):
        return f"ENVISTA® TORIC {obj.diopter}-{obj.cylinder}"


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

    @staticmethod
    def setup_eager_loading(queryset):
        """ optimizing "to-many" relationships with prefetch_related """
        queryset = queryset.prefetch_related(
            'orderline_set__diopter',
            'orderline_set__cylinder')
        return queryset
