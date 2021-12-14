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
from datarestorerapp.queries import (
    get_country_by_users,
    get_country_by_category,
    get_time_of_day_by_category,
    get_max_number_of_requests_per_hour,
    get_other_frequently_ordered_items,
    get_unpaid_baskets_quantity,
    get_regular_customer,
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
        return Response(
            {
                'status': 'ok',
                'message': 'logfile uploaded'
            }
        )


class TaskOneView(APIView):
    """
    1. Посетители из какой страны чаще всего посещают сайт?
    """

    def get(self, request):
        country, visit_count = get_country_by_users()[0]
        return Response(
            {
                'country': country,
                'number of visits': visit_count
            }
        )


class TaskTwoView(APIView):
    """
    2. Посетители из какой страны чаще всего интересуются товарами из
    определенной категории “fresh_fish”?
    """

    category_name = 'fresh_fish'

    def get(self, request):
        country, request_count = get_country_by_category(self.category_name)[0]
        return Response(
            {
                'country': country,
                'number of requests': request_count
            }
        )


class TaskThreeView(APIView):
    """
    3. В какое время суток чаще всего просматривают категорию “frozen_fish”?

    0 - ночь 00.00 - 05.59
    1 - утро 06.00 - 11.59
    2 - день 12.00 - 17.59
    3 - вечер 18.00 - 23.59
    """

    DAYTIME_MAPPER = {
        0: 'night (00.00 - 05.59)',
        1: 'morning (06.00 - 11.59)',
        2: 'day (12.00 - 17.59)',
        3: 'evening (00.00 - 23.59)',
    }
    category_name = 'frozen_fish'

    def get(self, request):
        daytime, requests_count = get_time_of_day_by_category(self.category_name)[0]
        return Response(
            {
                'daytime': self.DAYTIME_MAPPER[daytime],
                'number of requests': requests_count
            }
        )


class TaskFourView(APIView):
    """
    4. Какое максимальное число запросов на сайт за астрономический час
    (с 00 минут 00 секунд до 59 минут 59 секунд)?
    """

    def get(self, request):
        date_time, requests_count = get_max_number_of_requests_per_hour()[0]
        return Response(
            {
                'datetime': date_time,
                'max number of requests per hour': requests_count
            }
        )


class TaskFiveView(APIView):
    """
    5. Товары из какой категории чаще всего покупают совместно с товаром из
    категории “semi_manufactures”?
    """

    category_name = 'semi_manufactures'

    def get(self, request):
        category_id, order_count = get_other_frequently_ordered_items(self.category_name)[0]
        category = ProductCategory.objects.get(id=category_id)
        return Response(
            {
                'category id': category.id,
                'category name': category.name,
                'orders number': order_count
            }
        )


class TaskSixView(APIView):
    """
    6. Сколько не оплаченных корзин имеется?
    """

    def get(self, request):
        cart_count = get_unpaid_baskets_quantity()[0][0]
        return Response(
            {
                'number of unpaid carts': cart_count
            }
        )


class TaskSevenView(APIView):
    """
    7. Какое количество пользователей совершали повторные покупки?
    """

    def get(self, request):
        customers_count = get_regular_customer()[0][0]
        return Response(
            {
                'number of regular customers': customers_count
            }
        )
