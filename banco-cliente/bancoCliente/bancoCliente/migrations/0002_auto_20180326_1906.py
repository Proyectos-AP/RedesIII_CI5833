# Generated by Django 2.0 on 2018-03-26 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bancoCliente', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuentas',
            name='tdc_number',
            field=models.IntegerField(),
        ),
    ]
