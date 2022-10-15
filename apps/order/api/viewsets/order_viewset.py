from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Prefetch

from apps.order.api.serializer.order_serializer import OrderSerializer, OrderDetailSerializer



class OrderViewSets(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = OrderSerializer.Meta.model.objects.all()

    # sobre escribo el get_queryset para evitar hacer N+1 y asi hacer menos consultas
    def get_queryset(self):
            queryset = super().get_queryset()
            queryset = queryset.prefetch_related(
                Prefetch('order')
            )
            return queryset

    def create(self, request):
        order_serializer = self.serializer_class(data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response({'Message':'Order created'}, status=status.HTTP_201_CREATED) 
        return Response({
                'Errors': order_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailViewSets(viewsets.ModelViewSet):
    serializer_class = OrderDetailSerializer
    queryset = OrderDetailSerializer.Meta.model.objects.all()


