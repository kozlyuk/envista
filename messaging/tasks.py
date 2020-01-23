from __future__ import absolute_import, unicode_literals

from celery.utils.log import get_task_logger
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from envista.celery import app

from accounts.models import User
from purchase.models import OrderLine, Order

logger = get_task_logger(__name__)

@app.task
def send_confirmation_email(user_id, order_id):

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logger.info("Tried to send verification email to non-existing user '%s'", user_id)

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.info("Tried to send verification email to non-existing user '%s'", order_id)

    context = {'customer': user,
               'order': order,
               'orderlines': order.orderline_set.all(),
               'url': settings.SITE_URL,
               'signature': settings.SIGNATURE}

    title = "Підтвердження замовлення {}".format(order.invoice_number)
    msg_plain = title
    msg_html = render_to_string('order_confirmation.html', context)

    if send_mail(title, msg_plain, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=msg_html):
        logger.info("Confirmation email to %s sent", user)
