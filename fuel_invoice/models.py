from django.db import models

# Create your models here.
class FuelInvoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True)
    invoice_date = models.DateField()
    recived_date = models.DateField()
    payment_date = models.DateField(blank=True, null=True)
    related_month = models.IntegerField(default=12)
    related_year = models.IntegerField(default=2024)

    # Quantity
    petrol_92_quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    petrol_95_quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) 
    euro_3_quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    disel_quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    x_mile_quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    super_disel_quantity = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)


    # RATE
    petrol_92_rate = models.DecimalField(max_digits=5, decimal_places=2)
    petrol_95_rate = models.DecimalField(max_digits=5, decimal_places=2) 
    euro_3_rate = models.DecimalField(max_digits=5, decimal_places=2)
    disel_rate = models.DecimalField(max_digits=5, decimal_places=2)
    x_mile_rate = models.DecimalField(max_digits=5, decimal_places=2)
    super_disel_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.invoice_number}"