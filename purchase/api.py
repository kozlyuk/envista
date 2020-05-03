""" API for Purchase app"""

from datetime import datetime
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

    def get(self, request):
        # get the existing customer cart
        try:
            order = Order.objects.get(customer=self.request.user, status=Order.InCart)
        except Order.DoesNotExist:
            return Response([{"lines":[]}], status=status.HTTP_200_OK)
        except Order.MultipleObjectsReturned:
            return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

        # send JSON-coded list of orderlines in customer cart
        json_data = []
        json_data.append({"availableorders": []})
        index = 0
        for line in order.orderline_set.filter(order_type=OrderLine.AvailableOrder):
            index += 1
            order_line = [index, line.product.product.title, line.diopter.value, line.cylinder.value,
                          line.quantity, line.unit_price, line.product.pk, line.product.quantity_in_hand]
            json_data[0]["availableorders"].append({"line": order_line})
        json_data.append({"orders_total": order.value_total()})

        # add JSON-coded list of orderlines in preorder
        json_data.append({"preorders": []})
        index = 0
        for line in order.orderline_set.filter(order_type=OrderLine.PreOrder):
            index += 1
            order_line = [index, line.product.product.title, line.diopter.value, line.cylinder.value,
                          line.quantity, line.unit_price, line.product.pk, line.product.quantity_in_hand]
            json_data[2]["preorders"].append({"line": order_line})
        json_data.append({"preorders_total": order.preorder_total()})
        return Response(json_data, status=status.HTTP_200_OK)


class AddToCart(views.APIView):
    """
    This view add to cart the instance of product
    If product added return status HTTP_201_CREATED
    If product not found in ProductInstance's return HTTP_404_NOT_FOUND
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    If product out of stock return status HTTP_409_CONFLICT
    """

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

        cylinder = Cylinder.objects.get(pk=column)
        diopter = DiopterPower.objects.get(pk=row)
        # Check availability of orderline
        if product.quantity_in_hand > 0:
            # get the existing Avaible OrderLine or create new one
            order_line, created = OrderLine.objects.get_or_create(product=product,
                                                                  order=order,
                                                                  order_type=OrderLine.AvailableOrder,
                                                                  defaults={'unit_price': product.price,
                                                                            'cylinder': cylinder,
                                                                            'diopter': diopter})
            if order_line.quantity + 1 <= product.quantity_in_hand:
                order_line.quantity += 1
                order_line.save()
                return Response(_('Product added to the cart'), status=status.HTTP_201_CREATED)
        # get the existing Preorder OrderLine or create new one
        order_line, created = OrderLine.objects.get_or_create(product=product,
                                                              order=order,
                                                              order_type=OrderLine.PreOrder,
                                                              defaults={'unit_price': product.price,
                                                                        'cylinder': cylinder,
                                                                        'diopter': diopter})
        order_line.quantity += 1
        order_line.save()
        return Response(_('Preorder added to the cart'), status=status.HTTP_201_CREATED)


class UpdateQuantity(views.APIView):
    """
    This view update the product in cart
    If product updated return status HTTP_200_OK
    If product not found in ProductInstance's return HTTP_404_NOT_FOUND
    If product not found in cart return status HTTP_404_NOT_FOUND
    If product out of stock return status HTTP_409_CONFLICT
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """

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
            if order_line.order_type == OrderLine.AvailableOrder and quantity > product.quantity_in_hand:
                return Response(_('Product is out of stock'), status=status.HTTP_409_CONFLICT)
            order_line.quantity = quantity
            order_line.save()
            return Response(_('Product updated'), status=status.HTTP_200_OK)
        except OrderLine.DoesNotExist:
            return Response(_('Product not in cart'), status=status.HTTP_404_NOT_FOUND)


