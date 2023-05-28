import re

import pytest
import requests

from utils import exceptions
from utils.log import log


class ApiBase:
    # 构造函数，传入session对象
    def __init__(self, base_url: str = None, timeout=10, headers=None):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = headers or self.session.headers

    @staticmethod
    def check_url(base_url: str, url: str) -> str:
        """ 拼接base_url 和 url 地址"""
        if re.compile(r"(http)(s?)(://)").match(url):
            return url
        elif base_url:
            if re.compile(r"(http)(s?)(://)").match(base_url):
                return f"{base_url.rstrip('/')}/{url.lstrip('/')}"
            else:
                log.error(f'{base_url} -->  base url do yo mean http:// or https://!')
                raise exceptions.ParserError("base url do yo mean http:// or https://!")
        else:
            log.error(f'{url} --> url invalid or base url missed!')
            raise exceptions.ParserError("url invalid or base url missed!")

    # 判断url是否需要拼接base_url
    def _build_url(self, url):
        if url.startswith('http://') or url.startswith('https://'):
            return url
        return "{}{}".format(self.base_url, url)

    # 发送请求
    def send_request(self, method, url, base_url=None, data=None, json=None, headers=None, **kwargs):
        headers = headers if headers else self.headers
        full_url = self.check_url(base_url, url) if base_url else self.check_url(self.base_url, url)
        # full_url = self._build_url(url)
        log.debug('{} request to {}'.format(method, full_url))

        if data:
            log.debug('request body: {}'.format(data))
        elif json:
            log.debug('request body: {}'.format(json))

        response = self.session.request(method, full_url, data=data, json=json, headers=headers, **kwargs)

        log.debug('status code: {}'.format(response.status_code))
        log.debug('response body: {}'.format(response.text))
        return response

    # 发送GET请求
    def get(self, url, params=None, **kwargs):
        return self.send_request('GET', url, params=params, **kwargs)

    # 发送POST请求
    def post(self, url, data=None, json=None, **kwargs):
        return self.send_request('POST', url, data=data, json=json, **kwargs)

    # 发送PUT请求
    def put(self, url, data=None, **kwargs):
        return self.send_request('PUT', url, data=data, **kwargs)

    # 发送DELETE请求
    def delete(self, url, **kwargs):
        return self.send_request('DELETE', url, **kwargs)
