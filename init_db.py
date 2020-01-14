from product.models import ProductInstance, DiopterPower, Cylinder, Stock, Product
import random
from datetime import date

product = Product.objects.create(title='ИНТРАОКУЛЯРНАЯ ЛИНЗА ENVISTA',
                                 short_description='ИНТРАОКУЛЯРНАЯ ЛИНЗА ENVISTA',
                                 product_image='product/enVista_920x632.png',
                                 brand_name='Bausch&Lomb',
                                 brand_image='brand/BL_logo.png',
                                 date_created=date.today(),
                                 date_updated=date.today(),
                                 created_by_id=1,
                                )

for value in range(125, 576, 75):
    Cylinder.objects.create(value=str(value/100))

for value in range(60, 301, 5):
    DiopterPower.objects.create(value=str(value/10))

for column in Cylinder.objects.all():
    for row in DiopterPower.objects.all():
        pi = ProductInstance.objects.create(product=product, cylinder=column, diopter=row)
        Stock.objects.create(product_instance=pi, quantity_in_hand=random.randint(1,10))
