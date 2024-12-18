import os
import json
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import FuelRecord
from fuel_invoice.models import FuelInvoice
from .forms import ExcelUploadForm
from datetime import datetime
import math
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='/')
def upload_file(request):
    if request.method == 'POST' and request.FILES.get('file') and request.user.has_perm('fuel_invoice.add_fuel_invoice'):
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get invoice number
            invoice_number = form.cleaned_data['invoice_number']

            if not invoice_number:
                return HttpResponse("Invoice number cannot be empty!", status=400)

            has_previous_data = FuelRecord.objects.filter(invoice_number=invoice_number).exists()

            if has_previous_data:
                return HttpResponse(f"You have already uploaded breakdown for Invoice No: {invoice_number}", status=400)
            
            # Read the uploaded file
            file = request.FILES['file']

            try:
                # Read the Excel file into a DataFrame
                df = pd.read_excel(file, header=None, skiprows=1, dtype = {
                    0: 'str',
                    1: 'str',
                    2: 'str',
                    3: 'str',
                    4: 'str',
                    5: 'float',
                    6: 'str',
                    7: 'float',
                    8: 'float'
                })

                # Process the data
                records_to_insert = []
                seen_token_numbers = set()
                seen_running_chart_numbers = set()

                for index, row in df.iterrows():
                    # Stop processing at the first blank cell in column A
                    if pd.isna(row[0]):
                        break

                    date = pd.to_datetime(row[0], format='%d/%m/%Y').date()
                    token_number = str(row[1]).strip()
                    transporter_name = str(row[2]).strip()
                    vehicle_number = str(row[3]).strip()
                    running_chart_number = str(row[4]).strip()
                    liters_pumped = float(row[5])
                    fuel_type = str(row[6]).strip()
                    fuel_rate = float(row[7])
                    profit_per_litre = float(row[8])

                    # Check for duplicate token numbers or running chart numbers
                    if token_number in seen_token_numbers:
                        return HttpResponse(
                            f"Duplicate token number detected: {token_number}.", status=400
                        )
                    if running_chart_number in seen_running_chart_numbers:
                        return HttpResponse(
                            f"Duplicate running chart number detected: {running_chart_number}.", status=400
                        )

                    seen_token_numbers.add(token_number)
                    seen_running_chart_numbers.add(running_chart_number)

                    # Prepare the record for bulk insertion
                    records_to_insert.append(FuelRecord(
                        date=date,
                        token_number=token_number,
                        transporter_name = transporter_name,
                        vehicle_number=vehicle_number,
                        running_chart_number=running_chart_number,
                        liters_pumped=liters_pumped,
                        fuel_type=fuel_type,
                        fuel_rate=fuel_rate,
                        profit_per_litre = profit_per_litre,
                        invoice_number=invoice_number,  # Store the invoice number
                        deducted_running_chart_number=None,  # Initially empty
                        is_deducted=False  # Default value
                    ))

                # Bulk insert records into the database
                FuelRecord.objects.bulk_create(records_to_insert)

                return HttpResponse("Data successfully processed and stored in the database.")
            except Exception as e:
                return HttpResponse(f"An error occurred: {e}", status=500)
    else:
        form = ExcelUploadForm()

    return render(request, 'upload.html', {'form': form})



