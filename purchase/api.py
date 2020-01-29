""" API for Purchase app"""

from datetime import date
from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, views, status
from rest_framework.response import Response

from purchase.models import Order, OrderLine, Purchase, PurchaseLine
from product.models import ProductInstance, Cylinder, DiopterPower
from messaging.tasks import send_confirmation_email, send_new_order_email


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
        for row in DiopterPower.objects.order_by('pk').values_list('value', flat=True):
            quantity_list = ProductInstance.objects.filter(diopter__value=row).order_by('pk') \
                                                   .values_list('quantity_in_hand', flat=True)
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
            order_line = [index, line.product.product.title, line.diopter.value, line.cylinder.value,
                line.quantity, line.unit_price, line.product.pk, line.product.quantity_in_hand]
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
            cylinder = Cylinder.objects.get(pk=column)
            diopter = DiopterPower.objects.get(pk=row)
            order_line, created = OrderLine.objects.get_or_create(product=product,
                                                                  order=order,
                                                                  defaults={'unit_price': product.price,
                                                                            'cylinder': cylinder,
                                                                            'diopter': diopter})
            if order_line.quantity + 1 <= product.quantity_in_hand:
                order_line.quantity += 1
                order_line.save()
                return Response(_('Product added to the cart'), status=status.HTTP_201_CREATED)
        return Response(_('Product is out of stock'), status=status.HTTP_409_CONFLICT)


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

    def get(self, request, product_pk: int, quantity: int):
        # get the existing object of ProductInstance
        try:
            product = ProductInstance.objects.get(pk=product_pk)
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

        # reduce stocks
        for order_line in order.orderline_set.all():
            # delete orderline if its quantity is 0
            if order_line.quantity == 0:
                order_line.delete()
                continue
            order_line.product.quantity_in_hand -= order_line.quantity
            order_line.product.save()

        # check if order not empty
        if order.orderline_set.exists():
            # change order status to NewOrder and assign invoice number
            order.status = Order.NewOrder
            order.invoice_number = order.invoice_number_generate()
            order.invoice_date = date.today()
            order.value = order.value_total()
            order.created_by = self.request.user
            order.save()

            # send confirmation email
            try:
                if not self.request.user.groups.filter(name='Менеджери').exists():
                    send_confirmation_email.delay(order.pk)
                send_new_order_email.delay(order.pk)
            except ConnectionError:
                pass
            return Response(_('Order accepted. Wait for call from manager please!'),
                            status=status.HTTP_201_CREATED)
        else:
            return Response(_('Order if empty! Please add products'),
                            status=status.HTTP_412_PRECONDITION_FAILED)


class GetPurchaseTable(views.APIView):
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
        for row in DiopterPower.objects.order_by('pk').values_list('value', flat=True):
            quantity_list = ProductInstance.objects.filter(diopter__value=row).order_by('pk') \
                                                   .values_list('quantity_in_hand', flat=True)
            json_data[1]["rows"].append({"row": row, "quantities": quantity_list})
        return Response(json_data, status=status.HTTP_200_OK)


class GetPurchaseList(views.APIView):
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
        for row in DiopterPower.objects.order_by('pk').values_list('value', flat=True):
            quantity_list = ProductInstance.objects.filter(diopter__value=row).order_by('pk') \
                                                   .values_list('quantity_in_hand', flat=True)
            json_data[1]["rows"].append({"row": row, "quantities": quantity_list})
        return Response(json_data, status=status.HTTP_200_OK)


class AddToPurchase(views.APIView):
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
            cylinder = Cylinder.objects.get(pk=column)
            diopter = DiopterPower.objects.get(pk=row)
            order_line, created = OrderLine.objects.get_or_create(product=product,
                                                                  order=order,
                                                                  defaults={'unit_price': product.price,
                                                                            'cylinder': cylinder,
                                                                            'diopter': diopter})
            if order_line.quantity + 1 <= product.quantity_in_hand:
                order_line.quantity += 1
                order_line.save()
                return Response(_('Product added to the cart'), status=status.HTTP_201_CREATED)
        return Response(_('Product is out of stock'), status=status.HTTP_409_CONFLICT)


class UpdatePurchaseLine(views.APIView):
    """
    This view update the product in cart
    If product updated return status HTTP_200_OK
    If product not found in ProductInstance's return HTTP_404_NOT_FOUND
    If product not found in cart return status HTTP_404_NOT_FOUND
    If product out of stock return status HTTP_409_CONFLICT
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, product_pk: int, quantity: int):
        # get the existing object of ProductInstance
        try:
            product = ProductInstance.objects.get(pk=product_pk)
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


class ConfirmPurchase(views.APIView):
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
        order.invoice_date = date.today()
        order.value = order.value_total()
        order.created_by = self.request.user
        order.save()

        # reduce stocks
        for order_line in order.orderline_set.all():
            order_line.product.quantity_in_hand -= order_line.quantity
            order_line.product.save()

        # send confirmation email
        if not self.request.user.groups.filter(name='Менеджери').exists():
            send_confirmation_email.delay(order.pk)
        send_new_order_email.delay(order.pk)

        return Response(_('Order accepted. Wait for call from manager please!'),
                        status=status.HTTP_201_CREATED)
