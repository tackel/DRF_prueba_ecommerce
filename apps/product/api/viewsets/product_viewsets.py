from rest_framework import viewsets

from apps.product.api.serializer.product_serializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects
    