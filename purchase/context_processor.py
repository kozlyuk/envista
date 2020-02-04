from purchase.models import Order

def new_orders_count(request):
    """ Reurn count of new orders """
    return {'new_orders_count' : Order.objects.filter(status=Order.NewOrder).count()}
