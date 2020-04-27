from django.urls import path

from accounts.api import UserDetailsView, Register, Activate, GetOrders

urlpatterns = (
    path("api/v1/user/", UserDetailsView.as_view()),

    path("api/v1/get_orders/<str:customer>/", GetOrders.as_view(), name='get_orders'),

    path("api/v1/register/", Register.as_view(), name='register'),
    path("api/v1/activate/<str:uidb64>/<str:token>/", Activate.as_view(), name='activate'),
)
