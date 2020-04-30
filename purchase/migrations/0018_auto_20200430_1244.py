# Generated by Django 2.2.10 on 2020-04-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0017_remove_order_invoice_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='order_type',
            field=models.CharField(choices=[('AO', 'Order'), ('PO', 'Pre-order')], default='AO', max_length=2, verbose_name='Order type'),
        ),
        migrations.AlterField(
            model_name='order',
            name='old_status',
            field=models.CharField(choices=[('IC', 'Products in cart'), ('NO', 'New order'), ('CN', 'Order canceled'), ('CF', 'Order confirmed'), ('PO', 'Pre-order'), ('RT', 'Order returned')], default='NO', max_length=2),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('IC', 'Products in cart'), ('NO', 'New order'), ('CN', 'Order canceled'), ('CF', 'Order confirmed'), ('PO', 'Pre-order'), ('RT', 'Order returned')], default='IC', max_length=2, verbose_name='Order status'),
        ),
    ]