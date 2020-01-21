from django.urls import path, include
from rest_framework import routers

from purchase import api

router = routers.DefaultRouter()
router.register("PurchaseLine", api.PurchaseLineViewSet)
router.register("OrderLine", api.OrderLineViewSet)
router.register("Order", api.OrderViewSet)
router.register("Purchase", api.PurchaseViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("api/v1/get_stocks/", api.GetStocks.as_view()),
    path("api/v1/add_to_cart/<int:row>/<int:column>/", api.AddToCart.as_view()),
    path("api/v1/get_cart/", api.GetCart.as_view()),
    path("api/v1/del_from_cart/<int:row>/<int:column>/", api.DelFromCart.as_view()),
    path("api/v1/update_quantity/<int:pk>/<int:quantity>/", api.UpdateQuantity.as_view()),
    path("api/v1/confirm_order/", api.ConfirmOrder.as_view()),

)
