from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot
import logging


envista_bot = telebot.TeleBot(settings.TG_TOKEN)

@csrf_exempt
def bot(request):

    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        envista_bot.process_new_updates([update])

        return HttpResponse("")

    raise PermissionDenied


@envista_bot.message_handler(content_types=["text"])
def get_okn(message):
    envista_bot.send_message(message.chat.id, "Hello, bot!")
