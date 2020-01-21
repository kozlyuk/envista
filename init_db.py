import random

from django.contrib.auth.models import Group, Permission
from product.models import ProductInstance, DiopterPower, Cylinder, Product


PRODUCT = Product.objects.create(title='ІНТРАОКУЛЯРНА ЛІНЗА ENVISTA® TORIC',
                                 short_description="The Clear Choice for Exceptional Astigmatism Management. Exacting astigmatism correction. Dependable stability. Pristine visual clarity. It all comes together in the proven enVista platform to deliver:"
                                 "- Aberration-free, glistening-free performance"
                                 "- Proven rotational stability"
                                 "- Exceptional outcomes"
                                 "- Delivered through an incision size as small as 2.2mm to limit potential SIA",
                                 product_image='product/enVista_920x632.png',
                                 brand_name='Bausch&Lomb',
                                 brand_image='brand/BL_logo.png',
                                 footer="© 2020 ТОВ «Оптдіея». Усі права захищені."
                                )

for value in range(125, 576, 75):
    Cylinder.objects.create(value=str(value/100))

for value in range(60, 301, 5):
    DiopterPower.objects.create(value=str(value/10))

PRICES = [3000, 3850, 5600, 7300, 7300, 7300, 7300]
PRICES_INDEX = 0

for column in Cylinder.objects.all():
    for row in DiopterPower.objects.all():
        ProductInstance.objects.create(product=PRODUCT,
                                       cylinder=column,
                                       diopter=row,
                                       quantity_in_hand=random.randint(1, 10),
                                       price=PRICES[PRICES_INDEX])
    prices_index += 1


def create_permission(group, model, permission):
    new_group, created = Group.objects.get_or_create(name=group)
    name = 'Can {} {}'.format(permission, model)
    try:
        model_add_perm = Permission.objects.get(name=name)
    except Permission.DoesNotExist:
        return print("Permission not found with name '{}'.".format(name))
    new_group.permissions.add(model_add_perm)
    return print("Added permission with name '{}'.".format(name))

create_permission('Менеджери', 'user', 'view')
create_permission('Менеджери', 'user', 'add')
create_permission('Менеджери', 'user', 'change')
create_permission('Менеджери', 'log entry', 'view')
create_permission('Менеджери', 'Cylinder', 'view')
create_permission('Менеджери', 'Diopter Power', 'view')
create_permission('Менеджери', 'Product', 'view')
create_permission('Менеджери', 'Product', 'change')
create_permission('Менеджери', 'Product Instance', 'view')
create_permission('Менеджери', 'Product Instance', 'change')
create_permission('Менеджери', 'Order', 'view')
create_permission('Менеджери', 'Order', 'add')
create_permission('Менеджери', 'Order', 'change')
create_permission('Менеджери', 'Order', 'delete')
create_permission('Менеджери', 'order line', 'view')
create_permission('Менеджери', 'order line', 'add')
create_permission('Менеджери', 'order line', 'change')
create_permission('Менеджери', 'order line', 'delete')
create_permission('Менеджери', 'Purchase', 'view')
create_permission('Менеджери', 'Purchase', 'add')
create_permission('Менеджери', 'Purchase', 'change')
create_permission('Менеджери', 'Purchase', 'delete')
create_permission('Менеджери', 'purchase line', 'view')
create_permission('Менеджери', 'purchase line', 'add')
create_permission('Менеджери', 'purchase line', 'change')
create_permission('Менеджери', 'purchase line', 'delete')

create_permission('Клієнт', 'Order', 'view')
create_permission('Клієнт', 'Order', 'add')
create_permission('Клієнт', 'Order', 'change')
create_permission('Клієнт', 'order line', 'view')
create_permission('Клієнт', 'order line', 'add')
create_permission('Клієнт', 'order line', 'change')
create_permission('Клієнт', 'order line', 'delete')
