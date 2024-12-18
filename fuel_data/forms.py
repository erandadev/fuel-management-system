from django import forms
from fuel_invoice.models import FuelInvoice
import datetime

class ExcelUploadForm(forms.Form):
    file = forms.FileField()
    # invoice_number = forms.CharField(max_length=100, required=True)  # Make this required
    invoice_number = forms.ModelChoiceField(required=True, queryset=FuelInvoice.objects.all())


# speed = forms.ModelChoiceField(queryset=Speed.objects.all())