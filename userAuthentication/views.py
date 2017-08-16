from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import products.models
import datetime as D
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, get_object_or_404

from django.core.mail import send_mail


def loginView(request):
    cookie_name = ""
    cart = request.session.get('cart', {})
    
    first_split = ""
    second_split = ""
    product = ""
    
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request,user)
            
            current_user = str(request.user)
            cookie_name = "cart-" + str(current_user)
            
            if request.COOKIES.get(cookie_name):
                productCookie = request.COOKIES[cookie_name]
                #print(productCookie)

                first_split = productCookie.split("-")
                
                for i in range(1,len (first_split)):
                    #print(first_split[i])
                    product = first_split[i]
                    second_split = product.split(",")
                    #print(second_split)

                    product_pk = second_split[0]
                    product_title = second_split[1]
                    product_quantity = second_split[2]

                    productModel = get_object_or_404(products.models.Product, pk=product_pk)

                    #add all_products to cart
                    if productModel.title in cart:
                        cart[productModel.title] = int(product_quantity)
                        #print("Product Added")
                    else:
                        cart[productModel.title] = int(product_quantity)
                        #print("Product Added On ELSE")
                        
                    request.session['cart'] = cart
            
            if 'next' in request.POST:
                return redirect(request.POST['next'])
                
            return render(request, 'userAuthentication/login.html', {'error': 'Login successful'})
        else:
            return render(request, 'userAuthentication/login.html', {'error': 'Username or Password didnt match'})
    else:
        return render(request, 'userAuthentication/login.html')

def logoutView(request):
    cart = request.session.get('cart', {})
    cartDictionary = printCart(cart)
    product       = cartDictionary["product"]
    numberOfItems = cartDictionary["numberOfItems"]
    orderTotal    = cartDictionary["orderTotal"]

    product_Cookie = ""
    cookie_name = ""
    response = HttpResponseRedirect('home')
    
    if request.method == 'POST':
        
        current_user = str(request.user)
        emptyDictionary = {}
        
        if(cart == emptyDictionary and request.user.is_authenticated()):
            print("CART IS EMPTY AND USER LOGGED IN NO NEED TO CREATE COOKIE")
        else:
            product_Cookie = product_Cookie + current_user + "-"
            
            for i in range(0,len (product)):
                product_Cookie = product_Cookie + str(product[i][5]) + "," + product[i][1] + "," + str(product[i][3])
                if (i < (len (product)-1)):
                    product_Cookie = product_Cookie + "-"
                    
            newCookie(product_Cookie, response, "cart", current_user)
        
        logout(request)
        return response



def signupView(request):
    if request.method == 'POST':
        if request.POST['password-signup'] == request.POST['confirm-password']:
            try:
                user = User.objects.get(username=request.POST['username-signup'])
                return render(request, 'userAuthentication/signup.html', {'error': 'Username has already been taken'})
            
            except User.DoesNotExist:
                user = User.objects.create_user(username = request.POST['username-signup'], password = request.POST['password-signup'], first_name = request.POST['first-name-sign'], last_name = request.POST['last-name-sign'], email = request.POST['email-sign'])
                
                login(request, user)
                current_user = str(request.user)
                
                email = request.POST['email-sign']
                subject = 'Registration complete'
                name = request.POST['first-name-sign']
                psw = request.POST['password-signup']
                usname = current_user
                message = 'Dear, ' + name + '\n Thank you very much for registering with Fruit And Veg. '
                message += '\n Your username is ' + usname + ' and your password is ' + psw
                message += '\n Lets make life of farmers better together!'
                message += '\n \n Kind regards, \n Yours Fruit and Veg team'
                from_email = 'freetradefruitandveg@gmail.com'
                send_mail(subject, message, from_email, [email])

                return render(request, 'userAuthentication/signup.html', {'message': 'Registration Successful, \n email confirmation has been sent to ' + email})
        else:
            return render(request, 'userAuthentication/signup.html', {'error': 'Passwords didnt match'})
    else:
        return render(request, 'userAuthentication/signup.html')


def newCookie(value, response, control, current_user):
    
    if (control == "cart"):
        cookie_name = "cart-" + current_user
        
        now = D.datetime.utcnow()
        max_age = 7 * 24 * 60 * 60 # seven days
        exp = now + D.timedelta(seconds=max_age)
        format = "%a, %d-%b-%Y %H:%M:%S GMT"
        exp_str = D.datetime.strftime(exp, format)
        response.set_cookie(cookie_name,value,expires=exp_str)

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