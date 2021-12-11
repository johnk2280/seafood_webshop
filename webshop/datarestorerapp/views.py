from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets, mixins

from datarestorerapp.models import (
    ShopUser,
    Product,
    ProductCategory,
    Order,
    OrderItem,
    ShopUserAction,
)
from datarestorerapp.serializers import (
    ShopUserSerializer,
    ProductSerializer,
    ProductCategorySerializer,
    OrderSerializer,
    OrderItemSerializer,
    ShopUserActionSerializer,
)


class ShopUserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ShopUserSerializer
    queryset = ShopUser.objects.all()


class ProductViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCategoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()


class OrderViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


class ShopUserActionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ShopUserActionSerializer
    queryset = ShopUserAction.objects.all()

# line_pattern = r"^" \
#                r".*?(?P<date_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})" \
#                r".*?(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})" \
#                r".*?(?P<url>http.*)" \
#                r"$"
