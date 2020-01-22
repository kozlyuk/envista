""" Models for managing purchases """

import datetime
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.db.models import F, FloatField, Sum

from accounts.models import User
from product.models import ProductInstance, DiopterPower, Cylinder


def docs_directory_path(filename):
    """  file will be uploaded to MEDIA_ROOT/invoices/Year/Month/<filename> """
    return 'invoices/{0}/{1}/{2}'.format(datetime.datetime.now().year, datetime.datetime.now().month, filename)


class Purchase(models.Model):
    """ Abstract Model contains Purchases """
    products = models.ManyToManyField(ProductInstance, through='PurchaseLine', related_name='purchases',
                                      verbose_name=_('Goods'), blank=True)
    invoice_number = models.CharField(_('Invoice number'), max_length=45)
    invoice_date = models.DateField(_('Invoice date'), default=datetime.date.today)
    value = models.DecimalField(_('Value'), max_digits=8, decimal_places=2, default=0)
    comment = models.TextField(_('Comment'), blank=True)
    # Creator and Date information
    created_by = models.ForeignKey(User, verbose_name=_('Created by'), related_name='creator_purchases',
                                   blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        verbose_name = _('Purchase')
        verbose_name_plural = _('Purchases')
        ordering = ['-date_created', '-invoice_number']

    def __str__(self):
        return self.invoice_number


class Order(models.Model):
    """ Model contains Sales, Carts """
    InCart = 'IC'
    NewOrder = 'NO'
    Cancelled = 'CN'
    Confirmed = 'CF'
    Sent = 'ST'
    Received = 'RC'
    Returned = 'RT'
    STATUS_CHOICES = (
        (InCart, _('Products in cart')),
        (NewOrder, _('New order')),
        (Cancelled, _('Order canceled')),
        (Confirmed, _('Order confirmed')),
        (Sent, _('Order sent')),
        (Returned, _('Order returned')),
    )
    NotPaid = 'NP'
    AdvancePaid = 'AP'
    PaidUp = 'PU'
    # PAYMENT_STATUS_CHOICES = (
    #     (NotPaid, 'Не оплачений'),
    #     (AdvancePaid, 'Оплачений аванс'),
    #     (PaidUp, 'Оплачений')
    #     )
    products = models.ManyToManyField(ProductInstance, through='OrderLine', related_name='orders',
                                      verbose_name=_('Goods'), blank=True)
    customer = models.ForeignKey(User, verbose_name=_('Customer'), blank=True, null=True, on_delete=models.PROTECT)
    invoice_number = models.CharField(_('Invoice number'), max_length=45)
    invoice_date = models.DateField(_('Invoice date'), default=datetime.date.today)
    comment = models.TextField(_('Comment'), blank=True)
    status = models.CharField(_('Order status'), max_length=2, choices=STATUS_CHOICES, default=InCart)
    # pay_status = models.CharField('Статус оплати', max_length=2, choices=PAYMENT_STATUS_CHOICES, default=NotPaid)
    value = models.DecimalField(_('Value'), max_digits=8, decimal_places=2, default=0)
    invoice_file = models.FileField(_('Download Invoice'), upload_to=docs_directory_path, blank=True, null=True)
    # Creator and Date information
    created_by = models.ForeignKey(User, verbose_name=_('Created by'), related_name='creator_orders',
                                   blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-date_created', 'invoice_number']

    def __str__(self):
        return self.invoice_number

    def value_total(self):
        """ return calculated from invoice_lines purchase value"""
        return self.orderline_set.aggregate(total_value=Sum(F('quantity')*F('unit_price'),
                                                            output_field=FloatField())) \
                                            ['total_value'] or 0
    value_total.short_description = _('Calculated invoice value')

    @classmethod
    def invoice_number_generate(cls):
        """ return autogenerated invoice number"""
        today_str = datetime.date.today().strftime('%Y%m%d')
        today_orders_count = cls.objects.filter(invoice_number__startswith=today_str).count()
        return today_str + '-' + str(today_orders_count + 1)
    invoice_number_generate.short_description = _('Generated invoice number')


class PurchaseLine(models.Model):
    """ Model contains InvoiceLines for Purchases model """
    purchase = models.ForeignKey(Purchase, verbose_name=_('Purchase'), on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInstance, verbose_name=_('Goods'), on_delete=models.PROTECT)
    diopter = models.ForeignKey(DiopterPower, on_delete=models.PROTECT)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(_('Quantity'), default=1)
    last_quantity = models.PositiveSmallIntegerField(default=0)
    unit_price = models.DecimalField(_('Unit price'), max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ['purchase', 'product']

    def save(self, *args, **kwargs):
        self.last_quantity = self.quantity
        super().save(*args, **kwargs) # Call the real save() method


class OrderLine(models.Model):
    """ Model contains InvoiceLines for Purchases model """
    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.CASCADE)
    product = models.ForeignKey(ProductInstance, verbose_name=_('Goods'), on_delete=models.PROTECT)
    diopter = models.ForeignKey(DiopterPower, on_delete=models.PROTECT)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(_('Quantity'), default=0)
    last_quantity = models.PositiveSmallIntegerField(default=0)
    unit_price = models.DecimalField(_('Unit price'), max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ['order', 'product']

    def save(self, *args, **kwargs):
        self.last_quantity = self.quantity
        super().save(*args, **kwargs) # Call the real save() method

    def value_total(self):
        """ return calculated invoice_line value"""
        return self.unit_price * self.quantity
    value_total.short_description = _('Calculated invoice_line value')
