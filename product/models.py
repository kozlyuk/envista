""" Models for managing products """

import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
#from django.utils.timezone import now
from django_userforeignkey.models.fields import UserForeignKey
from warehouse.models import Stock


def image_directory_path(instance, filename):
    """ file will be uploaded to MEDIA_ROOT/product/product_upc/<filename> """
    return 'products/{0}/{1}'.format(instance.product.upc, filename)


class Brand(models.Model):
    """ Model contains product Brands """
    name = models.CharField(_('Brand name'), max_length=32, unique=True)
    image = models.ImageField(_('Brand Image'), upload_to='brands/', blank=True, null=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ['name']

    def __str__(self):
        return self.name

    def products_count(self):
        """ return product quantity of brand"""
        return self.product_set.all().count()
    products_count.short_description = _('Products count')


class Product(models.Model):
    """ Model contains Products """
    title = models.CharField(_('Product title'), max_length=255)
    brand = models.ForeignKey(Brand, verbose_name=_('Product Brand'), on_delete=models.PROTECT)
    description = models.TextField(_('Product description'), blank=True)
    default_uom = models.CharField(_('Default units of measurement'), max_length=8, default=_('pcs.'))
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-date_created', 'title']

    def __str__(self):
        return self.title

    def actual_price(self):
        """ return actual product price for current date """
        actual_price = None
        actual_from_date = None
        for price in self.pricerecord_set.all():
            if price.from_date <= datetime.date.today():
                if not actual_from_date or actual_from_date < price.from_date:
                    actual_from_date = price.from_date
                    actual_price = price.regular_price
        return actual_price
    actual_price.short_description = _('Actual price')

    def get_image(self):
        """ return first image path """
        return self.image_set.all().first()
    get_image.short_description = _('Image')


class Image(models.Model):
    """ Model contains product Images """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(_('Product image'), upload_to=image_directory_path)
    main = models.BooleanField(_('Is main image'), default=True)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')

    def __str__(self):
        return self.image.url


class PriceRecord(models.Model):
    """ Model contains product Price records """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    from_date = models.DateField(_('Actual from'))
    price = models.DecimalField(_('Product price'), max_digits=8, decimal_places=2, default=0)
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Price Record')
        verbose_name_plural = _('Price Records')

    def __str__(self):
        return str(self.regular_price) + ' ' + settings.DEFAULT_CURRENCY


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
    upc = models.CharField(_('Product UPC'), max_length=32, unique=True)
    stock = models.ForeignKey(Stock, on_delete=models.PROTECT)
    # Creator and Date information
    created_by = UserForeignKey(auto_user_add=True, verbose_name=_('Created by'))
    date_created = models.DateField(_('Created'), auto_now_add=True)
    date_updated = models.DateField(_('Updated'), auto_now=True)

    class Meta:
        verbose_name = _('Product Instance')
        verbose_name_plural = _('Product Instances')

    def __str__(self):
        return self.serial_number
