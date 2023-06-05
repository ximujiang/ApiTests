import os

import pytest
import requests

from platformapi.push_api import PushApi
from service.scenario.push_service import PushService
from utils import render_template_obj
from utils.api_base import ApiBase
from utils.base import Tenant
from utils.common import read_yaml
from utils.log import set_log_format, log


# @pytest.fixture(scope='class',autouse=True)
# def ste_up():
#     push_service = PushService()
#     return push_service


# def pytest_addoption(parser):  # noqa
#     # run env
#     parser.addini('env', default=None, help='run environment by test or uat ...')
#     parser.addoption(
#         "--env", action="store", default=None, help="run environment by test or uat ..."
#     )
#     parser.addoption("--time-out", action="store", default=10, help="time out value")
#     # # base url
#     # parser.addini("base_url", help="base url for the api test.")
#     # parser.addoption(
#     #     "--base-url",
#     #     metavar="url",
#     #     default=os.getenv("PYTEST_BASE_URL", None),
#     #     help="base url for the api test.",
#     # )
#     # proxies_ip
#     parser.addini("proxies_ip", default=None, help="proxies_ip for the  test.")
#     parser.addoption(
#         "--proxies-ip",
#         action="store", default=None,
#         help="proxies_ip for the  test.",
#     )


def pytest_configure(config):  # noqa
    # 配置日志文件和格式
    set_log_format(config)


@pytest.fixture(scope='session', autouse=True)
def login():
    Tenant.login_base.login_tenant()


@pytest.fixture(scope="function")
def testcase_info(request):
    # 获取当前测试用例的名称
    test_name = request.node.name
    log.debug(f'当前测试：{test_name}')
    # 获取当前测试用例的路径
    test_path = request.node.fspath
    log.debug(f'当前测试路径：{test_name}')
    # 将测试用例的名称和路径封装为一个字典
    testcase_info = dict(name=test_name, path=test_path)

    # 将测试用例的信息返回给测试用例函数
    yield testcase_info


@pytest.fixture(scope="function")
def data(request):
    # 获取当前测试用例的名称
    test_name = request.node.name
    log.debug(f'当前测试：{test_name}')
    # 获取当前测试用例的路径
    test_path = request.node.fspath
    log.debug(f'当前测试路径：{test_path}')
    # 获取文件名和扩展名
    name, ext = os.path.splitext(test_path)
    # 拼接新的文件名
    yaml_file_path = name + '.yaml'
    log.debug(f'用例数据路径：{yaml_file_path}')
    case_data = read_yaml(yaml_file_path)[test_name]
    data = render_template_obj.rend_template_any(case_data, case_data)
    return data

