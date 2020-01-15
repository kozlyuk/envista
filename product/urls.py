from django.urls import path, include
from rest_framework import routers

from . import api


router = routers.DefaultRouter()
router.register("ProductInstance", api.ProductInstanceViewSet)
router.register("Cylinder", api.CylinderViewSet)
router.register("Product", api.ProductViewSet)
router.register("DiopterPower", api.DiopterPowerViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
)
