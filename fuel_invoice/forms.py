from django import forms
import datetime

# widget=forms.TextInput(attrs={'placeholder': 'Search'}))


class InvoiceForm(forms.Form):

    months = (
        ("1", "January"),
        ("2", "February"),
        ("3", "March"),
        ("4", "April"),
        ("5", "May"),
        ("6", "June"),
        ("7", "July"),
        ("8", "August"),
        ("9", "September"),
        ("10", "October"),
        ("11", "November"),
        ("12", "December")
    )



    years = (
        ("2024", "2024"),
        ("2025", "2025"),
        ("2026", "2026"),
        ("2027", "2027"),
        ("2028", "2028"),
        ("2029", "2029"),
        ("2035", "2035"),
    )

    invoice_number = forms.CharField(max_length=100, required=True)
    invoice_date = forms.DateField(required=True, widget=forms.DateInput(attrs={'placeholder': "YYYY-MM-DD"}))
    recived_date = forms.DateField(initial=datetime.date.today, required=True, widget=forms.DateInput(attrs={'placeholder': "YYYY-MM-DD"}))
    payment_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'placeholder': "YYYY-MM-DD"}))

    # Quantity
    petrol_92_rate = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'With VAT'}))
    petrol_92_quantity = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
 
    petrol_95_rate = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'With VAT'}))
    petrol_95_quantity = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    euro_3_rate = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'With VAT'}))
    euro_3_quantity = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    disel_rate = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'With VAT'}))
    disel_quantity = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    x_mile_rate = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'With VAT'}))
    x_mile_quantity = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    super_disel_rate = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'placeholder': 'With VAT'}))
    super_disel_quantity = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    related_month = forms.ChoiceField(choices=months, required=True)
    related_year = forms.ChoiceField(choices=years, required=True)