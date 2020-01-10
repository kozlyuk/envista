from django.utils.translation import gettext_lazy as _
from rest_framework import permissions, views, status
from rest_framework.response import Response

# from . import serializers
from product.models import ProductInstance
from purchase.models import Order, OrderInvoiceLine


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
        # get the existing object of ProductInstance
        # if object does not exist return HTTP_400_BAD_REQUEST
        try:
            product = ProductInstance.objects.get(diopter=row, cylinder=column)
        except ProductInstance.DoesNotExist:
            return Response(_('Product does not exist'), status=status.HTTP_400_BAD_REQUEST)

        # get the existing customer cart or create new one
        if 'purchase_id' in self.request.session and \
                Order.objects.filter(pk=self.request.session.get('purchase_id')).exists():
            purchase = Purchase.objects.get(pk=self.request.session.get('purchase_id'))
        else:
            purchase = Purchase.objects.create(invoice_number='Cart')
            self.request.session['purchase_id'] = purchase.id

        # get the existing OrderInvoiceLine or create new one
        if product.quantity_in_hand and product.quantity_in_hand > 0:
            invoice_line, created = InvoiceLine.objects.get_or_create(product=product,
                                                                      purchase=purchase,
                                                                      defaults={'unit_price': product.price})
            if invoice_line.quantity + 1 <= product.quantity_in_hand:
                invoice_line.quantity += 1
            else:
                Response(_('Product is out of stock'), status=status.HTTP_409_CONFLICT)

        return Response(_('Product added to the cart'), status=status.HTTP_201_CREATED)
