from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from product.serializers import ProductSerializer
from product.models import Product


class ProductDetailsView(RetrieveAPIView):
    """
    Returns Product fields.
    """
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return Product.objects.first()
