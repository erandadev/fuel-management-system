# Generated by Django 5.1.3 on 2024-11-23 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FuelInvoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=100, unique=True)),
                ('invoice_date', models.DateField()),
                ('recived_date', models.DateField()),
                ('payment_date', models.DateField(blank=True, null=True)),
                ('petrol_92_quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('petrol_95_quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('euro_3_quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('disel_quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('x_mile_quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('super_disel_quantity', models.DecimalField(decimal_places=2, max_digits=5)),
                ('petrol_92_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('petrol_95_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('euro_3_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('disel_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('x_mile_rate', models.DecimalField(decimal_places=2, max_digits=5)),
                ('super_disel_rate', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
