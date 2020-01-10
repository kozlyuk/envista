from django.urls import path, include

from purchase import api


urlpatterns = (
    path("api/v1/add_to_basket/<int:row>/<int:column>/", api.AddToBasket.as_view()),

)
