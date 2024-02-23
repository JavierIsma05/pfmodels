from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import login,authenticate
import json
import datetime
from .models import * 
from .forms import * 
from .utils import cookieCart, cartData, guestOrder
from .forms import CustomUserCreationForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)

def dashboard(request):
	data = {
		'form': ProductForm()
	}
	if request.method == 'POST':
		formulario = ProductForm(data=request.POST,files=request.FILES)
		if formulario.is_valid():
			formulario.save()
		else:
			data["form"] = formulario	
	return render(request,'store/dashboard.html',data)

def contact(request):
    return render(request,'store/contact.html')

def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/carrito.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Pago enviado..', safe=False)

from django.shortcuts import render, get_object_or_404

# funcion para ver el prodcuto en solitario
def ver_producto(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/ver_producto.html', {'product': product})


from .forms import CategoryForm
#lista de productos
def product_list(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            category = Category.objects.get(name=category_name)
            products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    form = CategoryForm()
    context = {
        'products': products,
        'form': form,
        'categories': categories
    }
    return render(request, 'store/product_list.html', context)


from django.views.generic import View
#Registrarse como usuario
def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            #redirigir al home
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            login(request,user)
            return redirect(to="store")
        data["form"] = formulario
    return render(request,'registration/register.html',data)
