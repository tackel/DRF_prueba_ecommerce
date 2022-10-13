from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from apps.product.api.serializer.product_serializer import ProductSerializer, ChangeStockProduct, ProductRetrieveSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    #queryset = ProductSerializer.Meta.model.objects.all()

    def get_queryset(self, pk=None):
        if pk is None:
            return self.get_serializer().Meta.model.objects.filter(state=True)
        return self.get_serializer().Meta.model.objects.filter(id=pk, state=True).first()

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

    def create(self, request):
        product_serializer = self.serializer_class(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()    
            return Response({'Message':f"Product {product_serializer.data['name']} created"}, status=status.HTTP_201_CREATED )
        return Response({'Message':'','Error':product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST )

    def update(self, request, pk=None):
        product_serializer = self.serializer_class(self.get_queryset(pk), request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response({'Message':f"Product {product_serializer.data['name']} updated successfully!"}, status=status.HTTP_200_OK)
        return Response({'Message':'', 'Error':product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            print(product)
            product.state = False
            product.save()
            return Response({'Message':f'Product {product} was removed!'}, status=status.HTTP_200_OK)
        return Response({'Error':'The product does not exist!'}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product_serializer = ProductRetrieveSerializer(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        return Response({'Error':'The product does not exist!'}, status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['put'], detail=True)
    def change_stock(self, request, pk=None):
        product = self.get_queryset(pk)
        if product:
            product_serializer = ChangeStockProduct(self.get_queryset(pk),request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response({'Message':f"Stock of Product {product} updated "}, status=status.HTTP_200_OK)
            return Response({'Message':'', 'Error':product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        '''
        product = self.get_queryset(pk)
        if product:
            print(product)
            print(request.data)
            stock_serializer = ChangeStockProduct(data= request.data)
            print(stock_serializer)
            if stock_serializer.is_valid():
                stock_serializer.save()
        '''
        return Response({'Message':'', 'Error':'The product does not exist!'}, status=status.HTTP_400_BAD_REQUEST)


