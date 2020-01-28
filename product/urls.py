from django.urls import path, include

from product.api import ProductDetailsView


urlpatterns = (
    path("api/v1/get_product/", ProductDetailsView.as_view()),
)
