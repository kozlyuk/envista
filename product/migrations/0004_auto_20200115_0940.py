# Generated by Django 2.2.8 on 2020-01-15 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20200113_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand_image',
            field=models.ImageField(upload_to='brand/', verbose_name='Brand Image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(upload_to='product/', verbose_name='Product image'),
        ),
    ]
