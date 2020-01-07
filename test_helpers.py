import random
import string

from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

from product import models as product_models
from purchase import models as purchase_models


def random_string(length=10):
    # Create a random string of length length
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def create_User(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return User.objects.create(**defaults)


def create_AbstractUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractUser.objects.create(**defaults)


def create_AbstractBaseUser(**kwargs):
    defaults = {
        "username": "%s_username" % random_string(5),
        "email": "%s_username@tempurl.com" % random_string(5),
    }
    defaults.update(**kwargs)
    return AbstractBaseUser.objects.create(**defaults)


def create_Group(**kwargs):
    defaults = {
        "name": "%s_group" % random_string(5),
    }
    defaults.update(**kwargs)
    return Group.objects.create(**defaults)


def create_ContentType(**kwargs):
    defaults = {
    }
    defaults.update(**kwargs)
    return ContentType.objects.create(**defaults)


def create_product_ProductInstance(**kwargs):
    defaults = {}
    defaults["date_updated"] = datetime.now()
    defaults["date_created"] = datetime.now()
    defaults["price"] = ""
    if "diopter" not in kwargs:
        defaults["diopter"] = create_DiopterPower()
    if "cylinder" not in kwargs:
        defaults["cylinder"] = create_Cylinder()
    if "product" not in kwargs:
        defaults["product"] = create_Product()
    defaults.update(**kwargs)
    return product_models.ProductInstance.objects.create(**defaults)
def create_product_Stock(**kwargs):
    defaults = {}
    defaults["quantity_in_hand"] = ""
    if "product_instance" not in kwargs:
        defaults["product_instance"] = create_ProductInstance()
    defaults.update(**kwargs)
    return product_models.Stock.objects.create(**defaults)
def create_product_Cylinder(**kwargs):
    defaults = {}
    defaults["value"] = ""
    defaults.update(**kwargs)
    return product_models.Cylinder.objects.create(**defaults)
def create_product_Product(**kwargs):
    defaults = {}
    defaults["date_created"] = datetime.now()
    defaults["date_updated"] = datetime.now()
    defaults["brand_name"] = ""
    defaults["brand_image"] = ""
    defaults["short_description"] = ""
    defaults["long_description"] = ""
    defaults["product_image"] = ""
    defaults["title"] = ""
    defaults.update(**kwargs)
    return product_models.Product.objects.create(**defaults)
def create_product_DiopterPower(**kwargs):
    defaults = {}
    defaults["value"] = ""
    defaults.update(**kwargs)
    return product_models.DiopterPower.objects.create(**defaults)
def create_purchase_PurchaseInvoiceLine(**kwargs):
    defaults = {}
    defaults["quantity"] = ""
    defaults["unit_price"] = ""
    if "product" not in kwargs:
        defaults["product"] = create_ProductInstance()
    if "purchase" not in kwargs:
        defaults["purchase"] = create_Purchase()
    defaults.update(**kwargs)
    return purchase_models.PurchaseInvoiceLine.objects.create(**defaults)
def create_purchase_OrderInvoiceLine(**kwargs):
    defaults = {}
    defaults["unit_price"] = ""
    defaults["quantity"] = ""
    if "product" not in kwargs:
        defaults["product"] = create_ProductInstance()
    if "order" not in kwargs:
        defaults["order"] = create_Order()
    defaults.update(**kwargs)
    return purchase_models.OrderInvoiceLine.objects.create(**defaults)
def create_purchase_Order(**kwargs):
    defaults = {}
    defaults["invoice_date"] = datetime.now()
    defaults["date_created"] = datetime.now()
    defaults["date_updated"] = datetime.now()
    defaults["invoice_file"] = ""
    defaults["comment"] = ""
    defaults["pay_status"] = ""
    defaults["value"] = ""
    defaults["invoice_number"] = ""
    defaults["status"] = ""
    if "customer" not in kwargs:
        defaults["customer"] = create_User()
    defaults.update(**kwargs)
    return purchase_models.Order.objects.create(**defaults)
def create_purchase_Purchase(**kwargs):
    defaults = {}
    defaults["comment"] = ""
    defaults["invoice_number"] = ""
    defaults["invoice_date"] = datetime.now()
    defaults["date_created"] = datetime.now()
    defaults["date_updated"] = datetime.now()
    if "customer" not in kwargs:
        defaults["customer"] = create_User()
    defaults.update(**kwargs)
    return purchase_models.Purchase.objects.create(**defaults)
