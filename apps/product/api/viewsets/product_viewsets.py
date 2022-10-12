from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from apps.product.api.serializer.product_serializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = ProductSerializer.Meta.model.objects.all()
    def list(self, request):
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        '''
        data = {
            "total": self.get_queryset().count(),
            "totalNotFiltered": self.get_queryset().count(),
            "rows": product_serializer.data
        }
        '''
        return Response(product_serializer.data, status=status.HTTP_200_OK)

    