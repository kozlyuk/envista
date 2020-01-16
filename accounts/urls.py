from django.urls import path

from accounts.api import UserDetailsView

urlpatterns = (
    path("api/v1/User/", UserDetailsView.as_view()),
)
