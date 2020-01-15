from product.models import ProductInstance, DiopterPower, Cylinder, Product
import random
from datetime import date

product = Product.objects.create(title='ІНТРАОКУЛЯРНА ЛІНЗА ENVISTA',
                                 short_description='ІНТРАОКУЛЯРНАЯ ЛІНЗА ENVISTA',
                                 product_image='product/enVista_920x632.png',
                                 brand_name='Bausch&Lomb',
                                 brand_image='brand/BL_logo.png',
                                 date_created=date.today(),
                                 date_updated=date.today(),
                                 created_by_id=1,
                                 footer="© 2020 ТОВ «Оптдіея». Усі права захищені."
                                )

for value in range(125, 576, 75):
    Cylinder.objects.create(value=str(value/100))

for value in range(60, 301, 5):
    DiopterPower.objects.create(value=str(value/10))

for column in Cylinder.objects.all():
    for row in DiopterPower.objects.all():
        ProductInstance.objects.create(product=product,
                                       cylinder=column,
                                       diopter=row,
                                       quantity_in_hand=random.randint(1,10),
                                       price=random.randint(1000,10000))
