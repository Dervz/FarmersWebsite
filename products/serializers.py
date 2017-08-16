from rest_framework import serializers
from products.models import Product, Categories

class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id','title','price','quantity','description','category')

class CategoriesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Categories
        fields = ('id','title')