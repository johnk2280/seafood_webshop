from django.urls import path, include
from rest_framework.routers import DefaultRouter

from datarestorerapp.views import (
    ShopUserViewSet,
    ProductViewSet,
    ProductCategoryViewSet,
    OrderViewSet,
    OrderItemViewSet,
    ShopUserActionViewSet,
    LogfileUploadView,
)

app_name = 'datarestorerapp'

router = DefaultRouter(trailing_slash=True)
router.register(r'shop_users', ShopUserViewSet, basename='shop_users')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'product_categories', ProductCategoryViewSet, basename='product_categories')
router.register(r'orders', OrderViewSet, basename='shop_users')
router.register(r'order_items', OrderItemViewSet, basename='order_items')
router.register(r'shop_user_actions', ShopUserActionViewSet, basename='shop_user_actions')

urlpatterns = [
    path('', include(router.urls)),
    path('log_file_upload/', LogfileUploadView.as_view(), name='log_file_upload'),

]
