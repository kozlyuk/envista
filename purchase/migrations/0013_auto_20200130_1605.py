# Generated by Django 2.2.8 on 2020-01-30 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0012_remove_purchase_invoice_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseline',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Quantity'),
        ),
    ]