from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


from apps.order.api.serializer.order_serializer import OrderSerializer
from apps.order.api.serializer.order_detail_serializer import OrderDetailSerializer


class OrderViewSets(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = OrderSerializer.Meta.model.objects.all()
    def create(self, request):
        order_serializer = self.serializer_class(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response({'Message':'Order created'}, status=status.HTTP_201_CREATED) 
        return Response({
                'Errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailViewSets(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetailSerializer.Meta.model.objects.all()


