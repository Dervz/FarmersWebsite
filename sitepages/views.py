from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
import products.models

from django.shortcuts import render, get_object_or_404

def home(request):
    return render(request, 'sitepages/index.html')


def view_basket(request):
    cart = request.session.get('cart', {})
    
    if request.method == 'POST':

        addSubmit      = request.POST.get("Add", False)
        minusSubmit    = request.POST.get("Minus", False)
        deleteSubmit   = request.POST.get("Delete", False)
        add_single_product = request.POST.get("add_single_product", False)
        selectedProduct  = request.POST.get("SelectedProduct", False)
        productModel     = get_object_or_404(products.models.Product, pk=selectedProduct)

        if addSubmit == "+":
            #add to cart
            if productModel.title in cart:
                cart[productModel.title] += 1
            else:
                cart[productModel.title] = 1
                
            request.session['cart'] = cart
            
            #print cart
            cartDictionary = printCart(cart)
            product       = cartDictionary["product"]
            numberOfItems = cartDictionary["numberOfItems"]
            orderTotal    = cartDictionary["orderTotal"]
            #print(cartDictionary["orderTotal"])
            
            return render(request, 'sitepages/basket.html', {'product':product, 'numberOfItems':numberOfItems, 'orderTotal':orderTotal, 'message': 'Add Button Pressed'} )
        elif minusSubmit == "-":
            
            if productModel.title in cart:
                if cart[productModel.title] <= 0:
                    del(cart[productModel.title])
                else:
                    cart[productModel.title] -= 1
                    if cart[productModel.title] <= 0:
                        del(cart[productModel.title])
            else:
                cart[productModel.title] = 1
                
            request.session['cart'] = cart
            
            #print cart
            
            cartDictionary = printCart(cart)
            product       = cartDictionary["product"]
            numberOfItems = cartDictionary["numberOfItems"]
            orderTotal    = cartDictionary["orderTotal"]
            #print(cartDictionary["orderTotal"])
            
            return render(request, 'sitepages/basket.html', {'product':product, 'numberOfItems':numberOfItems, 'orderTotal':orderTotal, 'message': 'Minus Button Pressed'} )
        elif deleteSubmit == "x" :
            
            if productModel.title in cart:
                del(cart[productModel.title])
                
            request.session['cart'] = cart
            
            #print cart
            
            cartDictionary = printCart(cart)
            product       = cartDictionary["product"]
            numberOfItems = cartDictionary["numberOfItems"]
            orderTotal    = cartDictionary["orderTotal"]
            #print(cartDictionary["orderTotal"])

            return render(request, 'sitepages/basket.html', {'product':product, 'numberOfItems':numberOfItems, 'orderTotal':orderTotal, 'message': 'Delete Button Pressed'} )
        elif add_single_product == "Add Recipe":
            #add to cart
            if productModel.title in cart:
                cart[productModel.title] += 1
            else:
                cart[productModel.title] = 1
                
            request.session['cart'] = cart
            
            #print cart
            cartDictionary = printCart(cart)
            product       = cartDictionary["product"]
            numberOfItems = cartDictionary["numberOfItems"]
            orderTotal    = cartDictionary["orderTotal"]
            #print(cartDictionary["orderTotal"])
            
            return render(request, 'sitepages/basket.html', {'product':product, 'numberOfItems':numberOfItems, 'orderTotal':orderTotal, 'message': 'Add Button Pressed'} )
    else:
        cartDictionary = printCart(cart)
        product       = cartDictionary["product"]
        numberOfItems = cartDictionary["numberOfItems"]
        orderTotal    = cartDictionary["orderTotal"]
        #print(cartDictionary["orderTotal"])
        return render(request, 'sitepages/basket.html', {'product':product, 'numberOfItems':numberOfItems, 'orderTotal':orderTotal} )

def printCart(cart):

    products_dictionary = products.models.Product.objects.order_by('id')
    
    title_dictionary = {}
    price_dictionary = {}
    quantity_dictionary = {}
    
    count = 0
    
    product = []
    orderTotal = 0
    numberOfItems = 0
    
    for i in range(0,len (products_dictionary)):
        title  = products_dictionary.values('title')[i].get('title')
        price  = products_dictionary.values('price')[i].get('price')
        image  = products_dictionary.values('image')[i].get('image')
        id_rec = products_dictionary.values('id')[i].get('id')
        
        for cart_title, cart_quantity in cart.items():
            if title == cart_title:
                
                try:
                    subtotal = int(cart_quantity) * price
                except ValueError:
                    #Try float.
                    subtotal = float(cart_quantity)* price
                
                orderTotal = orderTotal + subtotal
                
                product.append([image, title,str(price), cart_quantity,subtotal,id_rec])
                numberOfItems = numberOfItems + cart_quantity
                
                count = count + 1
    
    #print(product)
    cartDictionary = {"product": product, "numberOfItems":numberOfItems, "orderTotal":orderTotal}
    #print(cartDictionary["orderTotal"])
    return cartDictionary

def thank_you(request):
    cart = request.session.get('cart', {})
    
    cartDictionary = printCart(cart)
    product       = cartDictionary["product"]
    numberOfItems = cartDictionary["numberOfItems"]
    orderTotal    = cartDictionary["orderTotal"]
    
    response = HttpResponseRedirect('thank_you')
    
    usernamed = str(request.user)
    cookie_name = "cart-" + usernamed
    
    if request.method == 'POST':
        #email for checkout confirmation
        try:
            u = User.objects.get(username=usernamed)
            
            subject = 'Order Confirmation'
            
            message = 'Dear ' + usernamed + ',\n \n'
            message += 'Your order is complete and items are going to be dispatched soon. \n \n'
            message += 'Please see your order details below: \n'

            for p in product:
                message += str(p[1]) + ', ' + str(p[3]) + ' (' + str(p[2]) + '$)'  + '\n'

            message += ' Total amount paid: ' + str(orderTotal) + '$ \n \n'

            message += 'Kind regards, \n Free Trade Fruit And Veg Team'
            from_email = 'freetradefruitandveg@gmail.com'
            
            User.email_user(u, subject, message, from_email)

        except User.DoesNotExist:
            print("USER DOES NOT EXIST")
        
        #empting the cart
        cart = {}
        request.session['cart'] = cart
        
        if (request.COOKIES.get(cookie_name) is not None):
            #delete cookie
            response.delete_cookie(cookie_name)
            return response
        else:
            print("THERES NO COOKIE")
        
        return render(request, 'sitepages/thankyou.html', {"product": product, "numberOfItems":numberOfItems, "orderTotal":orderTotal, "message": "Please Find your recipt at your email."})
    else:   
        return render(request, 'sitepages/thankyou.html', {"message_reload": "Please Find your recipt at your email."})