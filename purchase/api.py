from rest_framework import viewsets, permissions

from . import serializers
from . import models


class PurchaseInvoiceLineViewSet(viewsets.ModelViewSet):
    """ViewSet for the PurchaseInvoiceLine class"""

    queryset = models.PurchaseInvoiceLine.objects.all()
    serializer_class = serializers.PurchaseInvoiceLineSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderInvoiceLineViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderInvoiceLine class"""

    queryset = models.OrderInvoiceLine.objects.all()
    serializer_class = serializers.OrderInvoiceLineSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for the Order class"""

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseViewSet(viewsets.ModelViewSet):
    """ViewSet for the Purchase class"""

    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]
