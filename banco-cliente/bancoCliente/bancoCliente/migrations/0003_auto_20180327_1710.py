# Generated by Django 2.0 on 2018-03-27 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bancoCliente', '0002_auto_20180326_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentas',
            name='tdc_number',
            field=models.IntegerField(unique=True),
        ),
    ]