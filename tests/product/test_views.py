import pytest
import test_helpers

from django.urls import reverse
from django.test import Client


pytestmark = [pytest.mark.django_db]


def tests_ProductInstance_list_view():
    instance1 = test_helpers.create_product_ProductInstance()
    instance2 = test_helpers.create_product_ProductInstance()
    client = Client()
    url = reverse("product_ProductInstance_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_ProductInstance_create_view():
    diopter = test_helpers.create_DiopterPower()
    cylinder = test_helpers.create_Cylinder()
    product = test_helpers.create_Product()
    client = Client()
    url = reverse("product_ProductInstance_create")
    data = {
        "date_updated": datetime.now(),
        "date_created": datetime.now(),
        "price": 1.0,
        "diopter": diopter.pk,
        "cylinder": cylinder.pk,
        "product": product.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_ProductInstance_detail_view():
    client = Client()
    instance = test_helpers.create_product_ProductInstance()
    url = reverse("product_ProductInstance_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_ProductInstance_update_view():
    diopter = test_helpers.create_DiopterPower()
    cylinder = test_helpers.create_Cylinder()
    product = test_helpers.create_Product()
    client = Client()
    instance = test_helpers.create_product_ProductInstance()
    url = reverse("product_ProductInstance_update", args=[instance.pk, ])
    data = {
        "date_updated": datetime.now(),
        "date_created": datetime.now(),
        "price": 1.0,
        "diopter": diopter.pk,
        "cylinder": cylinder.pk,
        "product": product.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Stock_list_view():
    instance1 = test_helpers.create_product_Stock()
    instance2 = test_helpers.create_product_Stock()
    client = Client()
    url = reverse("product_Stock_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Stock_create_view():
    product_instance = test_helpers.create_ProductInstance()
    client = Client()
    url = reverse("product_Stock_create")
    data = {
        "quantity_in_hand": 1,
        "product_instance": product_instance.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Stock_detail_view():
    client = Client()
    instance = test_helpers.create_product_Stock()
    url = reverse("product_Stock_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Stock_update_view():
    product_instance = test_helpers.create_ProductInstance()
    client = Client()
    instance = test_helpers.create_product_Stock()
    url = reverse("product_Stock_update", args=[instance.pk, ])
    data = {
        "quantity_in_hand": 1,
        "product_instance": product_instance.pk,
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Cylinder_list_view():
    instance1 = test_helpers.create_product_Cylinder()
    instance2 = test_helpers.create_product_Cylinder()
    client = Client()
    url = reverse("product_Cylinder_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Cylinder_create_view():
    client = Client()
    url = reverse("product_Cylinder_create")
    data = {
        "value": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Cylinder_detail_view():
    client = Client()
    instance = test_helpers.create_product_Cylinder()
    url = reverse("product_Cylinder_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Cylinder_update_view():
    client = Client()
    instance = test_helpers.create_product_Cylinder()
    url = reverse("product_Cylinder_update", args=[instance.pk, ])
    data = {
        "value": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Product_list_view():
    instance1 = test_helpers.create_product_Product()
    instance2 = test_helpers.create_product_Product()
    client = Client()
    url = reverse("product_Product_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_Product_create_view():
    client = Client()
    url = reverse("product_Product_create")
    data = {
        "date_created": datetime.now(),
        "date_updated": datetime.now(),
        "brand_name": "text",
        "brand_image": "anImage",
        "short_description": "text",
        "long_description": "text",
        "product_image": "anImage",
        "title": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_Product_detail_view():
    client = Client()
    instance = test_helpers.create_product_Product()
    url = reverse("product_Product_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_Product_update_view():
    client = Client()
    instance = test_helpers.create_product_Product()
    url = reverse("product_Product_update", args=[instance.pk, ])
    data = {
        "date_created": datetime.now(),
        "date_updated": datetime.now(),
        "brand_name": "text",
        "brand_image": "anImage",
        "short_description": "text",
        "long_description": "text",
        "product_image": "anImage",
        "title": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_DiopterPower_list_view():
    instance1 = test_helpers.create_product_DiopterPower()
    instance2 = test_helpers.create_product_DiopterPower()
    client = Client()
    url = reverse("product_DiopterPower_list")
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance1) in response.content.decode("utf-8")
    assert str(instance2) in response.content.decode("utf-8")


def tests_DiopterPower_create_view():
    client = Client()
    url = reverse("product_DiopterPower_create")
    data = {
        "value": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302


def tests_DiopterPower_detail_view():
    client = Client()
    instance = test_helpers.create_product_DiopterPower()
    url = reverse("product_DiopterPower_detail", args=[instance.pk, ])
    response = client.get(url)
    assert response.status_code == 200
    assert str(instance) in response.content.decode("utf-8")


def tests_DiopterPower_update_view():
    client = Client()
    instance = test_helpers.create_product_DiopterPower()
    url = reverse("product_DiopterPower_update", args=[instance.pk, ])
    data = {
        "value": "text",
    }
    response = client.post(url, data)
    assert response.status_code == 302
