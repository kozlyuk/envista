from django.urls import path, include
from rest_framework import routers

from . import api


router = routers.DefaultRouter()
router.register("PurchaseInvoiceLine", api.PurchaseInvoiceLineViewSet)
router.register("OrderInvoiceLine", api.OrderInvoiceLineViewSet)
router.register("Order", api.OrderViewSet)
router.register("Purchase", api.PurchaseViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
)
