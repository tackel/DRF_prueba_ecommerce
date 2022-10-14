from rest_framework.routers import DefaultRouter

from apps.order.api.viewsets.order_viewset import OrderViewSets, OrderDetailViewSets

router = DefaultRouter()

router.register(r'order', OrderViewSets, basename='order')
router.register(r'orderdetail', OrderDetailViewSets, basename='orderdetail')

urlpatterns = router.urls