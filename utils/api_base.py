import re

import requests

from utils import exceptions
from utils.log import log
from utils.common import read_config, write_config, extract_response


class ApiBase:
    """
    客户端基类，用于创建 HTTP 请求和处理返回结果。
    """

    def __init__(self, session=None):
        """
        构造函数，初始化类的基本属性。
        """
        # API 基础 URL
        self.base_url = read_config('DEFAULT', 'BASE_URL')
        # 请求超时时间
        self.timeout = int(read_config('DEFAULT', 'DEFAULT_TIMEOUT'))
        # 使用会话对象以便在多个请求之间共享信息
        self.session = session or requests.Session()
        # 设置请求头信息

    def update_headers(self):
        """
        用于更新 HTTP 请求的头部信息。
        :return: 更新后的请求头
        """
        # 从配置文件中获取 USER_AGENT 和 TOKEN
        user_agent = read_config('Headers', 'USER_AGENT')
        token = read_config('Headers', 'TOKEN')

        # 更新请求头
        self.session.headers.update({'User-Agent': f'{user_agent}'})
        self.session.headers.update({"X-XSRF-TOKEN": f"{token}"})

        # 获取更新后的请求头
        headers = self.session.headers
        return headers

    def request(self, method, url, base_url=None, timeout=None, params=None, data=None, json=None, files=None,
                headers=None,
                **kwargs):
        """
        发送HTTP请求.
        :param method: 请求方法，eg：get/post/put/delete；
        :param url: 请求url
        :param base_url: 请求基础url；
        :param timeout: 请求超时时间
        :param params: get请求的查询参数
        :param data: 需要发送的数据，可以是一个字典或字符串；
        :param json: 需要发送的数据，可以是一个字典或字符串；
        :param files:需要上传的文件，需要传递一个字典对象，其中key为文件名，value为文件对象；
        :param headers: 需要发送的请求头，需要传递一个字典对象；
        :param kwargs: 其他需要设置的参数，可以是任意关键字参数；
        :return:
        """
        full_url = self.check_url(base_url, url) if base_url else self.check_url(self.base_url, url)
        headers = headers if headers else self.update_headers()
        time_out = timeout if timeout else self.timeout
        res = self.session.request(method, url=full_url, params=params, data=data, json=json, files=files,
                                   headers=headers, timeout=time_out, **kwargs)
        res.encoding = 'utf-8'
        return res

    def get(self, url, params=None, headers=None, **kwargs):
        """
        发送HTTP get请求。
        :param url: 请求的 URL 地址
        :param params: 可选参数，GET 请求的查询参数，默认为 None
        :param headers: 可选参数，请求头信息，默认为 None
        :param kwargs: 可选参数，其他可传递给 request 方法的关键字参数
        :return: 返回HTTP响应对象
        """
        return self.request('GET', url, params=params, headers=headers, **kwargs)

    def post(self, url, data=None, json=None, files=None, headers=None, **kwargs):
        """
        发送HTTP POST请求。
        :param url: 请求地址
        :param data: 请求的数据内容，通常为dict或字符串形式
        :param json: 请求的json数据，通常为dict形式
        :param files: 上传的文件，通常为dict形式，key为文件名，value为文件内容
        :param headers: 请求的头信息，通常为dict形式
        :param kwargs: 可选参数，用于传递其他用于请求的参数，例如请求超时或代理设置。
        :return: 返回HTTP响应对象
        """
        return self.request('POST', url, data=data, json=json, files=files, headers=headers, **kwargs)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        """
        发送 PUT 请求，返回响应对象。
        :param url: 目标 URL。
        :param data: 请求正文（默认为 None）。
        :param json: 请求正文作为 JSON 序列化（默认为 None）。
        :param headers: 字典类型的 HTTP 头（默认为 None）。
        :param kwargs: 可选参数，用于传递其他用于请求的参数，例如请求超时或代理设置。
        :return: 请求的响应对象。
        """
        return self.request('PUT', url, data=data, json=json, headers=headers, **kwargs)

    def delete(self, url, **kwargs):
        """
        发送 delete 请求，返回响应对象。
        :param url: 目标 URL。
        :param kwargs: 可选参数，用于传递其他用于请求的参数，例如请求超时或代理设置。
        :return: 请求的响应对象。
        """
        return self.request('DELETE', url, **kwargs)

    @staticmethod
    def check_url(base_url: str, url: str) -> str:
        """
        根据给定的基础网址和URL检查URL是否是合法的，并返回合法的URL。
        :param base_url: 基础网址，格式应为 http(s)://
        :param url: 待检查的URL
        :return: 返回合法的URL
        """
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


