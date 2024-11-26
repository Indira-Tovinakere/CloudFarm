from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import UserRegistration, UserLogin
from .models import Fertilizer


def register(request):
    if request.method == 'POST':
        number = request.POST['number']
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if UserRegistration.objects.filter(number=number).exists():
            messages.error(request, "This number is already registered!")
            return redirect('register')

        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered!")
            return redirect('register')

        user = UserRegistration(number=number, email=email, name=name, password=password)
        user.save()
        messages.success(request, "Registration successful!")
        return redirect('login')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        number = request.POST['number']
        password = request.POST['password']

        try:
            user = UserRegistration.objects.get(number=number, password=password)
            messages.success(request, f"Welcome back, {user.name}!")
            return redirect('dashboard')  # Redirect to the dashboard or homepage
        except UserRegistration.DoesNotExist:
            messages.error(request, "Invalid login credentials!")
            return redirect('login')
    return render(request, 'login.html')

# ML INTEGRATION

from django.shortcuts import render
from .ml_utils import predict_crop_and_fertilizer

def prediction(request):
    result = {}
    if request.method == "POST":
        n = float(request.POST.get("nitrogen"))
        p = float(request.POST.get("phosphorus"))
        k = float(request.POST.get("potassium"))
        rainfall = float(request.POST.get("rainfall"))
        ph = float(request.POST.get("ph"))

        result = predict_crop_and_fertilizer(n, p, k, rainfall, ph)


        result = predict_crop_and_fertilizer(n, p, k, rainfall, ph)

    return render(request, "prediction.html", {"result": result})

def fertilizer_list(request):
    fertilizers = Fertilizer.objects.all()
    return render(request, 'fertilizer_list.html', {'fertilizers': fertilizers})

def fertilizer_detail(request, pk):
    fertilizer = get_object_or_404(Fertilizer, pk=pk)
    return render(request, 'fertilizer_detail.html', {'fertilizer': fertilizer})

from django.shortcuts import render

# Home view
def home(request):
    return render(request, 'home.html')

# Fertilizer list page view
def fertilizer_list(request):
    return render(request, 'fertilizer_list.html')

# About Us page view
def about_us(request):
    return render(request, 'Aboutus.html')

from django.shortcuts import redirect
from django.contrib.auth import logout

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login.html')  # Redirects to the login page

from django.shortcuts import render

def buy_products(request):
    return render(request, 'buy_products.html')


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# View to display the cart
def view_cart(request):
    # Get the cart from the session, or set it to an empty list if not found
    cart_items = request.session.get('cart', [])
    
    return render(request, 'view_cart.html', {'cart_items': cart_items})

def add_to_cart(request, product_id):
    # Retrieve cart from session, or initialize an empty list if not found
    cart = request.session.get('cart', [])
    
    # Add product ID to the cart (ensure no duplicates)
    if product_id not in cart:
        cart.append(product_id)
    
    # Save the cart back to the session
    request.session['cart'] = cart
    request.session.modified = True  # Mark session as modified
    
    return redirect('view_cart')  # Redirect to the cart view after adding

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    request.session['cart'] = cart
    return redirect('view_cart')

