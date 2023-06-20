from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import json
from .utils import cookieCart, cartData


def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    signin_btn_txt = data['txt']
    
    products = Product.objects.all()
    return render(request, 'products/index.html', {'products': products, 'cartItems': cartItems, 'signin_btn_txt': signin_btn_txt})

def cart(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    signin_btn_txt = data['txt']
    
    context= {
        'items':items, 
        'order': order,
        'cartItems': cartItems,
        'signin_btn_txt': signin_btn_txt}
    return render(request, 'products/cart.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print('productId: ', productId)
    print('action: ', action)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse("Item was added", safe=False)

def checkout(request):
    return render(request, 'products/checkout.html')


# def new(request):
#     return HttpResponse('New Product')