from django.contrib import admin
from .models import Customer, Car, Rental


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'license_number', 'date_registered', 'visible']
    list_filter = ['visible', 'date_registered']
    search_fields = ['name', 'email', 'phone', 'license_number']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'plate_number', 'daily_rate', 'available', 'visible']
    list_filter = ['available', 'visible', 'transmission', 'brand']
    search_fields = ['brand', 'model', 'plate_number']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['customer', 'car', 'start_date', 'end_date', 'total_cost', 'status', 'visible']
    list_filter = ['status', 'visible', 'start_date']
    search_fields = ['customer__name', 'car__brand', 'car__model']
