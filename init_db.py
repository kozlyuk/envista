from product.models import ProductInstance, DiopterPower, Cylinder, Product
import random
from datetime import date

product = Product.objects.create(title='ІНТРАОКУЛЯРНА ЛІНЗА ENVISTA® TORIC',
                                 short_description="""The Clear Choice for Exceptional Astigmatism Management.
                                                      Exacting astigmatism correction. Dependable stability. Pristine visual clarity. It all comes together in the proven enVista platform to deliver:
                                                      Aberration-free, glistening-free performance.
                                                      Proven rotational stability.
                                                      Exceptional outcomes.
                                                      Delivered through an incision size as small as 2.2mm to limit potential SIA.""",
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

prices = [3000, 3850, 5600, 7300, 7300, 7300, 7300]
prices_index = 0

for column in Cylinder.objects.all():
    for row in DiopterPower.objects.all():
        ProductInstance.objects.create(product=product,
                                       cylinder=column,
                                       diopter=row,
                                       quantity_in_hand=random.randint(1,10),
                                       price=prices[prices_index])
    prices_index += 1
