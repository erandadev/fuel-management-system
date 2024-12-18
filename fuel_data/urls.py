from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('fuel-records/', views.display_fuel_records, name='fuel_records'),
    # path('filter_fuel_records/', views.filter_fuel_records, name='filter_fuel_records'),
    path('logout/', views.logout_view, name='logout'),
    # path('admin/', views.the_admin, )
    path('change_fuel_records/', views.change_fuel_records, name='change_fuel_records'),
    path('update_status', views.update_status, name="update_status")
]