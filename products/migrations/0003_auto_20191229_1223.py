# Generated by Django 3.0 on 2019-12-29 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20191225_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price_profit',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_purchase',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='price_sales',
            field=models.FloatField(default=0),
        ),
    ]
