import re
from datetime import datetime
from urllib.parse import urlparse, parse_qs

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
    ACTIONS = {

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

    def fill_db(self, lines: list) -> dict:
        for line in lines:
            data = self._parse(line)
            print(1)

    def _parse(self, line: str) -> dict:
        url_params = {}
        category, product = None, None
        date_time, ip, url = self.line_pattern.findall(line)[0]
        url_obj = urlparse(url)
        url_parts = url_obj.path.replace('/', ' ').split()
        if url_parts:
            key = self.url_key_pattern.findall(url_obj.path)[0]
            if key not in ['cart', 'pay', 'success_pay_']:
                category, product = url_parts if len(url_parts) == 2 else url_parts[0], None
            else:
                url_params[key] = parse_qs(url_obj.query)

        return {
            'ip': ip,
            'datetime': self._get_datetime(date_time),
            'country': self._get_user_country(ip),
            'category': category,
            'product': product,
            'url_params': url_params
        }

    def _add_item(self, date_time: datetime = None, ip: str = None, **kwargs) -> None:
        print(1)

    def _update_payment_status(self):
        pass

    def _get_user_country(self, ip: str) -> str:
        return self.geo_obj.country_name(ip)

    def _get_datetime(self, date_time: str) -> datetime:
        return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    def _get_data(self, lines: list) -> dict:
        pass

    def save(self) -> None:
        content = self._reader(self.file_path)
        data = self.fill_db(content)
