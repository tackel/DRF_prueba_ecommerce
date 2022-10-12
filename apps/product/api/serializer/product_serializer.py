from rest_framework import serializers
from apps.product.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta():
        model = Product
        exclude = ('state',)
        #fields = '__all__'