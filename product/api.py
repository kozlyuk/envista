from rest_framework import viewsets, permissions

from . import serializers
from . import models


class ProductInstanceViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProductInstance class"""

    queryset = models.ProductInstance.objects.all()
    serializer_class = serializers.ProductInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]


class StockViewSet(viewsets.ModelViewSet):
    """ViewSet for the Stock class"""

    queryset = models.Stock.objects.all()
    serializer_class = serializers.StockSerializer
    permission_classes = [permissions.IsAuthenticated]


class CylinderViewSet(viewsets.ModelViewSet):
    """ViewSet for the Cylinder class"""

    queryset = models.Cylinder.objects.all()
    serializer_class = serializers.CylinderSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for the Product class"""

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class DiopterPowerViewSet(viewsets.ModelViewSet):
    """ViewSet for the DiopterPower class"""

    queryset = models.DiopterPower.objects.all()
    serializer_class = serializers.DiopterPowerSerializer
    permission_classes = [permissions.IsAuthenticated]
