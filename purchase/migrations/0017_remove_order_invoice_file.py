# Generated by Django 2.2.10 on 2020-04-27 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0016_auto_20200225_0953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='invoice_file',
        ),
    ]
