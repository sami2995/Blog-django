from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Customer, Car, Rental


def user_login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_url')
        else:
            error_message = 'Invalid username or password'
    return render(request, 'login.html', {'error_message': error_message})


def user_logout(request):
    logout(request)
    return redirect('login_url')


@login_required(login_url='login_url')
def dashboard(request):
    total_customers = Customer.objects.filter(visible=True).count()
    total_cars = Car.objects.filter(visible=True).count()
    available_cars = Car.objects.filter(visible=True, available=True).count()
    active_rentals = Rental.objects.filter(visible=True, status='Active').count()
    recent_rentals = Rental.objects.filter(visible=True).order_by('-date_created')[:5]
    return render(request, 'dashboard.html', {
        'total_customers': total_customers,
        'total_cars': total_cars,
        'available_cars': available_cars,
        'active_rentals': active_rentals,
        'recent_rentals': recent_rentals
    })


def car_list(request):
    cars = Car.objects.filter(visible=True, available=True)
    return render(request, 'car_list.html', {'cars': cars})


def car_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'car_detail.html', {'car': car})


@login_required(login_url='login_url')
def customer_admin(request):
    customers = Customer.objects.filter(visible=True)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        license_number = request.POST.get('license_number')
        obj = Customer()
        obj.name = name
        obj.email = email
        obj.phone = phone
        obj.address = address
        obj.license_number = license_number
        obj.save()
    return render(request, 'customer_admin.html', {'customers': customers})


@login_required(login_url='login_url')
def customer_edit(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        customer.license_number = request.POST.get('license_number')
        customer.save()
        return redirect('customer_admin_url')
    return render(request, 'customer_edit.html', {'customer': customer})


@login_required(login_url='login_url')
def customer_delete(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.visible = False
    customer.save()
    return redirect('customer_admin_url')


@login_required(login_url='login_url')
def car_admin(request):
    cars = Car.objects.filter(visible=True)
    if request.method == 'POST':
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year')
        color = request.POST.get('color')
        plate_number = request.POST.get('plate_number')
        transmission = request.POST.get('transmission')
        daily_rate = request.POST.get('daily_rate')
        image = request.FILES.get('image')
        obj = Car()
        obj.brand = brand
        obj.model = model
        obj.year = year
        obj.color = color
        obj.plate_number = plate_number
        obj.transmission = transmission
        obj.daily_rate = daily_rate
        obj.image = image
        obj.save()
    return render(request, 'car_admin.html', {'cars': cars})


@login_required(login_url='login_url')
def car_edit(request, car_id):
    car = Car.objects.get(id=car_id)
    if request.method == 'POST':
        car.brand = request.POST.get('brand')
        car.model = request.POST.get('model')
        car.year = request.POST.get('year')
        car.color = request.POST.get('color')
        car.plate_number = request.POST.get('plate_number')
        car.transmission = request.POST.get('transmission')
        car.daily_rate = request.POST.get('daily_rate')
        image = request.FILES.get('image')
        car.image = image if image != None else car.image
        car.available = request.POST.get('available') == 'on'
        car.save()
        return redirect('car_admin_url')
    return render(request, 'car_edit.html', {'car': car})


@login_required(login_url='login_url')
def car_delete(request, car_id):
    car = Car.objects.get(id=car_id)
    car.visible = False
    car.save()
    return redirect('car_admin_url')


@login_required(login_url='login_url')
def rental_admin(request):
    rentals = Rental.objects.filter(visible=True)
    customers = Customer.objects.filter(visible=True)
    cars = Car.objects.filter(visible=True, available=True)
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        car_id = request.POST.get('car')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_cost = request.POST.get('total_cost')
        obj = Rental()
        obj.customer = Customer.objects.get(id=customer_id)
        obj.car = Car.objects.get(id=car_id)
        obj.start_date = start_date
        obj.end_date = end_date
        obj.total_cost = total_cost
        obj.save()
        car = Car.objects.get(id=car_id)
        car.available = False
        car.save()
    return render(request, 'rental_admin.html', {
        'rentals': rentals,
        'customers': customers,
        'cars': cars
    })


@login_required(login_url='login_url')
def rental_edit(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    customers = Customer.objects.filter(visible=True)
    cars = Car.objects.filter(visible=True)
    if request.method == 'POST':
        rental.customer = Customer.objects.get(id=request.POST.get('customer'))
        old_car_id = rental.car.id
        new_car_id = int(request.POST.get('car'))
        rental.car = Car.objects.get(id=new_car_id)
        rental.start_date = request.POST.get('start_date')
        rental.end_date = request.POST.get('end_date')
        rental.total_cost = request.POST.get('total_cost')
        rental.status = request.POST.get('status')
        rental.save()
        if rental.status == 'Completed' or rental.status == 'Cancelled':
            car = Car.objects.get(id=new_car_id)
            car.available = True
            car.save()
        if old_car_id != new_car_id:
            old_car = Car.objects.get(id=old_car_id)
            old_car.available = True
            old_car.save()
        return redirect('rental_admin_url')
    return render(request, 'rental_edit.html', {
        'rental': rental,
        'customers': customers,
        'cars': cars
    })


@login_required(login_url='login_url')
def rental_delete(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    rental.visible = False
    rental.save()
    car = rental.car
    car.available = True
    car.save()
    return redirect('rental_admin_url')
