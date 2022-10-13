from rest_framework import serializers
from apps.product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta():
        model = Product
        exclude = ('state',)
        #fields = '__all__'
    
class ChangeStockProduct(serializers.ModelSerializer):
    class Meta():
        model = Product
        fields = ('stock',)
    

class ProductRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ('state',)
    

