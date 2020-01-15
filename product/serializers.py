from rest_framework import serializers

from . import models


class ProductInstanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ProductInstance
        fields = [
            "product",
            "cylinder",
            "diopter",
            "price",
            "quantity_in_hand",
        ]

class CylinderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Cylinder
        fields = [
            "value",
        ]

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Product
        fields = [
            "date_created",
            "date_updated",
            "brand_name",
            "brand_image",
            "short_description",
            "long_description",
            "product_image",
            "title",
        ]

class DiopterPowerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DiopterPower
        fields = [
            "value",
        ]