if __name__ == '__main__':
    api = ApiBase()
    cookies = {
        'Cookie':
            'HttpOnly; siteCode=2B32DC97D4D74484816EB181BE7C67A3; siteThirdLoginUrl=undefined; siteType=1; siteThirdAuthType=undefined; siteTenantId=undefined; ua=admin@d16fa496f47; vk=d7a7b857-4ac0-4928-82db-9c655a547ff2; lang=zh; HWWAFSESID=2b209792a09749b1dd; HWWAFSESTIME=1684773572556; x-wlk-gray=0; SessionID=ec3d46a4-d0d7-4fb4-bc69-463cf20bd30f; ad_sc=; ad_mdm=; ad_cmp=; ad_ctt=; ad_tm=; ad_adp=; cf=Direct; TWO-FACTOR-LOGIN-CODE="+OkGIr1SH4P+nCMsnMwy7Q==/fMoqnfEO0Qzd3Q8Hv0GXKxS9GDdeTVzX9B/wvy6RGQS3Tasn1hDwk1Td+e9wayiEmlvhE5gCv2n4Wkpw8PuHvU="; cdn_token=A732A9AEE6984CFA97D9313C2A2E99A9#1685638619#620a84ce080e37a26acb0295c26559b15fd108a83158acda199e7b051baec40c; X-XSRF-TOKEN=B92C173CB3AD571C6EB170065ACE6FF0271836BA9973F938834B8E213ECACFA808047D8078BAC4F776D7B8B2DA8ADCCBC104; JSESSIONID=137E45355B120EB34B41B2C79FD3242E9635E40DAD364A63'
    }
    data1 = {
        'tenantId': 'A732A9AEE6984CFA97D9313C2A2E99A9',
        'thirdAuthType': 1,
        'userName': 'admin@d16fa496f47',
        'password': 'lkjLKJ+2023',
        'redirect_url': 'redirect_uri=https%3A%2F%2Fwelink.huaweicloud.com%2Fweb%2Fapp%2F%23%2Fathena-tenant%2FrightManaulTrigger%2FdesPage',
        'errorCode': None,
        'sliderUid': None,
        'mobile': '+86-18576797850'
    }
    url1 = 'https://login.welink.huaweicloud.com/sso/v3/pclogintenant'
    res1 = api.post(url=url1, data=data1, cookies=cookies)
    tokens = res1.headers['X-XSRF-TOKEN']
    write_config('Headers', 'TOKEN', tokens)

    # 设置请求url/data等入参
    url2 = 'https://welink.huaweicloud.com/athenatenant/v1/findapprovalcontextaware'
    datas = {"title": "", "pageNumber": 1, "pageSize": 10}
    params1 = {"language": "zh"}
    # 发送post请求
    res2 = api.post(url=url2, json=datas, params=params1)
    print(res2.text)

    url3 = 'athenatenant/v1/findcontextawareevent'
    params2 = {
        "name": "",
        "pageNumber": 1,
        "pageSize": 10,
        "startTime": "2023-04-16",
        "endTime": "2023-06-01",
        "n": 0.5998682653328589,
        "language": "zh"
    }
    # 发送get请求
    res3 = api.get(url=url3, params=params2)
    print(res3.text)
    eventId = extract_response(res3, {'eventId': '$..pageCount'})
    print(eventId)
