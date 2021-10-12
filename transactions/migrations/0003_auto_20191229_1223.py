# Generated by Django 3.0 on 2019-12-29 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_transactiondetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='cash',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='change',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='discount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='grandtotal',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='subtotal',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='tax',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transactiondetail',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]