

from apps.product.api.serializer.product_serializer import ProductSerializer


def change_stock(order_detail, key, previus_cuat, previus_product):
        if key == 'create_new_order':
                # Descuento el stock de cada producto agregado a la orden  
                product_obj = ProductSerializer.Meta.model.objects.filter(id=order_detail['product'].id).first()
                product_obj.stock = (order_detail['product'].stock - order_detail['cuantity'])
                product_obj.save()
        if key == 'update_order':
                product_obj = ProductSerializer.Meta.model.objects.filter(id=order_detail.product.id, state=True).first()
                if previus_product == product_obj:
                        stock_a_descontar = previus_cuat - order_detail.cuantity
                        product_obj.stock += stock_a_descontar
                        product_obj.save()
                       
                else:

                        product_obj.stock = (product_obj.stock - order_detail.cuantity)
                        product_obj.save()


                