@login_required(login_url='/')
def display_fuel_records(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    is_filter = False
    
    
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        if post_data["year"] and post_data["month"]:
            current_year = post_data["year"]
            current_month = post_data["month"]
            is_filter = True

    fuel_invoices = FuelInvoice.objects.filter(related_month=current_month, related_year=current_year)
    
    output = {}
    summary = []
    meta_data = {}
    

    for fuel_invoice in fuel_invoices:
        fuel_records = FuelRecord.objects.filter(invoice_number = fuel_invoice)

        if(fuel_records):
            tmp_fuel_record = {
            'date': "",
            'vehicle_number': "",
            'fuel_type': "",
            'liters_pumped': "",
            'fuel_rate': "",
            'total': '',
            'profit_per_litre': '',
            'with_profit_total': '',
            'is_deducted': '',
            'deducted_chart': ''
        }
            
            final_total = 0
            total_profit = 0
            total_litres = 0
            deducted_total = 0


            summary = []
            for fuel_record_row in fuel_records:
                total = 0
                with_profit_total = 0

                total = float(fuel_record_row.fuel_rate) * float(fuel_record_row.liters_pumped)
                with_profit_total = (float(fuel_record_row.liters_pumped) * float(fuel_record_row.profit_per_litre))

                if fuel_record_row.is_deducted: 
                    print(fuel_record_row.is_deducted)
                    deducted_total += total

                tmp_fuel_record = {
                'date': fuel_record_row.date,
                'vehicle_number': fuel_record_row.vehicle_number,
                'fuel_type': fuel_record_row.fuel_type,
                'liters_pumped': fuel_record_row.liters_pumped,
                'fuel_rate': fuel_record_row.fuel_rate,
                'total': '{:,}'.format(round(total, 2)),
                'profit_per_litre': fuel_record_row.profit_per_litre,
                'with_profit_total': '{:,}'.format(round(with_profit_total, 2)),
                'is_deducted': fuel_record_row.is_deducted,
                'deducted_chart': fuel_record_row.deducted_running_chart_number
            } 

                final_total += total
                total_profit += with_profit_total
                total_litres += float(fuel_record_row.liters_pumped)

                summary.append(tmp_fuel_record)  

            deducted_precentage = deducted_total / (final_total + total_profit) * 100
            meta_data[fuel_invoice.invoice_number] = {
                'final_total': '{:,}'.format(round(final_total, 2)),
                'total_profit': '{:,}'.format(round(total_profit, 2)),
                'total_litres': '{:,}'.format(round(total_litres, 2)),
                'deducted_precentage': '{:,}'.format(math.trunc(deducted_precentage)),
            }
            output[fuel_invoice.invoice_number] = summary
            

    if is_filter: return JsonResponse({'breakdowns': output, 'meta_data': meta_data })
    return render(request, 'dashboard.html', {'breakdowns': output, 'meta_data': meta_data })
    


# @login_required(login_url='/')
# def filter_fuel_records(request):
#     post_data = json.loads(request.body.decode("utf-8"))
    
#     if request.method == 'POST' and post_data["year"] and post_data["month"]:
#         current_year = post_data["year"]
#         current_month = post_data["month"]
   
#         fuel_invoices = FuelInvoice.objects.filter(related_month=current_month, related_year=current_year)
        
        
#         output = {}
#         summary = []
#         meta_data = {}
        

#         for fuel_invoice in fuel_invoices:
#             fuel_records = FuelRecord.objects.filter(invoice_number = fuel_invoice)

#             if(fuel_records):
#                 tmp_fuel_record = {
#                 'date': "",
#                 'vehicle_number': "",
#                 'fuel_type': "",
#                 'liters_pumped': "",
#                 'fuel_rate': "",
#                 'total': '',
#                 'profit_per_litre': '',
#                 'with_profit_total': '',
#                 'is_deducted': '',
#             }
                
#                 final_total = 0
#                 total_profit = 0
#                 total_litres = 0
#                 deducted_total = 0

#                 summary = []
#                 for fuel_record_row in fuel_records:
#                     total = 0
#                     with_profit_total = 0

#                     total = float(fuel_record_row.fuel_rate) * float(fuel_record_row.liters_pumped)
#                     with_profit_total = (float(fuel_record_row.liters_pumped) * float(fuel_record_row.profit_per_litre))

#                     if fuel_record_row.is_deducted: deducted_total += total


#                     if fuel_record_row.is_deducted: 
#                         print(fuel_record_row.is_deducted)
#                         deducted_total += total

#                     tmp_fuel_record = {
#                     'date': fuel_record_row.date,
#                     'vehicle_number': fuel_record_row.vehicle_number,
#                     'fuel_type': fuel_record_row.fuel_type,
#                     'liters_pumped': fuel_record_row.liters_pumped,
#                     'fuel_rate': fuel_record_row.fuel_rate,
#                     'total': '{:,}'.format(round(total, 2)),
#                     'profit_per_litre': fuel_record_row.profit_per_litre,
#                     'with_profit_total': '{:,}'.format(round(with_profit_total, 2)),
#                     'is_deducted': fuel_record_row.is_deducted,
#                 } 

#                     final_total += total
#                     total_profit += with_profit_total
#                     total_litres += float(fuel_record_row.liters_pumped)

                    

#                     summary.append(tmp_fuel_record)  
                

#                 deducted_precentage = deducted_total / final_total * 100
#                 output[fuel_invoice.invoice_number] = summary
#                 meta_data[fuel_invoice.invoice_number] = {
#                     'final_total': '{:,}'.format(round(final_total, 2)),
#                     'total_profit': '{:,}'.format(round(total_profit, 2)),
#                     'total_litres': '{:,}'.format(round(total_litres, 2)),
#                     'deducted_precentage': '{:,}'.format(math.trunc(deducted_precentage))
#                 }
            
#         return JsonResponse({'breakdowns': output, 'meta_data': meta_data })


@login_required(login_url='/')
def change_fuel_records(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    is_filter = False
    
    
    if request.method == 'POST':
        post_data = json.loads(request.body.decode("utf-8"))
        if post_data["year"] and post_data["month"]:
            current_year = post_data["year"]
            current_month = post_data["month"]
            is_filter = True

    fuel_invoices = FuelInvoice.objects.filter(related_month=current_month, related_year=current_year)
    
    output = []
    meta_data = {}
    
    final_total = 0
    final_with_profit_total = 0
    total_litres = 0
    final_deducted_total = 0

    for fuel_invoice in fuel_invoices:
        fuel_records = FuelRecord.objects.filter(invoice_number = fuel_invoice)

        if(fuel_records):
        #     tmp_fuel_record = {
        #     'date': "",
        #     'transporter_name': "",
        #     'vehicle_number': "",
        #     'liters_pumped': "",
        #     'fuel_rate': "",
        #     'total': '',
        #     'profit_per_litre': "",
        #     'Total deduction': "",
        #     'is_deducted': '',
        # }   
            
            for fuel_record_row in fuel_records:
                total = 0
                with_profit_total = 0
                deducted_total = 0

                total = float(fuel_record_row.fuel_rate) * float(fuel_record_row.liters_pumped)
                with_profit_total = total + (float(fuel_record_row.liters_pumped) * float(fuel_record_row.profit_per_litre))

                if fuel_record_row.is_deducted: 
                    deducted_total += with_profit_total

                tmp_fuel_record = {
                # 'date': fuel_record_row.date,
                'id': fuel_record_row.pk,
                'token_number': fuel_record_row.token_number,
                'running_chart': fuel_record_row.running_chart_number,
                'transporter_name': fuel_record_row.transporter_name,
                'vehicle_number': fuel_record_row.vehicle_number,
                'liters_pumped': fuel_record_row.liters_pumped,
                'fuel_rate': fuel_record_row.fuel_rate,
                'total': '{:,}'.format(round(total, 2)),
                'profit_per_litre': fuel_record_row.profit_per_litre,
                'total_deduction': '{:,}'.format(round(with_profit_total, 2)),
                'is_deducted': fuel_record_row.is_deducted,

            } 

                final_total += total
                final_with_profit_total += with_profit_total
                total_litres += fuel_record_row.liters_pumped
                final_deducted_total += deducted_total

                output.append(tmp_fuel_record)  

    if not final_deducted_total: deducted_precentage = 0
    else: deducted_precentage = final_deducted_total / final_with_profit_total * 100

    meta_data = {
        'final_total': '{:,}'.format(round(final_total, 2)),
        'final_with_profit_total': '{:,}'.format(round(final_with_profit_total, 2)),
        'total_litres': '{:,}'.format(round(total_litres, 2)),
        'deducted_total': '{:,}'.format(round(final_deducted_total, 2)),
        'deducted_precentage': '{:,}'.format(math.trunc(deducted_precentage))
    }
            # output[.invoice_number] = summary
            

    if is_filter: return JsonResponse({'breakdowns': output, 'meta_data': meta_data })
    return render(request, 'admin_pannel.html', {'breakdowns': output, 'meta_data': meta_data })



def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    
    return redirect('login')



def update_status(request):
    if request.method == "POST" and request.user.has_perm('fuel_invoice.add_fuel_invoice'): 
        post_data = json.loads(request.body.decode("utf-8"))
        id = post_data["id"]
        deducted_running_chart = post_data["deducted_running_chart"]

        print(id)
        print(deducted_running_chart)

        obj = FuelRecord.objects.get(id=id)

        if(obj.is_deducted):
            obj.is_deducted = False
            obj.deducted_running_chart_number = ""
        else:
            obj.is_deducted = True
            obj.deducted_running_chart_number = deducted_running_chart

        obj.save()
        
        return JsonResponse({'success': True })
    return JsonResponse({'success': False })