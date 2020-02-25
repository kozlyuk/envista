from __future__ import absolute_import, unicode_literals

from smtplib import SMTPException
from celery.utils.log import get_task_logger
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from envista.celery import app

from accounts.models import User
from purchase.models import Order
from messaging.views import send_notice

logger = get_task_logger(__name__)

@app.task
def send_confirmation_email(order_id):
    """ send email to client about order confirmation """

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.warning("Order with id '%s' does not exist", order_id)

    context = {'customer': order.customer,
               'order': order,
               'orderlines': order.orderline_set.all(),
               'signature': settings.SIGNATURE}

    title = "Підтвердження замовлення {}".format(order.invoice_number)
    msg_plain = title
    msg_html = render_to_string('order_confirmation.html', context)

    try:
        send_mail(title, msg_plain, settings.DEFAULT_FROM_EMAIL,
                  [order.customer.email], html_message=msg_html)
        logger.info("Confirmation email to %s sent", order.customer)
    except SMTPException:
        logger.info("Connection error while send email to %s", order.customer)


@app.task
def send_new_order_email(order_id):
    """ send email to all managers about receiving a new order """

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.warning("Order with id '%s' does not exist", order_id)

    managers = User.objects.filter(groups__name='Менеджери') \
                   .values_list('email', flat=True)

    context = {'customer': order.customer,
               'order': order,
               'orderlines': order.orderline_set.all(),
               'signature': settings.SIGNATURE}

    title = f'Отримано нове замовлення {order.invoice_number}'
    msg_plain = title
    msg_html = render_to_string('order_received.html', context)

    try:
        send_mail(title, msg_plain, settings.DEFAULT_FROM_EMAIL,
                  managers, html_message=msg_html)
        logger.info("Email about receiving a new order sent to all managers")
    except SMTPException:
        logger.info("Connection error while send email to managers")

    # send telegram notification
    telegram_ids = User.objects.filter(groups__name='Менеджери', telegram_id__isnull=False) \
                   .values_list('telegram_id', flat=True)
    title += f'\nПокупець - {order.customer.first_name} {order.customer.last_name}'
    for orderline in order.orderline_set.all():
        title += (f'\n{orderline.product.product.title} {orderline.product.diopter.value}-'
                  f'{orderline.product.cylinder.value} - {orderline.quantity}шт.')
    for chat_id in telegram_ids:
        send_notice(chat_id, title)
        logger.info("Telegram notification sent to chat_id '%s'", chat_id)


@app.task
def send_status_change_email(order_id):
    """ send email about changing order status to customer """

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.warning("Order with id '%s' does not exist", order_id)

    context = {'customer': order.customer,
               'order': order,
               'status': order.get_status_display,
               'orderlines': order.orderline_set.all(),
               'signature': settings.SIGNATURE}

    title = "Статус Вашого замовлення {} змінено".format(order.invoice_number)
    msg_plain = title
    msg_html = render_to_string('status_change.html', context)

    try:
        send_mail(title, msg_plain, settings.DEFAULT_FROM_EMAIL,
                  [order.customer.email], html_message=msg_html)
        logger.info("Changing status email to %s sent", order.customer)
    except SMTPException:
        logger.info("Connection error while send email to %s", order.customer)
