from datetime import datetime
import re
from urllib.parse import urlparse, parse_qs

from django.contrib.gis.geoip2 import GeoIP2


class LogParser:
    LINE_PATTERN = r"^" \
                   r".*?(?P<date_time>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})" \
                   r".*?(?P<ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})" \
                   r".*?(?P<url>http.*)" \
                   r"$"
    ACTIONS = {

    }

    def __init__(self, file_path):
        self.file_path = file_path
        self.line_pattern = re.compile(self.LINE_PATTERN)
        self.geo_obj = GeoIP2()

        # self._reader(file_path)
        self.save()

    def _reader(self, file_path: str) -> list:
        with open(file_path, 'r', encoding='utf-8') as f_obj:
            content = f_obj.readlines()

        return content

    def _parse(self, lines: list) -> dict:
        for line in lines:
            date_time, ip, url = self.line_pattern.findall(line)[0]
            date_time_obj = self._get_datetime(date_time)
            country = self._get_user_country(ip)
            url_parts = self._parse_url(url)

    def _parse_url(self, url: str) -> list:
        url_obj = urlparse(url)
        url_params = parse_qs(url_obj.query)
        print(1)

    def _get_user_country(self, ip: str) -> str:
        return self.geo_obj.country_name(ip)

    def _get_datetime(self, date_time: str) -> datetime:
        return datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')

    def _get_data(self, lines: list) -> dict:
        pass

    def save(self) -> None:
        content = self._reader(self.file_path)
        data = self._parse(content)
