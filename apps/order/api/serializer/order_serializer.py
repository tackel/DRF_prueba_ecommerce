from rest_framework import serializers

from apps.order.models import Order
from apps.order.models import OrderDetail
from apps.product.models import Product
from apps.product.api.serializer.product_serializer import ProductSerializer

from apps.order.utils import change_stock

class OrderDetailSerializer(serializers.ModelSerializer):

    # para colocar lo que hay en el __str__ del modelo llamado
    #product = serializers.StringRelatedField()
    # para retornar lo que envia el serializador del modelo
    #product = ProductSerializer(read_only=True, many=False)
    productId = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Product.objects.all(),source='product')

    class Meta():
        model = OrderDetail
        fields = ('cuantity', 'productId')

    def validate_productId(self, value):
        if value.stock <= 0:
            raise serializers.ValidationError({"Error": "Stock of product is 0"})
        return value
    
    def validate(self, data):
        if data['product'].stock - data['cuantity'] >= 0:
            #product_obj = ProductSerializer.Meta.model.objects.filter(id=data['product'].id).first() # consigo la instancia
            #product_obj.stock = (data['product'].stock - data['cuantity'])
            #product_obj.save()
            return data
        raise serializers.ValidationError({"Error": f"Insufficient stock of {data['product']} for this order"})
    
    def to_representation(self, instance):
        #stock = instance.product.stock - instance.cuantity
        return {
            "id": instance.id,
            "cuantity":instance.cuantity,
            "product": {
                'id': instance.product.id,
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
        fields = ('id','cuantity','product','productId')
        extra_kwargs = {'id': {'read_only':False}}

    def to_representation(self, instance):
        #stock = instance.product.stock - instance.cuantity
        return {
            "id": instance.id,
            "cuantity":instance.cuantity,
            "product": {
                'id': instance.product.id,
                'Name':instance.product.name,
                'Price': instance.product.price,
                'Stock': instance.product.stock
                }
        }
    
class OrderSerializer(serializers.ModelSerializer):
    order = OrderDetailSerializer(many=True)
    class Meta():
        model = Order
        fields = ('id','create_date','order')

    def discount_stock(self, order_detail):
        # Descuento el stock de cada producto agregado a la orden  
        product_obj = ProductSerializer.Meta.model.objects.filter(id=order_detail['product'].id).first()
        product_obj.stock = (order_detail['product'].stock - order_detail['cuantity'])
        product_obj.save()

    def create(self, validated_data):
        #Obtener el contenido de order_detail
        order_details_data = validated_data.pop('order')
        #Creamos el nuevo registro de la orden
        nueva_orden = Order.objects.create(**validated_data)
        
        #En un ciclo, recorremos el orden_detail y creamos el nuevo registro
        for order_detail in order_details_data:            
            OrderDetail.objects.create(**order_detail, order=nueva_orden) 
            change_stock(order_detail)
        return nueva_orden
   
class OrderUpdateSerializer(serializers.ModelSerializer):
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
        # Datos de Order Detail
        if orden_details_data:
            for order_detail in orden_details_data:
                order_detail_id = order_detail.get('id', None)
                if order_detail_id:
                    try:
                        update_order_detail = OrderDetail.objects.get(id=order_detail_id)
                    except:
                        raise serializers.ValidationError({
                                "Error": "id order detail is not in Order selected"
                            })
                    if update_order_detail.order.id == instance.id:
                        update_order_detail.product = order_detail.get('product')
                        update_order_detail.cuantity = order_detail.get('cuantity')
                        update_order_detail.save()

                    else:
                        raise serializers.ValidationError({
                                "Error": "id order detail is not in Order selected"
                            })
                      
                else:
                    raise serializers.ValidationError({
                                "Error": "Id of order detail not exist"
                            })
                    #En caso de no existir el id, crear un nuevo registro
                    #Orden_Detalles.objects.create(**orden_detail, orden=instance)
                
        else:
            raise serializers.ValidationError({
                                "Error": "Order detail data not exist"
                            })
        
        return instance
