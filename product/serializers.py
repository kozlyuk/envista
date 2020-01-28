from rest_framework import serializers

from product.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "brand_name",
            "brand_image",
            "title",
            "short_description",
            "product_image",
            "specifications_url",
            "footer"
        ]
