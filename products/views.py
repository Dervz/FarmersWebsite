import products.models
from products.models import Product, Categories
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductsSerializer, CategoriesSerializer
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.decorators import login_required

@login_required
def productPage(request):
    cart = request.session.get('cart', {})
    message = {}
    if request.method == 'POST':
        selectedProduct  = request.POST.get("SelectedProduct", False)
        productModel     = get_object_or_404(products.models.Product, pk=selectedProduct)
        
        #add all_products to car
        if productModel.title in cart:
            cart[productModel.title] += 1
            message = "Product Added"
        else:
            cart[productModel.title] = 1
            message = "Product Added"

        request.session['cart'] = cart
    #print("IM IN")
    #print(cart)
    
    return render(request, 'products/products.html', {'message': message })

def all_products(request):
    products_dictionary = products.models.Product.objects.order_by('id')
    
    product  = ''
    
    for i in range(0,len (products_dictionary)):
        product  += printProducts(products_dictionary,i)
    
    return render(request, 'products/products.html', { 'products_array':products_dictionary, 'product':product})


def printProducts(products_dictionary,i):   
    productprint = ''

    ids           = products_dictionary.values('id')
    titles        = products_dictionary.values('title')
    prices        = products_dictionary.values('price')
    quantitys     = products_dictionary.values('quantity')
    descriptions  = products_dictionary.values('description')
    images        = products_dictionary.values('image')
    
    id_value          = ids[i].get('id')
    title_value       = titles[i].get('title')
    price_value       = prices[i].get('price')
    quantity_value    = quantitys[i].get('quantity')
    description_value = descriptions[i].get('description')
    image_value       = images[i].get('image')
    
    #product_URL = ("recipes/{id_value}/".format(id_value=id_value))
    #product_URL_add_to_cart = ("add_to_cart/{id_value}/".format(id_value=id_value))
    #print (product_URL)
    
    productprint = '''
                <div class="col-lg-3 col-md-6 text-center">
                    <div class="service-box">
                        <a href="#"><img class="recipe-img" src="media/{image_value}" alt=""></a>
                        <h3>{title_value}</h3>
                        
                        <ul>
                            <li><i class="ion-ios-cart-outline icon-small"></i>{quantity_value} in stock</li>
                            <li><i class="ion-cash"></i>&#36;{price_value}</li>
                        </ul>
                        
                        <div>
                            <input type="submit" value="Add to Basket" name="Add" id="{id_value}" onClick="reply_click(this.id)">
                        </div>
                    </div>
                </div>
                
        '''.format(image_value=image_value, title_value=title_value, quantity_value=quantity_value, price_value=price_value, id_value=id_value)

    return productprint


def all_vegetables(request):
    products_dictionary = products.models.Product.objects.order_by('id')
    product  = ''
    
    products_category_model         = products_dictionary.values('category')
    product_category_id_vegetarian  = products_category_model[2].get('category')
    
    for i in range(0,len (products_dictionary)):
        if(products_dictionary.values('category')[i].get('category') == product_category_id_vegetarian):
            product  += printProducts(products_dictionary,i)
             
    return render(request, 'products/products.html', { 'products_array':products_dictionary, 'product':product})

def all_fruits(request):
    products_dictionary = products.models.Product.objects.order_by('id')
    product  = ''
    
    products_category_model         = products_dictionary.values('category')
    product_category_id_fruits  = products_category_model[1].get('category')
    
    for i in range(0,len (products_dictionary)):
        if(products_dictionary.values('category')[i].get('category') == product_category_id_fruits):
            product  += printProducts(products_dictionary,i)
             
    return render(request, 'products/products.html', { 'products_array':products_dictionary, 'product':product})


# model ViewSet that organizes urls that  
class ProductsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductsSerializer

class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all().order_by('id')
    serializer_class = CategoriesSerializer
