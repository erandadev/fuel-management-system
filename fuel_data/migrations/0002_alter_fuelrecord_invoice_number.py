# Generated by Django 5.1.3 on 2024-11-23 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_data', '0001_initial'),
        ('fuel_invoice', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelrecord',
            name='invoice_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fuel_invoice.fuelinvoice'),
        ),
    ]
