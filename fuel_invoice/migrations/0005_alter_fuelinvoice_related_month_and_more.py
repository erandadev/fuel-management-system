# Generated by Django 5.1.3 on 2024-12-14 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fuel_invoice', '0004_fuelinvoice_related_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelinvoice',
            name='related_month',
            field=models.IntegerField(default=12),
        ),
        migrations.AlterField(
            model_name='fuelinvoice',
            name='related_year',
            field=models.IntegerField(default=2024),
        ),
    ]