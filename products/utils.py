import json
from . models import *


def cookieCart(request):
    
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
        
    print('Cart: ', cart)
    items = []
    order = {'get_cart_total': 0,
             'get_cart_items': 0}
    cartItems = order['get_cart_items']
    
    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            
            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]
            
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]
            
            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)
        except:
            pass
    
    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        fname = request.user.get_short_name()
        signin_btn_txt = "Hello, {}".format(fname)
        
    else:
        signin_btn_txt = "Hello, Sign-In"
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    
    return {'cartItems': cartItems, 'order': order, 'items': items, 'txt': signin_btn_txt}