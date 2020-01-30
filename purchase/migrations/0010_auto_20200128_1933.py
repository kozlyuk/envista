# Generated by Django 2.2.8 on 2020-01-28 17:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0009_auto_20200123_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Customer'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='old_status',
            field=models.CharField(choices=[('IC', 'Products in cart'), ('NO', 'New order'), ('CN', 'Order canceled'), ('CF', 'Order confirmed'), ('RT', 'Order returned')], default='NO', max_length=2),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('IC', 'Products in cart'), ('NO', 'New order'), ('CN', 'Order canceled'), ('CF', 'Order confirmed'), ('RT', 'Order returned')], default='IC', max_length=2, verbose_name='Order status'),
        ),
    ]
