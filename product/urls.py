from django.urls import path

from product.api import ProductDetailsView


urlpatterns = (
    path("api/v1/get_product/", ProductDetailsView.as_view()),
)
