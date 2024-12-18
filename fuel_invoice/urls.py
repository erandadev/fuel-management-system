from django.urls import path
from . import views

urlpatterns = [
    path('create_fuel_invoice/', views.create_invoice, name='create_fuel_invoice'),
    path('view_fuel_invoice/', views.invoice_list, name='invoice_list'),
    path('view_fuel_invoice/<invoice_no>', views.invoice_detail, name='invoice_detail'),
    path('delete_invoice/', views.delete_invoice, name='delete_invoice'),
    path('update_invoice_paid_date/', views.update_invoice_paid_date, name='update_invoice_paid_date')   
]

