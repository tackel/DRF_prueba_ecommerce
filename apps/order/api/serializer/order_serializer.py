from rest_framework import serializers
from apps.order.models import Order
from apps.order.models import OrderDetail
from apps.product.models import Product
from apps.product.api.serializer.product_serializer import ProductSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    # para colocar lo que hay en el __str__ del modelo llamado
    #product = serializers.StringRelatedField()
    # para retornar lo que envia el serializador del modelo
    #product = ProductSerializer()
    class Meta():
        model = OrderDetail
        fields = ('cuantity','product')
    
    def to_representation(self, instance):
        #stock = instance.product.stock - instance.cuantity
        return {
            "cuantity":instance.cuantity,
            "product": {
                'Name':instance.product.name,
                'Price': instance.product.price,
                'Stock': instance.product.stock
                }
        }
    
class OrderSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(many=True, read_only=True)
    class Meta():
        model = Order
        fields = ('id','create_date','order')



