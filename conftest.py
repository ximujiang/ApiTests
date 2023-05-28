import os

import pytest

from platformapi.push_api import PushApi
from service.scenario.push_service import PushService
from utils.log import set_log_format


@pytest.fixture(scope='session')
def push_api(request):
    # 读取pytest.ini中的配置
    base_url = request.config.getoption('base_url')
    time_out = request.config.getoption('time_out')
    push_service = PushService(base_url=base_url, timeout=time_out)
    return push_service


def pytest_addoption(parser):  # noqa
    # run env
    parser.addini('env', default=None, help='run environment by test or uat ...')
    parser.addoption(
        "--env", action="store", default=None, help="run environment by test or uat ..."
    )
    parser.addoption("--time-out", action="store", default=10, help="time out value")
    # # base url
    # parser.addini("base_url", help="base url for the api test.")
    # parser.addoption(
    #     "--base-url",
    #     metavar="url",
    #     default=os.getenv("PYTEST_BASE_URL", None),
    #     help="base url for the api test.",
    # )
    # proxies_ip
    parser.addini("proxies_ip", default=None, help="proxies_ip for the  test.")
    parser.addoption(
        "--proxies-ip",
        action="store", default=None,
        help="proxies_ip for the  test.",
    )


def pytest_configure(config):  # noqa
    # 配置日志文件和格式
    set_log_format(config)


@pytest.fixture(scope='session', autouse=True)
def login(push_api):
    push_api.login_tenant_service()



