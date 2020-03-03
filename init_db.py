""" Create initial database """
from accounts.models import User
from product.models import ProductInstance, DiopterPower, Cylinder, Product
from purchase.models import Purchase, PurchaseLine

# Cteare superuser
User.objects.create_superuser('sergey.kozlyuk@gmail.com', 'password')


# Create initial db for product app
PRODUCT = Product.objects.create(title='ENVISTA® TORIC',
                                 short_description="The Clear Choice for Exceptional Astigmatism Management. Exacting astigmatism correction. Dependable stability. Pristine visual clarity. It all comes together in the proven enVista platform to deliver:"
                                 "- Aberration-free, glistening-free performance"
                                 "- Proven rotational stability"
                                 "- Exceptional outcomes"
                                 "- Delivered through an incision size as small as 2.2mm to limit potential SIA",
                                 product_image='product/enVista_920x632.png',
                                 brand_name='Bausch&Lomb',
                                 brand_image='brand/BL_logo.png',
                                 telegram_bot_url='https://t.me/envista_bot',
                                 footer="© 2020 ТОВ «Оптдіея». Усі права захищені."
                                 )
print("Initial Product created")

for value in range(125, 576, 75):
    Cylinder.objects.create(value=str(value/100))
print("Initial Cylinders created")

for value in range(60, 301, 5):
    DiopterPower.objects.create(value=str(value/10))
print("Initial Diopters created")

# Create initial db for purchase app

PRICES = [3000, 3850, 5600, 7300, 7300, 7300, 7300]

QUANTITIES = [[1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [3, 3, 3, 2, 2, 2, 2],
              [2, 2, 2, 2, 2, 2, 2],
              [2, 2, 2, 2, 2, 2, 2],
              [2, 2, 2, 2, 2, 2, 2],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1]
              ]

for column in Cylinder.objects.all():
    invoice_number = 'Initial purchase {}'.format(column.value)
    PURCHASE = Purchase.objects.create(invoice_number=invoice_number, created_by_id=1)
    for row in DiopterPower.objects.all():
        pi = ProductInstance.objects.create(product=PRODUCT,
                                            cylinder=column,
                                            diopter=row,
                                            quantity_in_hand=QUANTITIES[row.pk-1][column.pk-1],
                                            price=PRICES[column.pk-1])
        PurchaseLine.objects.create(product=pi,
                                    purchase=PURCHASE,
                                    cylinder=column,
                                    diopter=row,
                                    quantity=QUANTITIES[row.pk-1][column.pk-1])
print("Initial Purchases created")


# Create users permissions
def create_permission(group, model, permission):
    from django.contrib.auth.models import Group, Permission
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

create_permission('Клієнти', 'Product', 'view')
create_permission('Клієнти', 'Product Instance', 'view')
create_permission('Клієнти', 'Cylinder', 'view')
create_permission('Клієнти', 'Diopter Power', 'view')
create_permission('Клієнти', 'Order', 'view')
create_permission('Клієнти', 'Order', 'add')
create_permission('Клієнти', 'Order', 'change')
create_permission('Клієнти', 'order line', 'view')
create_permission('Клієнти', 'order line', 'add')
create_permission('Клієнти', 'order line', 'change')
create_permission('Клієнти', 'order line', 'delete')
