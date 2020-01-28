from django.urls import path

from purchase import api

urlpatterns = (
    path("api/v1/get_stocks/", api.GetStocks.as_view()),
    path("api/v1/add_to_cart/<int:row>/<int:column>/", api.AddToCart.as_view()),
    path("api/v1/get_cart/", api.GetCart.as_view()),
    path("api/v1/update_quantity/<int:product_pk>/<int:quantity>/", api.UpdateQuantity.as_view()),
    path("api/v1/confirm_order/", api.ConfirmOrder.as_view()),

)
