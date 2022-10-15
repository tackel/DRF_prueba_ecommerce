from rest_framework import serializers
from apps.order.models import Order
from apps.order.models import OrderDetail
from apps.product.models import Product
from apps.product.api.serializer.product_serializer import ProductSerializer


class OrderDetailSerializer(serializers.ModelSerializer):
    # para colocar lo que hay en el __str__ del modelo llamado
    #product = serializers.StringRelatedField()
    # para retornar lo que envia el serializador del modelo
    #product = ProductSerializer(read_only=True, many=False)
    productId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(),source='product')

    class Meta():
        model = OrderDetail
        fields = ('cuantity', 'productId')
    
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

class OrderDetailUpdateSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True, many=False)
    productId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(), source='product')

    class Meta:
        model = OrderDetail
        fields = ('id','cuantity','productoId')
        extra_kwargs = {'id': {'read_only':False}}
    
class OrderSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(many=True)
    #productId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(),source='product')
    class Meta():
        model = Order
        #fields = '__all__'
        fields = ('id','create_date','order')

    def create(self, validated_data):
        #Obtener el contenido de orden_detail
        order_details_data = validated_data.pop('order')
        #Creamos el nuevo registro de la orden
        nueva_orden = Order.objects.create(**validated_data)
        
        #En un ciclo, recorremos el orden_detail y creamos el nuevo registro
        for order_detail in order_details_data:
            OrderDetail.objects.create(**order_detail, order=nueva_orden)       
        return nueva_orden
   
class OrdenesUpdateSerializer(serializers.ModelSerializer):
    order = OrderDetailUpdateSerializer(many=True)
    class Meta:
        model = Order
        fields = ('id','create_date','order')

    def update(self, instance, validated_data):
        # Actualizar datos de orden
        '''
        instance.total = validated_data.get('total', instance.total)
        instance.status = validated_data.get('status', instance.status)
        instance.tipo_pago = validated_data.get('tipo_pago', instance.tipo_pago)
        instance.usuario = validated_data.get('usuario', instance.usuario)
        instance.save()
        '''
        orden_details_data = validated_data.pop('order')
        # Datos de Orden Detalles
        if orden_details_data:
            for orden_detail in orden_details_data:
                orden_detail_id = OrderDetail.get('id',None)
                if orden_detail_id:
                    update_order_detail = OrderDetail.objects.get(id=orden_detail_id)
                    #update_order_detail.productId = orden_detail.get('aplicacion_nutricion_id',update_order_detail.aplicacion_nutricion)
                    #update_order_detail.costo = orden_detail.get('costo',update_order_detail.costo)
                    update_order_detail.save()
                else:
                    #En caso de no existir el id, crear un nuevo registro
                    #Orden_Detalles.objects.create(**orden_detail, orden=instance)
                    pass
        else:
            # posiblemente se eliminarian en caso de existir
            pass
        
        return instance