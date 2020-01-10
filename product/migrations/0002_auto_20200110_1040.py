# Generated by Django 2.2.8 on 2020-01-10 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='long_description',
        ),
        migrations.AddField(
            model_name='product',
            name='footer',
            field=models.TextField(blank=True, verbose_name='Site footer'),
        ),
        migrations.AlterField(
            model_name='product',
            name='brand_image',
            field=models.ImageField(default='Bausch@Lomb', upload_to='brands/', verbose_name='Brand Image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='short_description',
            field=models.TextField(verbose_name='Short description'),
        ),
    ]
