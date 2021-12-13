import re
import socket
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from django.contrib.gis.geoip2 import GeoIP2, GeoIP2Exception
from geoip2.errors import AddressNotFoundError

from datarestorerapp.models import (
    ShopUser,
    ProductCategory,
    Product,
    Order,
    OrderItem,
    ShopUserAction,
)


class LogParser:
    LINE_PATTERN = r'^.*?(?P<date_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})' \
                   r'.*?(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' \
                   r'.*?(?P<url>http.*)$'
    URL_KEY_PATTERN = r'^\/(?P<key>[a-zA-Z_]+)'
    USER_ACTIONS = {
        'product': 'product viewing',
        'category': 'category viewing',
        'main': 'main viewing',
        'cart': 'add item to order',
        'pay': 'order viewing',
        'success_pay_': 'payed',
    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.line_pattern = re.compile(self.LINE_PATTERN)
        self.url_key_pattern = re.compile(self.URL_KEY_PATTERN)
        self.geo_obj = GeoIP2()

    def _reader(self, file_path: str) -> list:
        with open(file_path, 'r', encoding='utf-8') as f_obj:
            content = f_obj.readlines()

        return content

    def fill_db(self, lines: list) -> None:
        for line in lines:
            action = 'main'
            data = self._parse(line)
            user, _ = ShopUser.objects.get_or_create(ip=data['ip'], country=data['country'])

            if not data['url_params']:
                if data['category']:
                    action = 'category'
                    category, _ = ProductCategory.objects.get_or_create(name=data['category'])

                    if data['product']:
                        action = 'product'
                        product, _ = Product.objects.get_or_create(category=category, name=data['product'])
            else:
                key = list(data['url_params'].keys())[0]
                action = key
                if key == 'cart':
                    order, order_is_created = Order.objects.get_or_create(
                        id=int(data['url_params'][key]['cart_id'][0]),
                        user=user,
                        defaults={
                            'created_at': data['datetime'],
                            'updated_at': data['datetime'],
                        }
                    )
                    if not order_is_created:
                        order.updated_at = data['datetime']
                        order.save()

                    item = OrderItem(
                        order=order,
                        product_id=int(data['url_params'][key]['goods_id'][0]),
                        amount=int(data['url_params'][key]['amount'][0]),
                        created_at=data['datetime']
                    )
                    item.save()

                if key == 'success_pay_':
                    order_id = data['success_pay_']
                    order = Order.objects.filter(id=order_id).get()
                    order.is_paid = True
                    order.updated_at = data['datetime']
                    order.save()

            user_action = ShopUserAction(
                user=user,
                action=self.USER_ACTIONS[action],
                created_at=data['datetime']
            )
            user_action.save()

            data.clear()

    def _parse(self, line: str) -> dict:
        url_params = {}
        category, product = None, None
        success_pay_id = None

        date_time, ip, url = self.line_pattern.findall(line)[0]
        url_obj = urlparse(url)
        key = self.url_key_pattern.findall(url_obj.path)

        if key:
            if key[0] not in ['cart', 'pay', 'success_pay_']:
                category, product = self._get_url_parts(url_obj)
            else:
                url_params[key[0]] = parse_qs(url_obj.query)
                success_pay_id = int(url_obj.path[13:-1]) if key[0] == 'success_pay_' else None

        return {
            'ip': ip,
            'datetime': self._get_datetime(date_time),
            'country': self._get_user_country(ip),
            'category': category,
            'product': product,
            'success_pay_': success_pay_id,
            'url_params': url_params,
        }

    def _get_user_country(self, ip: str) -> str:
        try:
            return self.geo_obj.country_name(ip)
        except (GeoIP2Exception, AddressNotFoundError, socket.gaierror) as errors:
            return f'N/A'

    def _get_datetime(self, date_time: str) -> datetime:
        return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    def _get_url_parts(self, url_obj):
        url_parts = url_obj.path.replace('/', ' ').split()
        try:
            return url_parts[0], url_parts[1]
        except IndexError:
            return url_parts[0], None

    def save(self) -> None:
        content = self._reader(self.file_path)
        self.fill_db(content)
