# Generated by Django 2.2.8 on 2020-01-13 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0003_auto_20200111_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinvoiceline',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.Order', verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='purchaseinvoiceline',
            name='purchase',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.Purchase', verbose_name='Purchase'),
        ),
    ]
