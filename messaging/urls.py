from django.urls import path

from messaging.views import bot

urlpatterns = (
    path("webhook/telegram/", bot, name='telegram_bot'),
)
