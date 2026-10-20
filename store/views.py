from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product,Order
from django.contrib.auth import authenticate
from django.contrib.auth import logout

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'store/login.html')
def user_logout(request):
    logout(request)
    return redirect('home')
def place_order(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        quantity = int(request.POST.get('quantity', 1))

        Order.objects.create(
            customer_name=customer_name,
            product=product,
            quantity=quantity
        )

        return redirect('home')

    return render(request, 'store/order.html', {'product': product})