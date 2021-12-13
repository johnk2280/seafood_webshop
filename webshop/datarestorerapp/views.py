from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework import generics, viewsets, mixins

from datarestorerapp.log_parser import LogParser
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
    """
    List of shop users.
    """

    serializer_class = ShopUserSerializer
    queryset = ShopUser.objects.all()


class ProductViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    List of products.
    """
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ProductCategoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    List of product categories.
    """

    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()


class OrderViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    Orders list.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderItemViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    List of orders items.
    """
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()


class ShopUserActionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    List of shop user activity.
    """
    serializer_class = ShopUserActionSerializer
    queryset = ShopUserAction.objects.all().order_by('-id')[:1000]


class LogfileUploadView(APIView):
    """
    File upload view.
    """
    parser_classes = (MultiPartParser, FileUploadParser,)

    def post(self, request) -> Response:
        parser = LogParser(request.data.get('text').temporary_file_path())
        parser.save()
        return Response('ok')
