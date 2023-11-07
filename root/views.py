from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout
from django.contrib.auth.models import User
from django import forms
from .models import *
from .urls import  *
from django.contrib.auth.decorators import login_required



class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


def store(request):
	products=Product.objects.all()
	context={'products':products}
	return render(request,'root/store.html',context)
	
def cart(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
	else:
		items=[]
		order={'get_cart_total':0,'get_cart_items':0}
	context={'items':items,'order':order}
	return render(request,'root/cart.html',context)
	
@login_required(login_url='login')  # Make sure the user is authenticated to access the checkout page
def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    items = order.orderitem_set.all()
    context = {'items': items, 'order': order}

    if request.method == 'POST':
        # Get user info
        name = request.POST.get('name')
        email = request.POST.get('email')

        # Get shipping info
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # Create or update the shipping address
        shipping_address, created = ShippingAddress.objects.get_or_create(customer=customer, order=order)
        shipping_address.address = address
        shipping_address.city = city
        shipping_address.state = state
        shipping_address.zipcode = zipcode
        shipping_address.save()

        # Update user info (you might want to do more validation here)
        customer.name = name
        customer.email = email
        customer.save()

        # Mark the order as complete
        order.complete = True
        order.save()

        # You can add more logic here, like redirecting to a payment page

        return render(request,'root/success.html',context)

    
    return render(request, 'root/checkout.html', context)
def search(request):
    search_query = request.GET.get('query')
    

    if search_query is None or search_query.strip() == '':
        error_message = 'Please enter a valid search query.'
        return render(request, 'root/error.html', {'error_message': error_message})

    # Get all categories to populate the dropdown in the search form
    
    # Filter products based on search query and category
    product_results = Product.objects.filter(name__istartswith=search_query)

    
    context = {
        'product_results': product_results,
        'search_query': search_query,
        
    }

    return render(request, 'root/search.html', context)
    
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    print(f"{product.id}")
    
    if request.user.is_authenticated:
        # If authenticated, associate the order with the customer
        order, created = Order.objects.get_or_create(customer=request.user.customer, complete=False)
    else:
        # If not authenticated, create a temporary order for the guest user
        order, created = Order.objects.get_or_create(complete=False)
    
    # Check if the product is already in the cart
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    order_item.quantity += 1
    order_item.save()
    total = order.get_cart_total
    total_items=order.get_cart_items

    # Add a message to inform the user about the added item
    #messages.success(request, f'{product.name} was added to your cart.')

    # Redirect to the store or cart page, depending on your preference
    return redirect('cart')
    
def view(request,product_id):
	product=Product.objects.get(id=product_id)
	#print(f"product:{product}")
	return render(request,'root/view.html',{'products':product})   
	

def login_view(request):
    page='login'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        print(f"Username: {username}, Password: {password}, User: {user}")

        if user is not None and user.is_authenticated:
            auth_login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Username or Password invalid')

    context = {'page':page}
    return render(request, 'root/login.html', context)
    
    
def registerUser(request):

    form = SignUpForm  # Corrected this line
    

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # Check if passwords match
            if password == confirm_password:
                # Create the user
                user = User.objects.create_user(username=username, password=password)

                # Log in the user
                login(request, user)

                # Redirect to the store page or any other page you want
                return redirect('store')
            else:
                messages.error(request, 'Passwords do not match')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'root/login.html', {'form': form})


def custom_logout(request):
	logout(request)
	return redirect('store')
	
def increment_quantity(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    order_item.quantity += 1
    order_item.save()
    return redirect('cart')

def decrement_quantity(request, order_item_id):
    order_item = OrderItem.objects.get(id=order_item_id)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
    return redirect('cart')
 # Create your views here.
