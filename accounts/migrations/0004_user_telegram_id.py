# Generated by Django 2.2.8 on 2020-02-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200128_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]