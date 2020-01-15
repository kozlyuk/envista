# Generated by Django 2.2.8 on 2020-01-15 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20200115_0940'),
        ('purchase', '0004_auto_20200113_2059'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderline',
            unique_together={('order', 'product')},
        ),
        migrations.AlterUniqueTogether(
            name='purchaseline',
            unique_together={('purchase', 'product')},
        ),
    ]