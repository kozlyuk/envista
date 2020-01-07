""" Models for managing products """

import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from accounts.models import User


class Product(models.Model):
    """ Model contains Products """
    title = models.CharField(_('Product title'), max_length=255)
    short_description = models.TextField(_('Product description'), blank=True)
    long_description = models.TextField(_('Product description'), blank=True)
    product_image = models.ImageField(_('Product image'), upload_to='Product/image')
    brand_name = models.CharField(_('Brand name'), max_length=32, unique=True)
    brand_image = models.ImageField(_('Brand Image'), upload_to='brands/', blank=True, null=True)

    # Creator and Date information
    created_by = models.ForeignKey(User, verbose_name=_('Created by'),
        blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-date_created', 'title']

    def __str__(self):
        return self.title


class DiopterPower(models.Model):
    """ Model contains product Diopter Range values """
    value = models.CharField(_('Value'), max_length=4)

    class Meta:
        verbose_name = _('Diopter Power')
        verbose_name_plural = _('Diopter Powers')

    def __str__(self):
        return self.value


class  Cylinder(models.Model):
    """ Model contains product Cylinder values """
    value = models.CharField(_('Value'), max_length=4)

    class Meta:
        verbose_name = _('Cylinder')
        verbose_name_plural = _('Cylinders')

    def __str__(self):
        return self.value


class ProductInstance(models.Model):
    """ Model contains instances of products """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    diopter = models.ForeignKey(DiopterPower, on_delete=models.PROTECT)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.PROTECT)
    price = models.DecimalField(_('Product price'), max_digits=8, decimal_places=2, default=0)
    # Creator and Date information
    created_by = models.ForeignKey(User, verbose_name=_('Created by'),
        blank=True, null=True, on_delete=models.CASCADE)
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Product Instance')
        verbose_name_plural = _('Product Instances')

    def __str__(self):
        return self.serial_number

    def get_price(self):
        return str(self.price) + ' ' + settings.DEFAULT_CURRENCY


class Stock(models.Model):
    product_instance = models.OneToOneField(ProductInstance, verbose_name=_('Product'), on_delete=models.CASCADE)
    quantity_in_hand = models.IntegerField(_('Quantity in hand'))

    class Meta:
        verbose_name = _('Stock')
        verbose_name_plural = _('Stocks')

    def __str__(self):
        return self.quantity_in_hand
