from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response

from purchase import serializers
from purchase import models
from product.models import ProductInstance, Cylinder, DiopterPower
from purchase.models import Order, OrderLine


class GetStocks(views.APIView):
    """
    Send JSON-coded list of stocks for product instances
    Create new user cart or clear existing
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # Creating user cart or clear existing on loading.
        order, created = Order.objects.get_or_create(customer=self.request.user,
                                                     status=Order.InCart,
                                                     defaults={'invoice_number': 'InCart'})
        if not created:
            order.products.clear()

        # Sending JSON list of stocks for product instances.
        json_data = []
        json_data.append({"columns": Cylinder.objects.values_list('value', flat=True)})
        json_data.append({"rows": []})
        for row in DiopterPower.objects.values_list('value', flat=True):
            quantity_list = ProductInstance.objects.filter(diopter__value=row).values_list('quantity_in_hand', flat=True)
            json_data[1]["rows"].append({"row": row, "quantities": quantity_list})
        return Response(json_data, status=status.HTTP_200_OK)


class GetCart(views.APIView):
    """
    Send JSON-coded list of orderlines in customer cart
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # get the existing customer cart
        try:
            order = Order.objects.get(customer=self.request.user, status=Order.InCart)
        except Order.DoesNotExist:
            return Response(_('Cart does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Order.MultipleObjectsReturned:
            return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

        # send JSON-coded list of orderlines in customer cart
        json_data = []
        json_data.append({"lines": []})
        index = 0
        for line in order.orderline_set.all():
            index += 1
            order_line = [index, line.product.__str__(), line.quantity, line.unit_price]
            json_data[0]["lines"].append({"line": order_line})
        json_data.append({"value_total": order.value_total()})
        return Response(json_data, status=status.HTTP_200_OK)


class AddToCart(views.APIView):
    """
    This view add to cart the instance of product
    If product added return status HTTP_201_CREATED
    If product not found in ProductInstance's return HTTP_404_NOT_FOUND
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    If product out of stock return status HTTP_409_CONFLICT
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, row: int, column: int):
        # get the existing object of ProductInstance
        try:
            product = ProductInstance.objects.get(diopter=row, cylinder=column)
        except ProductInstance.DoesNotExist:
            return Response(_('Product does not exist'), status=status.HTTP_404_NOT_FOUND)

        # get the existing customer cart
        try:
            order = Order.objects.get(customer=self.request.user, status=Order.InCart)
        except Order.DoesNotExist:
            return Response(_('Cart does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Order.MultipleObjectsReturned:
            return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

        # get the existing OrderLine or create new one
        if product.quantity_in_hand > 0:
            order_line, created = OrderLine.objects.get_or_create(product=product,
                                                                  order=order,
                                                                  defaults={'unit_price': product.price})
            if order_line.quantity + 1 <= product.quantity_in_hand:
                order_line.quantity += 1
                order_line.save()
                return Response(_('Product added to the cart'), status=status.HTTP_201_CREATED)
        return Response(_('Product is out of stock'), status=status.HTTP_409_CONFLICT)


class DelFromCart(views.APIView):
    """
    This view delete the product from cart
    If product deleted return status HTTP_200_OK
    If product not found in ProductInstance's return HTTP_404_NOT_FOUND
    If product not found in cart return status HTTP_404_NOT_FOUND
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, row: int, column: int):
        # get the existing object of ProductInstance
        try:
            product = ProductInstance.objects.get(diopter=row, cylinder=column)
        except ProductInstance.DoesNotExist:
            return Response(_('Product does not exist'), status=status.HTTP_404_NOT_FOUND)

        # get the existing customer cart
        try:
            order = Order.objects.get(customer=self.request.user, status=Order.InCart)
        except Order.DoesNotExist:
            return Response(_('Cart does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Order.MultipleObjectsReturned:
            return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

        # remove the existing OrderLine or returm exception if it is not exists
        try:
            OrderLine.objects.get(product=product, order=order).delete()
            return Response(_('Product deleted'), status=status.HTTP_200_OK)
        except OrderLine.DoesNotExist:
            return Response(_('Product not in cart'), status=status.HTTP_404_NOT_FOUND)


class UpdateQuantity(views.APIView):
    """
    This view update the product in cart
    If product updated return status HTTP_200_OK
    If product not found in ProductInstance's return HTTP_404_NOT_FOUND
    If product not found in cart return status HTTP_404_NOT_FOUND
    If product out of stock return status HTTP_409_CONFLICT
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, row: int, column: int, quantity: int):
        # get the existing object of ProductInstance
        try:
            product = ProductInstance.objects.get(diopter=row, cylinder=column)
        except ProductInstance.DoesNotExist:
            return Response(_('Product does not exist'), status=status.HTTP_400_BAD_REQUEST)

        # get the existing customer cart
        try:
            order = Order.objects.get(customer=self.request.user, status=Order.InCart)
        except Order.DoesNotExist:
            return Response(_('Cart does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Order.MultipleObjectsReturned:
            return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

        # update the existing OrderLine or returm exception if it is not exists
        try:
            order_line = OrderLine.objects.get(product=product, order=order)
            if quantity <= product.quantity_in_hand:
                order_line.quantity = quantity
                order_line.save()
                return Response(_('Product updated'), status=status.HTTP_200_OK)
            else:
                return Response(_('Product is not enough in stock'), status=status.HTTP_409_CONFLICT)
        except OrderLine.DoesNotExist:
            return Response(_('Product not in cart'), status=status.HTTP_404_NOT_FOUND)


class ConfirmOrder(views.APIView):
    """
    Change order status from InCart to NewOrder and assign invoice number
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        # get the existing customer cart
        try:
            order = Order.objects.get(customer=self.request.user, status=Order.InCart)
        except Order.DoesNotExist:
            return Response(_('Cart does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Order.MultipleObjectsReturned:
            return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

        # change order status to NewOrder and assign invoice number
        order.status = Order.NewOrder
        order.invoice_number = order.invoice_number_generate()
        order.value = order.value_total()
        order.created_by = self.request.user
        order.save()

        # reduce stocks
        for order_line in order.orderline_set.all():
            order_line.product.quantity_in_hand -= order_line.quantity
            order_line.product.save()

        return Response(_('Order created'), status=status.HTTP_201_CREATED)


class PurchaseLineViewSet(viewsets.ModelViewSet):
    """ViewSet for the PurchaseLine class"""

    queryset = models.PurchaseLine.objects.all()
    serializer_class = serializers.PurchaseLineSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderLineViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderLine class"""

    queryset = models.OrderLine.objects.all()
    serializer_class = serializers.OrderLineSerializer
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
