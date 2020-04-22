from django.urls import path

from accounts.api import UserDetailsView, Register, Activate

urlpatterns = (
    path("api/v1/User/", UserDetailsView.as_view()),

    path("api/v1/register/", Register.as_view(), name='register'),
    path("api/v1/activate/<str:uidb64>/<str:token>/", Activate.as_view(), name='activate'),
)
