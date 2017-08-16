from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

import sitepages.views
import products.views
import userAuthentication.views

router = routers.DefaultRouter()
router.register(r'api/products', products.views.ProductsViewSet)
router.register(r'api/categories', products.views.CategoriesViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    url(r'^home', sitepages.views.home, name="home"),
    url(r'^basket', sitepages.views.view_basket, name="basket"),
    url(r'^thank_you', sitepages.views.thank_you, name="thank_you"),
    
    url(r'^products', products.views.productPage, name="products_main"),
    url(r'^all_products', products.views.all_products, name="all_products"),
    url(r'^fruits', products.views.all_fruits, name="fruits"),
    url(r'^vegetables', products.views.all_vegetables, name="vegetables"),
    
    url(r'^accounts/login/', userAuthentication.views.loginView, name="login"),
    url(r'^logout', userAuthentication.views.logoutView, name="log_out"),
    url(r'^signup', userAuthentication.views.signupView, name="signup"),
    
    url(r'^', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
