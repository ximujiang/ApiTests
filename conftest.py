import pytest

from utils.base import Tenant
from utils.common import read_config
from utils.log import set_log_format


def pytest_configure(config):  # noqa
    # 配置日志文件和格式
    set_log_format(config)


@pytest.fixture(scope='session', autouse=True)
def login():
    account_info = read_config('account')
    Tenant.login_base.login_tenant(account_info)
