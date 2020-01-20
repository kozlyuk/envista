# Generated by Django 2.2.8 on 2020-01-19 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='customer',
        ),
        migrations.AddField(
            model_name='purchase',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='Value'),
        ),
    ]
