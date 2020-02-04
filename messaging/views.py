from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
import telebot

from accounts.models import User


envista_bot = telebot.TeleBot(settings.TG_TOKEN)

@csrf_exempt
def bot(request):

    if request.META['CONTENT_TYPE'] == 'application/json':

        json_data = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_data)
        envista_bot.process_new_updates([update])
        return HttpResponse("")
    else:
        raise PermissionDenied


@envista_bot.message_handler(commands=['start'])
def send_welcome(message):
    msg = "Привіт для реєстрації на сповіщення натисни /register"
    envista_bot.send_message(message.chat.id, msg)


@envista_bot.message_handler(commands=['register'])
def register(message):
    msg = envista_bot.reply_to(message, "Введіть свою електронну пошту")
    envista_bot.register_next_step_handler(msg, process_email_step)


def process_email_step(message):
    try:
        email = message.text.lower()
        if User.objects.filter(groups__name='Менеджери', email=email).exists():
            user = User.objects.get(groups__name='Менеджери', email=email)
            user.telegram_id = message.from_user.id
            user.save()
            envista_bot.reply_to(message, "Дякую. Ви зареєстровані на сповіщення")
        else:
            envista_bot.reply_to(message, "Менеджера з такою електронною поштою не існує")
    except Exception:
        envista_bot.reply_to(message, 'Упс..')


def send_notice(chat_id: int, msg: str):
    envista_bot.send_message(chat_id, msg)
