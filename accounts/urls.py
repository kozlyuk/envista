from django.urls import path

from accounts.api import UserDetailsView, Register, Activate, GetOrders, CancelOrder

urlpatterns = (
    path("api/v1/user/", UserDetailsView.as_view()),
    path("api/v1/get_orders/", GetOrders.as_view(), name='get_orders'),
    # path("api/v1/cancel_order/<int:order>/", CancelOrder.as_view(), name='cancel_order'),

    path("api/v1/register/", Register.as_view(), name='register'),
    path("api/v1/activate/<str:uidb64>/<str:token>/", Activate.as_view(), name='activate'),
)
