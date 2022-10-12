from rest_framework.routers import DefaultRouter
from apps.product.api.viewsets.product_viewsets import ProductViewSet



router = DefaultRouter()

router.register(r'products', ProductViewSet, basename='products')

urlpatterns = router.urls