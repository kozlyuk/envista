# Generated by Django 2.2.8 on 2020-01-25 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20200121_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='specifications_url',
            field=models.URLField(blank=True, null=True, verbose_name='Specification'),
        ),
    ]
