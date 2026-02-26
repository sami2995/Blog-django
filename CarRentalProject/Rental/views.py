from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Customer, Car, Rental


# ============================================
# AUTHENTICATION VIEWS
# ============================================

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard_url')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login_url')


# ============================================
# DASHBOARD VIEW
# ============================================

@login_required
def dashboard(request):
    total_customers = Customer.objects.filter(visible=True).count()
    total_cars = Car.objects.filter(visible=True).count()
    available_cars = Car.objects.filter(visible=True, available=True).count()
    total_rentals = Rental.objects.filter(visible=True).count()
    active_rentals = Rental.objects.filter(visible=True, status='active').count()
    recent_rentals = Rental.objects.filter(visible=True).order_by('-date_created')[:5]
    
    context = {
        'total_customers': total_customers,
        'total_cars': total_cars,
        'available_cars': available_cars,
        'total_rentals': total_rentals,
        'active_rentals': active_rentals,
        'recent_rentals': recent_rentals,
    }
    return render(request, 'dashboard.html', context)


# ============================================
# PUBLIC CAR VIEWS
# ============================================

def car_list(request):
    cars = Car.objects.filter(visible=True, available=True)
    return render(request, 'car_list.html', {'cars': cars})


def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id, visible=True)
    return render(request, 'car_detail.html', {'car': car})


# ============================================
# CUSTOMER ADMIN CRUD
# ============================================

@login_required
def customer_admin(request):
    customers = Customer.objects.filter(visible=True)
    
    if request.method == 'POST':
        # Create new customer
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        license_number = request.POST.get('license_number')
        
        Customer.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            license_number=license_number
        )
        messages.success(request, 'Customer added successfully!')
        return redirect('customer_admin_url')
    
    return render(request, 'customer_admin.html', {'customers': customers})


@login_required
def customer_edit(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        customer.license_number = request.POST.get('license_number')
        customer.save()
        messages.success(request, 'Customer updated successfully!')
        return redirect('customer_admin_url')
    
    return render(request, 'customer_edit.html', {'customer': customer})


@login_required
def customer_delete(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.visible = False
    customer.save()
    messages.success(request, 'Customer deleted successfully!')
    return redirect('customer_admin_url')


# ============================================
# CAR ADMIN CRUD
# ============================================

@login_required
def car_admin(request):
    cars = Car.objects.filter(visible=True)
    
    if request.method == 'POST':
        # Create new car
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        year = request.POST.get('year')
        color = request.POST.get('color')
        plate_number = request.POST.get('plate_number')
        transmission = request.POST.get('transmission')
        daily_rate = request.POST.get('daily_rate')
        image = request.FILES.get('image')
        available = request.POST.get('available') == 'on'
        
        Car.objects.create(
            brand=brand,
            model=model,
            year=year,
            color=color,
            plate_number=plate_number,
            transmission=transmission,
            daily_rate=daily_rate,
            image=image,
            available=available
        )
        messages.success(request, 'Car added successfully!')
        return redirect('car_admin_url')
    
    return render(request, 'car_admin.html', {'cars': cars})


@login_required
def car_edit(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        car.brand = request.POST.get('brand')
        car.model = request.POST.get('model')
        car.year = request.POST.get('year')
        car.color = request.POST.get('color')
        car.plate_number = request.POST.get('plate_number')
        car.transmission = request.POST.get('transmission')
        car.daily_rate = request.POST.get('daily_rate')
        car.available = request.POST.get('available') == 'on'
        
        if request.FILES.get('image'):
            car.image = request.FILES.get('image')
        
        car.save()
        messages.success(request, 'Car updated successfully!')
        return redirect('car_admin_url')
    
    return render(request, 'car_edit.html', {'car': car})


@login_required
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.visible = False
    car.save()
    messages.success(request, 'Car deleted successfully!')
    return redirect('car_admin_url')


# ============================================
# RENTAL ADMIN CRUD
# ============================================

@login_required
def rental_admin(request):
    rentals = Rental.objects.filter(visible=True)
    customers = Customer.objects.filter(visible=True)
    cars = Car.objects.filter(visible=True)
    
    if request.method == 'POST':
        # Create new rental
        customer_id = request.POST.get('customer')
        car_id = request.POST.get('car')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        total_cost = request.POST.get('total_cost')
        status = request.POST.get('status')
        
        customer = get_object_or_404(Customer, id=customer_id)
        car = get_object_or_404(Car, id=car_id)
        
        Rental.objects.create(
            customer=customer,
            car=car,
            start_date=start_date,
            end_date=end_date,
            total_cost=total_cost,
            status=status
        )
        messages.success(request, 'Rental added successfully!')
        return redirect('rental_admin_url')
    
    context = {
        'rentals': rentals,
        'customers': customers,
        'cars': cars,
    }
    return render(request, 'rental_admin.html', context)


@login_required
def rental_edit(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    customers = Customer.objects.filter(visible=True)
    cars = Car.objects.filter(visible=True)
    
    if request.method == 'POST':
        customer_id = request.POST.get('customer')
        car_id = request.POST.get('car')
        
        rental.customer = get_object_or_404(Customer, id=customer_id)
        rental.car = get_object_or_404(Car, id=car_id)
        rental.start_date = request.POST.get('start_date')
        rental.end_date = request.POST.get('end_date')
        rental.total_cost = request.POST.get('total_cost')
        rental.status = request.POST.get('status')
        rental.save()
        messages.success(request, 'Rental updated successfully!')
        return redirect('rental_admin_url')
    
    context = {
        'rental': rental,
        'customers': customers,
        'cars': cars,
    }
    return render(request, 'rental_edit.html', context)


@login_required
def rental_delete(request, rental_id):
    rental = get_object_or_404(Rental, id=rental_id)
    rental.visible = False
    rental.save()
    messages.success(request, 'Rental deleted successfully!')
    return redirect('rental_admin_url')
