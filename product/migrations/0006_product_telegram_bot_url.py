# Generated by Django 2.2.8 on 2020-03-03 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_specifications_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='telegram_bot_url',
            field=models.URLField(blank=True, null=True, verbose_name='Telegram bot url'),
        ),
    ]
