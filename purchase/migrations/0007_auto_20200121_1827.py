# Generated by Django 2.2.8 on 2020-01-21 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0006_auto_20200121_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='last_quantity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='purchaseline',
            name='last_quantity',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='purchaseline',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Quantity'),
        ),
    ]
