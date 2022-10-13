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
    
    def validate_stock(self, value):
        if value == '' or value == None:
            raise serializers.ValidationError("Need input stock value.")
        return value

    def validate(self, data):
        if 'stock' not in data.keys():
            raise serializers.ValidationError({
                "measure_unit": "Stock field is required."
            })
        
        return data

    def to_representation(self, instance):
        return {
            "name":instance.name,
            "stock": instance.stock
        }
    

class ProductRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ('state',)
    

