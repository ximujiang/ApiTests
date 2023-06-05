import requests

from service.login.login_base import LoginBase
from service.scenario.push_service import PushService


class Tenant:
    session = requests.Session()
    push_service = PushService(session=session)
    login_base = LoginBase(session=session)