class ConfirmOrder(views.APIView):
    """
    Change order status from InCart to NewOrder and assign invoice number
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """

    def get(self, request):
        # get the existing customer cart
        try:
            order = Order.objects.get(customer=self.request.user, status=Order.InCart)
        except Order.DoesNotExist:
            return Response(_('Cart does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Order.MultipleObjectsReturned:
            return Response(_('Few carts exists'), status=status.HTTP_400_BAD_REQUEST)

        # get all orderlines
        orderlines = order.orderline_set.all()

        # delete orderlines if its quantity is 0
        for order_line in orderlines:
            if order_line.quantity == 0:
                order_line.delete()
                continue

        # Create PreOrder from not alailable Orderlines
        preorder_lines = orderlines.filter(order_type=OrderLine.PreOrder)
        # check if order not empty
        if preorder_lines.exists():
            # Creating user cart or clear existing on loading.
            order = Order.objects.create(customer=self.request.user,
                                         status=Order.PreOrder,
                                         created_by=self.request.user,
                                         date_created=datetime.now()
                                         )
            for order_line in preorder_lines:
                order_line.order = order
                order_line.save()
            order.invoice_number = order.invoice_number_generate()
            order.value = order.value_total()
            order.lenses_sum = order.lenses_count()
            order.save()

        # Create NewOrder from alailable Orderlines
        available_lines = orderlines.filter(order_type=OrderLine.AvailableOrder)
        # check if order not empty
        if available_lines.exists():
            # reduce stocks
            for order_line in available_lines:
                order_line.product.quantity_in_hand -= order_line.quantity
                order_line.product.save()
            # change order status to NewOrder and assign invoice number
            order.status = Order.NewOrder
            order.invoice_number = order.invoice_number_generate()
            order.value = order.value_total()
            order.lenses_sum = order.lenses_count()
            order.created_by = self.request.user
            order.date_created = datetime.now()
            order.save()

        # send confirmation email
        if available_lines.exists() or preorder_lines.exists():
            if not self.request.user.groups.filter(name='Менеджери').exists():
                send_confirmation_email.delay(order.pk)
            send_new_order_email(order.pk) # TODO add delay on production
            return Response(_('Order accepted. Wait for call from manager please!'),
                            status=status.HTTP_201_CREATED)

        return Response(_('Order if empty! Please add products'),
                        status=status.HTTP_412_PRECONDITION_FAILED)


class GetPurchaseTable(views.APIView):
    """
    Creating purchase cart or get existing.
    Send JSON-coded list of quantities in purchase cart.
    """

    def get(self, request):
        # Creating purchase cart or get existing.
        purchase, created = Purchase.objects.get_or_create(created_by=self.request.user,
                                                           invoice_number='InProcess')

        # Sending JSON list of quantities in purchase cart.
        purchase_lines = purchase.purchaseline_set.values_list('diopter__value', 'cylinder__value')
        json_data = []
        json_data.append({"columns": Cylinder.objects.values_list('value', flat=True)})
        json_data.append({"rows": []})
        for row in DiopterPower.objects.order_by('pk').values_list('value', flat=True):
            quantity_list = []
            for column in Cylinder.objects.order_by('pk').values_list('value', flat=True):
                if (row, column) in purchase_lines:
                    quantity_list.append(purchase.purchaseline_set.get(cylinder__value=column, diopter__value=row) \
                        .quantity)
                else:
                    quantity_list.append(0)
            json_data[1]["rows"].append({"row": row, "quantities": quantity_list})
        return Response(json_data, status=status.HTTP_200_OK)


class GetPurchaseList(views.APIView):
    """
    Send JSON-coded list of purchaselines in customer purchase
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """

    def get(self, request):
        # get the existing customer purchase
        try:
            purchase = Purchase.objects.get(created_by=self.request.user, invoice_number='InProcess')
        except Purchase.DoesNotExist:
            return Response(_('Purchase does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Purchase.MultipleObjectsReturned:
            return Response(_('Few purchases exists'), status=status.HTTP_400_BAD_REQUEST)

        # send JSON-coded list of orderlines in customer cart
        json_data = []
        json_data.append({"lines": []})
        index = 0
        for line in purchase.purchaseline_set.all():
            index += 1
            purchase_line = [index, line.product.product.title, line.diopter.value,
                             line.cylinder.value, line.quantity, line.product.pk]
            json_data[0]["lines"].append({"line": purchase_line})
        return Response(json_data, status=status.HTTP_200_OK)



class AddToPurchase(views.APIView):
    """
    This view add to purchase cart the instance of product
    If product added return status HTTP_201_CREATED
    If product not found in ProductInstance's return HTTP_404_NOT_FOUND
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """

    def get(self, request, row: int, column: int):
        # get the existing object of ProductInstance
        try:
            product = ProductInstance.objects.get(diopter=row, cylinder=column)
        except ProductInstance.DoesNotExist:
            return Response(_('Product does not exist'), status=status.HTTP_404_NOT_FOUND)

        # get the existing customer purchase
        try:
            purchase = Purchase.objects.get(created_by=self.request.user, invoice_number='InProcess')
        except Purchase.DoesNotExist:
            return Response(_('Purchase does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Purchase.MultipleObjectsReturned:
            return Response(_('Few purchases exists'), status=status.HTTP_400_BAD_REQUEST)

        # get the existing PurchaseLine or create new one
        cylinder = Cylinder.objects.get(pk=column)
        diopter = DiopterPower.objects.get(pk=row)
        purchase_line, created = PurchaseLine.objects.get_or_create(product=product,
                                                                    purchase=purchase,
                                                                    defaults={'cylinder': cylinder,
                                                                              'diopter': diopter})

        purchase_line.quantity += 1
        purchase_line.save()
        return Response(_('Product added to the purchase'), status=status.HTTP_201_CREATED)


class UpdatePurchaseLine(views.APIView):
    """
    This view update the product in purchase
    If product updated return status HTTP_200_OK
    If product not found in ProductInstance's return HTTP_404_NOT_FOUND
    If product not found in purchase return status HTTP_404_NOT_FOUND
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """

    def get(self, request, product_pk: int, quantity: int):
        # get the existing object of ProductInstance
        try:
            product = ProductInstance.objects.get(pk=product_pk)
        except ProductInstance.DoesNotExist:
            return Response(_('Product does not exist'), status=status.HTTP_404_NOT_FOUND)

        # get the existing customer purchase
        try:
            purchase = Purchase.objects.get(created_by=self.request.user, invoice_number='InProcess')
        except Purchase.DoesNotExist:
            return Response(_('Purchase does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Purchase.MultipleObjectsReturned:
            return Response(_('Few purchases exists'), status=status.HTTP_400_BAD_REQUEST)

        # update the existing PurchaseLine or returm exception if it is not exists
        try:
            purchase_line = PurchaseLine.objects.get(product=product, purchase=purchase)
            purchase_line.quantity = quantity
            purchase_line.save()
            return Response(_('Product updated'), status=status.HTTP_200_OK)
        except PurchaseLine.DoesNotExist:
            return Response(_('Product not in cart'), status=status.HTTP_404_NOT_FOUND)


class ConfirmPurchase(views.APIView):
    """
    Assign invoice number to purchase and save it
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """

    def get(self, request):
        # get the existing customer purchase
        try:
            purchase = Purchase.objects.get(created_by=self.request.user, invoice_number='InProcess')
        except Purchase.DoesNotExist:
            return Response(_('Purchase does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Purchase.MultipleObjectsReturned:
            return Response(_('Few purchases exists'), status=status.HTTP_400_BAD_REQUEST)

        # restock
        for purchase_line in purchase.purchaseline_set.all():
            # delete purchaseline if its quantity is 0
            if purchase_line.quantity == 0:
                purchase_line.delete()
                continue
            purchase_line.product.quantity_in_hand += purchase_line.quantity
            purchase_line.product.save()

        # check if order not empty
        if purchase.purchaseline_set.exists():
            # assign invoice number to purchase and save it
            purchase.invoice_number = purchase.invoice_number_generate()
            purchase.date_created = datetime.now()
            purchase.save()
            return Response(_('Purchase accepted.'),
                            status=status.HTTP_201_CREATED)
        return Response(_('Purchase is empty! Please add products'),
                        status=status.HTTP_412_PRECONDITION_FAILED)


class ClearPurchase(views.APIView):
    """
    Clear all purchase_lines in Purchase
    If exists problems with cart return status HTTP_400_BAD_REQUEST
    """

    def get(self, request):
        # get the existing customer purchase
        try:
            purchase = Purchase.objects.get(created_by=self.request.user, invoice_number='InProcess')
        except Purchase.DoesNotExist:
            return Response(_('Purchase does not exist'), status=status.HTTP_400_BAD_REQUEST)
        except Purchase.MultipleObjectsReturned:
            return Response(_('Few purchases exists'), status=status.HTTP_400_BAD_REQUEST)

        # clear
        purchase.products.clear()
        return Response(_('Purchase cleared.'), status=status.HTTP_200_OK)
