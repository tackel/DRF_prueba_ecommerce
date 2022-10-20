from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Prefetch
from apps.product.api.serializer.product_serializer import ProductSerializer
from apps.order.api.serializer.order_serializer import OrderSerializer, OrderDetailSerializer, OrderUpdateSerializer, OrderDetailCreateSerializer
from apps.order.models import Order


class OrderViewSets(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = OrderSerializer.Meta.model.objects.all()
    
    # sobre escribo el get_queryset para evitar hacer N+1 y asi hacer menos consultas
    def get_queryset(self, pk=None):
        if pk is None:
            queryset = super().get_queryset()
            queryset = queryset.prefetch_related(
                Prefetch('order')
            )
            return queryset
        return OrderUpdateSerializer.Meta.model.objects.filter(id=pk).first()
    
    def list(self, request):
        order_serializer = self.serializer_class(self.get_queryset(),many=True)
       
        return Response(order_serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        order_serializer = self.serializer_class(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response({'Message':'Order created'}, status=status.HTTP_201_CREATED) 
        return Response({
                'Errors': order_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        order_serializer = OrderUpdateSerializer(self.get_queryset(pk), request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response({'Message':"Order updated successfully!"}, status=status.HTTP_200_OK)
        return Response({'Message':'', 'Error':order_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailViewSets(viewsets.ModelViewSet):
    
    serializer_class = OrderDetailCreateSerializer
    queryset = OrderDetailCreateSerializer.Meta.model.objects.all()

    def create(self, request):
        order_detail_serilizer = self.serializer_class(data=request.data)
        if order_detail_serilizer.is_valid():
            order_detail_serilizer.save()
            return Response({'Message':f"Order detail created in orden {order_detail_serilizer.data['order']} "}, status=status.HTTP_200_OK)
        return Response({'Message':'', 'Error':order_detail_serilizer.errors}, status=status.HTTP_400_BAD_REQUEST)