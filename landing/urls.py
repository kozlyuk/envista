"""invista.landing URL Configuration"""

from django.urls import path

from landing import views


urlpatterns = (
    path("", views.MainView.as_view(), name='landing_main'),
)
