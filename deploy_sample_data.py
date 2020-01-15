from product.models import ProductInstance, DiopterPower, Cylinder, Stock, Product
import random

product = Product.objects.get(id=1)
for column in Cylinder.objects.all():
    for row in DiopterPower.objects.all():
        pi = ProductInstance.objects.create(product=product, cylinder=column, diopter=row)
        Stock.objects.create(product_instance=pi, quantity_in_hand=random.randint(1,10))