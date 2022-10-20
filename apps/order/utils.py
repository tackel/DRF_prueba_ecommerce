

from apps.product.api.serializer.product_serializer import ProductSerializer


def change_stock(order_detail):
        # Descuento el stock de cada producto agregado a la orden  
        product_obj = ProductSerializer.Meta.model.objects.filter(id=order_detail['product'].id).first()
        product_obj.stock = (order_detail['product'].stock - order_detail['cuantity'])
        product_obj.save()