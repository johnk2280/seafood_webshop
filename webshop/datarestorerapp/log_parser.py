import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs, parse_qsl

from django.contrib.gis.geoip2 import GeoIP2

from datarestorerapp.models import (
    ShopUser,
    ProductCategory,
    Product,
    Order,
    OrderItem,
    ShopUserAction,
)


class LogParser:
    LINE_PATTERN = r"^" \
                   r".*?(?P<date_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})" \
                   r".*?(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})" \
                   r".*?(?P<url>http.*)" \
                   r"$"
    URL_KEY_PATTERN = r'^\/(?P<key>[a-zA-Z_]+)'
    CAT_PROD_PATTEN = r'[a-zA-Z_]+'
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
        self.cat_prod_pattern = re.compile(self.CAT_PROD_PATTEN)
        self.geo_obj = GeoIP2()

        self.save()

    def _reader(self, file_path: str) -> list:
        with open(file_path, 'r', encoding='utf-8') as f_obj:
            content = f_obj.readlines()

        return content

    def fill_db(self, lines: list) -> None:
        for line in lines:
            key = 'main'
            data = self._parse(line)
            user, _ = ShopUser.objects.get_or_create(ip=data['ip'], country=data['country'])

            if not data['url_params']:
                if data['category']:
                    key = 'category'
                    category, _ = ProductCategory.objects.get_or_create(name=data['category'])

                    if data['product']:
                        key = 'product'
                        product, _ = Product.objects.get_or_create(category=category, name=data['product'])
            else:
                key = list(data['url_params'].keys())[0]
                if key == 'cart':
                    product_id = int(data['url_params'][key]['goods_id'][0])
                    amount = int(data['url_params'][key]['amount'][0])
                    order_id = int(data['url_params'][key]['cart_id'][0])

                    order, _ = Order.objects.get_or_create(id=order_id, user=user, created_at=data['datetime'])
                    item = OrderItem(order=order, product_id=product_id, amount=amount, created_at=data['datetime'])
                    item.save()

                if key == 'success_pay_':
                    order_id = data['success_pay_id']
                    order = Order.objects.get(id=order_id)
                    order.is_paid = True
                    order.save()

                    print(1)

            user_action = ShopUserAction(user=user, action=self.USER_ACTIONS[key], created_at=data['datetime'])
            user_action.save()

    def _parse(self, line: str) -> dict:
        url_params = {}
        category, product = None, None
        success_pay_id = None

        date_time, ip, url = self.line_pattern.findall(line)[0]
        url_obj = urlparse(url)
        url_parts = tuple(url_obj.path.replace('/', ' ').split())

        if url_parts:
            key = self.url_key_pattern.findall(url_obj.path)[0]
            if key not in ['cart', 'pay', 'success_pay_']:
                category, product = url_parts if len(url_parts) == 2 else url_parts[0], None
                success_pay_id = int(url_obj.path[12:]) if key == 'success_pay_' else None
            else:
                url_params[key] = parse_qs(url_obj.query)

        return {
            'ip': ip,
            'datetime': self._get_datetime(date_time),
            'country': self._get_user_country(ip),
            'category': category,
            'product': product,
            'success_pay_': success_pay_id,
            'url_params': url_params,
        }

    def _add_item(self, date_time: datetime = None, ip: str = None, **kwargs) -> None:
        print(1)

    def _update_payment_status(self):
        pass

    def _get_user_country(self, ip: str) -> str:
        return self.geo_obj.country_name(ip)

    def _get_datetime(self, date_time: str) -> datetime:
        return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    def save(self) -> None:
        content = self._reader(self.file_path)
        data = self.fill_db(content)
