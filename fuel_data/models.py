from django.db import models
from fuel_invoice.models import FuelInvoice

class FuelRecord(models.Model):
    date = models.DateField()
    token_number = models.CharField(max_length=100, unique=True)
    vehicle_number = models.CharField(max_length=100)
    running_chart_number = models.CharField(max_length=100, unique=True)
    liters_pumped = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_type = models.CharField(max_length=10)
    fuel_rate = models.DecimalField(max_digits=10, decimal_places=2)
    profit_per_litre = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    # invoice_number = models.CharField(max_length=100)
    transporter_name = models.CharField(max_length=100)
    invoice_number = models.ForeignKey(FuelInvoice, on_delete=models.CASCADE)
    deducted_running_chart_number = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    is_deducted = models.BooleanField(default=False)  # Added boolean field, default is False

    def __str__(self):
        return f"{self.token_number} - {self.date} - {self.vehicle_number}"
