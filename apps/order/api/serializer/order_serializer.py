from rest_framework import serializers
from apps.order.models import Order
from apps.order.models import OrderDetail
from apps.product.models import Product
from apps.product.api.serializer.product_serializer import ProductSerializer

class OrderDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)
    class Meta():
        model = OrderDetail
        fields = ('cuantity','product')


class OrderSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(many=True)
    class Meta():
        model = Order
        fields = ('id','create_date','order')

