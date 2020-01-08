from rest_framework import viewsets, permissions, views, status

from . import serializers
from . import models


class AddToBasket(views.APIView):
    """
    This view add to basket the instance of product.
    If basket is not exist create new basket in sessions.
    If product added return status HTTP_201_CREATED
    If inbound parameters is wrong return status HTTP_400_BAD_REQUEST
    If product out of stock return status HTTP_409_CONFLICT
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, row, column):
        # message = "Mobile number must contain 10 digits"
        # if not re.match(r'^\d{10}$', mobile_number):
        #     return Response(message, status=status.HTTP_404_NOT_FOUND)
        # user, created = User.objects.get_or_create(mobile_number=mobile_number, defaults={'is_staff': False})
        # serializer = UserSerializer(user)
        # if created:
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
