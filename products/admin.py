from django.contrib import admin

from .models import Product
from .models import Categories
from .models import Orders
from .models import OrderDetails

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "price", "quantity", "category"]
    class Meta:
        model = Product
        
class CategoriesModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = Categories
        
class OrdersModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "user", "orderTotal"]
    class Meta:
        model = Orders

class OrderDetailsModelAdmin(admin.ModelAdmin):
    list_display = ["id", "order", "product", "quantity", "total"]
    class Meta:
        model = OrderDetails
        
admin.site.register(Product, ProductModelAdmin)
admin.site.register(Categories, CategoriesModelAdmin)
admin.site.register(Orders, OrdersModelAdmin)
admin.site.register(OrderDetails, OrderDetailsModelAdmin)