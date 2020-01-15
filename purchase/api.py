from django.utils.translation import gettext_lazy as _
from rest_framework import viewsets, permissions, views, status
from rest_framework.response import Response

from purchase import serializers
from purchase import models
from product.models import ProductInstance, Cylinder, DiopterPower, Stock
from purchase.models import Order, OrderLine


class GetStocks(views.APIView):
    """
    This view sending JSON list of stocks for product instances.
    Creating user cart or clear existing on loading.
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
            quantity_list = Stock.objects.filter(product_instance__diopter__value=row).values_list('quantity_in_hand', flat=True)
            json_data[1]["rows"].append({"row": row, "quantity": quantity_list})

        return Response(json_data, status=status.HTTP_200_OK)


class AddToCart(views.APIView):
    """
    This view add to cart the instance of product.
    If product added return status HTTP_201_CREATED
    If inbound parameters is wrong return status HTTP_404_NOT_FOUND
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
        if product.quantity_in_hand and product.quantity_in_hand > 0:
            invoice_line, created = OrderLine.objects.get_or_create(product=product,
                                                                    order=order,
                                                                    defaults={'unit_price': product.price})
            if invoice_line.quantity + 1 <= product.quantity_in_hand:
                invoice_line.quantity += 1
                return Response(_('Product added to the cart'), status=status.HTTP_201_CREATED)
        return Response(_('Product is out of stock'), status=status.HTTP_409_CONFLICT)


class DelFromCart(views.APIView):
    """
    This view delete the product from cart.
    If product deleted return status HTTP_200_OK
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

        # get the existing OrderLine or returm exception
        try:
            order.products.remove(product)
            return Response(_('Product deleted'), status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(_('Product not in cart'), status=status.HTTP_404_NOT_FOUND)


# class UpdateQuantity(views.APIView):
#     """
#     This view dell the  of product.
#     If cart is not exist create new cart one.
#     If product added return status HTTP_201_CREATED
#     If inbound parameters is wrong return status HTTP_400_BAD_REQUEST
#     If product out of stock return status HTTP_409_CONFLICT
#     """
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, row: int, column: int):
#         # get the existing object of ProductInstance
#         try:
#             product = ProductInstance.objects.get(diopter=row, cylinder=column)
#         except ProductInstance.DoesNotExist:
#             return Response(_('Product does not exist'), status=status.HTTP_400_BAD_REQUEST)

#         # get the existing customer cart
#         try:
#             order = Order.objects.get(customer=self.request.user, status=Order.InCart)
#         except Order.DoesNotExist:
#             return Response(_('Cart does not exist'), status=status.HTTP_400_BAD_REQUEST)
#         except Order.MultipleObjectsReturned:
#             return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

#         # get the existing OrderLine or create new one
#         if product.quantity_in_hand and product.quantity_in_hand > 0:
#             invoice_line, created = OrderLine.objects.get_or_create(product=product,
#                                                                            order=order,
#                                                                            defaults={'unit_price': product.price})
#             if invoice_line.quantity + 1 <= product.quantity_in_hand:
#                 invoice_line.quantity += 1
#             else:
#                 return Response(_('Product is out of stock'), status=status.HTTP_409_CONFLICT)

#         return Response(_('Product added to the cart'), status=status.HTTP_201_CREATED)


# class ConfirmOrder(views.APIView):
#     """
#     This view dell the product from cart.
#     If cart is not exist create new cart one.
#     If product added return status HTTP_201_CREATED
#     If inbound parameters is wrong return status HTTP_400_BAD_REQUEST
#     If product out of stock return status HTTP_409_CONFLICT
#     """
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, row: int, column: int):
#         # get the existing object of ProductInstance
#         try:
#             product = ProductInstance.objects.get(diopter=row, cylinder=column)
#         except ProductInstance.DoesNotExist:
#             return Response(_('Product does not exist'), status=status.HTTP_400_BAD_REQUEST)

#         # get the existing customer cart
#         try:
#             order = Order.objects.get(customer=self.request.user, status=Order.InCart)
#         except Order.DoesNotExist:
#             return Response(_('Cart does not exist'), status=status.HTTP_400_BAD_REQUEST)
#         except Order.MultipleObjectsReturned:
#             return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

#         # get the existing OrderLine or create new one
#         if product.quantity_in_hand and product.quantity_in_hand > 0:
#             invoice_line, created = OrderLine.objects.get_or_create(product=product,
#                                                                            order=order,
#                                                                            defaults={'unit_price': product.price})
#             if invoice_line.quantity + 1 <= product.quantity_in_hand:
#                 invoice_line.quantity += 1
#             else:
#                 return Response(_('Product is out of stock'), status=status.HTTP_409_CONFLICT)

#         return Response(_('Product added to the cart'), status=status.HTTP_201_CREATED)


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
