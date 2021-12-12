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
        self._reader(file_path)

    def _reader(self, file_path: str) -> list:
        result = []
        with open(file_path, 'r', encoding='utf-8') as f_obj:
            content = f_obj.readlines()
            data = self._parse(content)
            print(1)

    def _parse(self, lines: list) -> dict:
        for line in lines:
            print(self.line_pattern.findall(line))

    def _get_user_country(self, ip: str) -> str:
        pass

    def _get_data(self, lines: list) -> dict:
        pass

    def save(self) -> None:
        pass
