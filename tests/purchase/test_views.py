import pytest
import test_helpers

from django.urls import reverse
from django.test import Client


pytestmark = [pytest.mark.django_db]


def tests_PurchaseInvoiceLine_list_view():
    instance1 = test_helpers.create_purchase_PurchaseInvoiceLine()
    instance2 = test_helpers.create_purchase_PurchaseInvoiceLine()
    client = Client()
    url = reverse("purchase_PurchaseInvoiceLine_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_PurchaseInvoiceLine_create_view():
    product = test_helpers.create_ProductInstance()
    purchase = test_helpers.create_Purchase()
    client = Client()
    url = reverse("purchase_PurchaseInvoiceLine_create")
    data = {
        "quantity": 1,
        "unit_price": 1.0,
        "product": product.pk,
        "purchase": purchase.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_PurchaseInvoiceLine_detail_view():
    client = Client()
    instance = test_helpers.create_purchase_PurchaseInvoiceLine()
    url = reverse("purchase_PurchaseInvoiceLine_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_PurchaseInvoiceLine_update_view():
    product = test_helpers.create_ProductInstance()
    purchase = test_helpers.create_Purchase()
    client = Client()
    instance = test_helpers.create_purchase_PurchaseInvoiceLine()
    url = reverse("purchase_PurchaseInvoiceLine_update", args=[instance.pk, ])
    data = {
        "quantity": 1,
        "unit_price": 1.0,
        "product": product.pk,
        "purchase": purchase.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_OrderInvoiceLine_list_view():
    instance1 = test_helpers.create_purchase_OrderInvoiceLine()
    instance2 = test_helpers.create_purchase_OrderInvoiceLine()
    client = Client()
    url = reverse("purchase_OrderInvoiceLine_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_OrderInvoiceLine_create_view():
    product = test_helpers.create_ProductInstance()
    order = test_helpers.create_Order()
    client = Client()
    url = reverse("purchase_OrderInvoiceLine_create")
    data = {
        "unit_price": 1.0,
        "quantity": 1,
        "product": product.pk,
        "order": order.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_OrderInvoiceLine_detail_view():
    client = Client()
    instance = test_helpers.create_purchase_OrderInvoiceLine()
    url = reverse("purchase_OrderInvoiceLine_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_OrderInvoiceLine_update_view():
    product = test_helpers.create_ProductInstance()
    order = test_helpers.create_Order()
    client = Client()
    instance = test_helpers.create_purchase_OrderInvoiceLine()
    url = reverse("purchase_OrderInvoiceLine_update", args=[instance.pk, ])
    data = {
        "unit_price": 1.0,
        "quantity": 1,
        "product": product.pk,
        "order": order.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Order_list_view():
    instance1 = test_helpers.create_purchase_Order()
    instance2 = test_helpers.create_purchase_Order()
    client = Client()
    url = reverse("purchase_Order_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Order_create_view():
    customer = test_helpers.create_User()
    client = Client()
    url = reverse("purchase_Order_create")
    data = {
        "invoice_date": datetime.now(),
        "date_created": datetime.now(),
        "date_updated": datetime.now(),
        "invoice_file": "aFile",
        "comment": "text",
        "pay_status": "text",
        "value": 1.0,
        "invoice_number": "text",
        "status": "text",
        "customer": customer.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Order_detail_view():
    client = Client()
    instance = test_helpers.create_purchase_Order()
    url = reverse("purchase_Order_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Order_update_view():
    customer = test_helpers.create_User()
    client = Client()
    instance = test_helpers.create_purchase_Order()
    url = reverse("purchase_Order_update", args=[instance.pk, ])
    data = {
        "invoice_date": datetime.now(),
        "date_created": datetime.now(),
        "date_updated": datetime.now(),
        "invoice_file": "aFile",
        "comment": "text",
        "pay_status": "text",
        "value": 1.0,
        "invoice_number": "text",
        "status": "text",
        "customer": customer.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Purchase_list_view():
    instance1 = test_helpers.create_purchase_Purchase()
    instance2 = test_helpers.create_purchase_Purchase()
    client = Client()
    url = reverse("purchase_Purchase_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Purchase_create_view():
    customer = test_helpers.create_User()
    client = Client()
    url = reverse("purchase_Purchase_create")
    data = {
        "comment": "text",
        "invoice_number": "text",
        "invoice_date": datetime.now(),
        "date_created": datetime.now(),
        "date_updated": datetime.now(),
        "customer": customer.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Purchase_detail_view():
    client = Client()
    instance = test_helpers.create_purchase_Purchase()
    url = reverse("purchase_Purchase_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Purchase_update_view():
    customer = test_helpers.create_User()
    client = Client()
    instance = test_helpers.create_purchase_Purchase()
    url = reverse("purchase_Purchase_update", args=[instance.pk, ])
    data = {
        "comment": "text",
        "invoice_number": "text",
        "invoice_date": datetime.now(),
        "date_created": datetime.now(),
        "date_updated": datetime.now(),
        "customer": customer.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302
