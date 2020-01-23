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
def send_confirmation_email(customer_id, order_id):
    """ send email to client about order confirmation """

    try:
        customer = User.objects.get(pk=customer_id)
    except User.DoesNotExist:
        logger.warning("Tried to send email to non-existing user '%s'", customer_id)

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.warning("Tried to send email to non-existing user '%s'", order_id)

    context = {'customer': customer,
               'order': order,
               'orderlines': order.orderline_set.all(),
               'signature': settings.SIGNATURE}

    title = "Підтвердження замовлення {}".format(order.invoice_number)
    msg_plain = title
    msg_html = render_to_string('order_confirmation.html', context)

    if send_mail(title, msg_plain, settings.DEFAULT_FROM_EMAIL, [customer.email], html_message=msg_html):
        logger.info("Confirmation email to %s sent", customer)


@app.task
def send_new_order_email(order_id):
    """ send email to all managers about receiving a new order """

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.warning("Tried to send verification email to non-existing user '%s'", order_id)

    managers = User.objects.filter(groups__name='Менеджери') \
                           .exclude(pk=order.customer.pk) \
                           .values_list('email', flat=True)

    context = {'order': order,
               'signature': settings.SIGNATURE}

    title = "Отримано нове замовлення {}".format(order.invoice_number)
    msg_plain = title
    msg_html = render_to_string('order_received.html', context)

    if send_mail(title, msg_plain, settings.DEFAULT_FROM_EMAIL, managers, html_message=msg_html):
        logger.info("Email about receiving a new order sent to all managers")


@app.task
def send_status_change_email(customer_id, order_id):
    """ send email about changing order status to customer """

    try:
        customer = User.objects.get(pk=customer_id)
    except User.DoesNotExist:
        logger.warning("Tried to send email to non-existing user '%s'", customer_id)

    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        logger.warning("Tried to send email to non-existing user '%s'", order_id)

    context = {'customer': customer,
               'order': order,
               'signature': settings.SIGNATURE}

    title = "Статус Вашого замовлення {} змінено".format(order.invoice_number)
    msg_plain = title
    msg_html = render_to_string('status_change.html', context)

    if send_mail(title, msg_plain, settings.DEFAULT_FROM_EMAIL, [customer.email], html_message=msg_html):
        logger.info("Changing status email to %s sent", customer)
