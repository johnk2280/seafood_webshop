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

    def _reader(self, file_path: str) -> list:
        pass

    def _parse(self, line: str) -> list:
        pass

    def _get_user_country(self, ip: str) -> str:
        pass

    def _get_data(self, lines: list) -> dict:
        pass

    def save(self) -> None:
        pass
