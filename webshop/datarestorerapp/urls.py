from django.urls import path, include
from rest_framework.routers import DefaultRouter

from datarestorerapp.views import (
    ShopUserViewSet,
    ProductViewSet,
    ProductCategoryViewSet,
    OrderViewSet,
    OrderItemViewSet,
    ShopUserActionViewSet,
)

router = DefaultRouter(trailing_slash=True)
router.register(r'shop_users', ShopUserViewSet, basename='shop_users')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'product_categories', ProductCategoryViewSet, basename='product_categories')
router.register(r'orders', OrderViewSet, basename='shop_users')
router.register(r'order_items', OrderItemViewSet, basename='order_items')
router.register(r'shop_user_actions', ShopUserActionViewSet, basename='shop_user_actions')

app_name = 'datarestorerapp'

urlpatterns = [
    path('', include(router.urls))
    # path('shop_users/', ShopUserListView.as_view(), name='shop_users'),
    # path('products/'),
    # path('product_categories/'),
    # path('orders/'),
    # path('order_items/'),
]
