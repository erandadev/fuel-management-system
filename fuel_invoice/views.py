from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import FuelInvoice
from .forms import InvoiceForm
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json


def days_between(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


@login_required(login_url='/')
def create_invoice(request):
    """
    View to create a new fuel invoice record.
    """
    if request.method == 'POST' and request.user.has_perm('fuel_invoice.add_fuel_invoice'):
        form = InvoiceForm(request.POST)
        if form.is_valid():
            # Save form data to the FuelInvoice model
            data = form.cleaned_data
            try:
                invoice = FuelInvoice.objects.create(
                    invoice_number=data['invoice_number'],
                    invoice_date=data['invoice_date'],
                    recived_date=data['recived_date'],
                    payment_date=data.get('payment_date'),
                    related_month = data.get('related_month'),
                    related_year = data.get('related_year'),


                    # Quantities
                    petrol_92_quantity=data.get('petrol_92_quantity'),
                    petrol_95_quantity=data.get('petrol_95_quantity'),
                    euro_3_quantity=data.get('euro_3_quantity'),
                    disel_quantity=data.get('disel_quantity'),
                    x_mile_quantity=data.get('x_mile_quantity'),
                    super_disel_quantity=data.get('super_disel_quantity'),

                    # Rates
                    petrol_92_rate=data['petrol_92_rate'],
                    petrol_95_rate=data['petrol_95_rate'],
                    euro_3_rate=data['euro_3_rate'],
                    disel_rate=data['disel_rate'],
                    x_mile_rate=data['x_mile_rate'],
                    super_disel_rate=data['super_disel_rate'],
                )
                messages.success(request, f"Invoice {invoice.invoice_number} created successfully!")
                return redirect('invoice_list')  # Replace with the name of your invoice list view
            except Exception as e:
                print(str(e))
                messages.error(request, f"Error creating invoice: {str(e)}")
    else:
        form = InvoiceForm()
    
    return render(request, 'create_fuel_invoice.html', {'form': form})



@login_required(login_url='/')
def invoice_list(request):
    """
    View to list all fuel invoices.
    """
    invoices = FuelInvoice.objects.all()

    

    updated_invoices = []

    for invoice in invoices:
        tmp_invoice = {
        'invoice_number': "",
        'recived_to_pml': 0,
        'paid_within': 0,
        'invoice_total': 0.0,
        'vat': 0.0,
        'with_vat': 0.0
    }

        total = 0
        recived_to_pml = days_between(str(invoice.recived_date), str(invoice.invoice_date))
        
        paid_within = "Not paid yet"
        if(invoice.payment_date):
            paid_within = days_between(str(invoice.payment_date), str(invoice.recived_date))


        
        if(invoice.petrol_92_quantity):
            total += float(invoice.petrol_92_quantity) * float(invoice.petrol_92_rate)
        
        if(invoice.petrol_95_quantity):
            total += float(invoice.petrol_95_quantity) * float(invoice.petrol_95_rate)

        if(invoice.euro_3_quantity):
            total += float(invoice.euro_3_quantity) * float(invoice.euro_3_rate)
        
        if(invoice.disel_quantity):
            total += float(invoice.disel_quantity) * float(invoice.disel_rate)

        if(invoice.x_mile_quantity):
            total += float(invoice.x_mile_quantity) * float(invoice.x_mile_rate)

        if(invoice.super_disel_quantity):
            total += float(invoice.super_disel_quantity) * float(invoice.super_disel_rate)


        
        without_vat_total = total / 118 * 100
        vat = total - without_vat_total

        tmp_invoice.update({
            'invoice_number': invoice.invoice_number,
            'recived_to_pml': recived_to_pml,
            'paid_within': paid_within,
            'invoice_total': '{:,}'.format(round(without_vat_total, 2)),
            'vat': '{:,}'.format(round(vat, 2)),
            'with_vat': '{:,}'.format(round(total, 2))
        })


        updated_invoices.insert(0, tmp_invoice)

    return render(request, 'view_fuel_invoice.html', {'invoices': updated_invoices})


@login_required(login_url='/')
def invoice_detail(request, invoice_no):
    """
    View to display details of a specific invoice.
    """
    invoice = get_object_or_404(FuelInvoice, invoice_number=invoice_no)

    total = 0
    recived_to_pml = days_between(str(invoice.recived_date), str(invoice.invoice_date))
        
    paid_within = "Not paid yet"
    if(invoice.payment_date):
        paid_within = days_between(str(invoice.payment_date), str(invoice.recived_date))

    
    # VARIABLES
    petrol_92_total = 0.0
    petrol_95_total = 0.0
    euro_3_total = 0.0
    disel_total = 0.0
    x_mile_total = 0.0
    super_disel_total = 0.0



    if(invoice.petrol_92_quantity):
            total += float(invoice.petrol_92_quantity) * float(invoice.petrol_92_rate)
            petrol_92_total = float(invoice.petrol_92_quantity) * float(invoice.petrol_92_rate)
        
    if(invoice.petrol_95_quantity):
        total += float(invoice.petrol_95_quantity) * float(invoice.petrol_95_rate)
        petrol_95_total = float(invoice.petrol_95_quantity) * float(invoice.petrol_95_rate)

    if(invoice.euro_3_quantity):
        total += float(invoice.euro_3_quantity) * float(invoice.euro_3_rate)
        euro_3_total = float(invoice.euro_3_quantity) * float(invoice.euro_3_rate)
        
    if(invoice.disel_quantity):
        total += float(invoice.disel_quantity) * float(invoice.disel_rate)
        disel_total = float(invoice.disel_quantity) * float(invoice.disel_rate)
    

    if(invoice.x_mile_quantity):
        total += float(invoice.x_mile_quantity) * float(invoice.x_mile_rate)
        x_mile_total = float(invoice.x_mile_quantity) * float(invoice.x_mile_rate)

    if(invoice.super_disel_quantity):
        total += float(invoice.super_disel_quantity) * float(invoice.super_disel_rate)
        super_disel_total = float(invoice.super_disel_quantity) * float(invoice.super_disel_rate)

    without_vat_total = total / 118 * 100 
    vat = total - without_vat_total
    

    tmp_invoice = {
        'invoice_number': invoice.invoice_number,
        'recived_to_pml': recived_to_pml,
        'paid_within': paid_within,
        'invoice_total': '{:,}'.format(round(without_vat_total, 2)),
        'vat': '{:,}'.format(round(vat, 2)),
        'with_vat': '{:,}'.format(round(total, 2)),
        'recived_date': invoice.recived_date,
        'payment_date': invoice.payment_date,

        'breakdown': {
            'petrol_92_quantity':invoice.petrol_92_quantity,
            'petrol_95_quantity': invoice.petrol_95_quantity,
            'euro_3_quantity':invoice.euro_3_quantity,
            'disel_quantity': invoice.disel_quantity,
            'x_mile_quantity': invoice.x_mile_quantity,
            'super_disel_quantity': invoice.super_disel_quantity,

            'petrol_92_rate': invoice.petrol_92_rate,
            'petrol_95_rate': invoice.petrol_95_rate,
            'euro_3_rate': invoice.euro_3_rate,
            'disel_rate': invoice.disel_rate,
            'x_mile_rate': invoice.x_mile_rate,
            'super_disel_rate': invoice.super_disel_rate,

            'petrol_92_total': '{:,}'.format(round(petrol_92_total, 2)),
            'petrol_95_total': '{:,}'.format(round(petrol_95_total, 2)),
            'euro_3_total': '{:,}'.format(round(euro_3_total, 2)),
            'disel_total': '{:,}'.format(round(disel_total, 2)),
            'x_mile_total': '{:,}'.format(round(x_mile_total, 2)),
            'super_disel_total': '{:,}'.format(round(super_disel_total, 2)),
        }
    }


    print(invoice.disel_quantity)
    print(disel_total)


    # print(type(tmp_invoice['breakdown']['super_disel_total']))

    return render(request, 'view_fuel_invoice_detail.html', {'invoice': tmp_invoice})


@login_required(login_url='/')
def delete_invoice(request):
    post_data = json.loads(request.body.decode("utf-8"))
    invoice_number = post_data["invoice_number"]
    
    if request.method == 'POST' and request.user.has_perm('fuel_invoice.add_fuel_invoice'):
        invoice = get_object_or_404(FuelInvoice, invoice_number=invoice_number)
        invoice.delete()
        return JsonResponse({'success': True })
    return JsonResponse({'success': False })


@login_required(login_url='/')
def update_invoice_paid_date(request):
    if request.method == "POST" and request.user.has_perm('fuel_invoice.add_fuel_invoice'): 
        post_data = json.loads(request.body.decode("utf-8"))
        invoice_number = post_data["invoice_number"]
        paid_date = post_data["paid_date"]

        obj = FuelInvoice.objects.get(invoice_number=invoice_number)
        obj.payment_date = paid_date
        obj.save()
        
        return JsonResponse({'success': True })
    return JsonResponse({'success': False })