""" Models for managing products """

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """ Model contains Products """
    title = models.CharField(_('Product title'), max_length=255, unique=True)
    short_description = models.TextField(_('Short description'))
    product_image = models.ImageField(_('Product image'), upload_to='product/')
    brand_name = models.CharField(_('Brand name'), max_length=32)
    brand_image = models.ImageField(_('Brand Image'), upload_to='brand/')
    specifications_url = models.URLField(_('Specification'), blank=True, null=True)
    footer = models.CharField(_('Site footer'), max_length=255, blank=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def __str__(self):
        return self.title


class DiopterPower(models.Model):
    """ Model contains product Diopter Range values """
    value = models.CharField(_('Value'), max_length=4)

    class Meta:
        verbose_name = _('Diopter Power')
        verbose_name_plural = _('Diopter Powers')
        ordering = ['id']

    def __str__(self):
        return self.value


class  Cylinder(models.Model):
    """ Model contains product Cylinder values """
    value = models.CharField(_('Value'), max_length=4)

    class Meta:
        verbose_name = _('Cylinder')
        verbose_name_plural = _('Cylinders')
        ordering = ['id']

    def __str__(self):
        return self.value


class ProductInstance(models.Model):
    """ Model contains instances of products """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    diopter = models.ForeignKey(DiopterPower, on_delete=models.PROTECT)
    cylinder = models.ForeignKey(Cylinder, on_delete=models.PROTECT)
    price = models.DecimalField(_('Product price'), max_digits=8, decimal_places=2, default=0)
    quantity_in_hand = models.PositiveSmallIntegerField(_('Quantity in hand'), default=0)

    class Meta:
        verbose_name = _('Product Instance')
        verbose_name_plural = _('Product Instances')
        ordering = ['id']

    def __str__(self):
        return self.product.title + ' ' + str(self.cylinder) + '-' + str(self.diopter)

    def get_price(self):
        """Return price with currency"""
        return str(self.price) + ' ' + settings.DEFAULT_CURRENCY
