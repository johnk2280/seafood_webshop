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
        pass



