from service.base.push_base import PushBase
from utils.common import update_yaml_file


class PushService(PushBase):
    def __init__(self):
        super().__init__()

    def login_tenant_service(self):
        res = self.login_tenant_base()
        return res

    def find_context_aware_event_service(self, step, data):
        param = data[step]['request']
        res = self.find_context_aware_event_base(parameters=param)
        # update_yaml_file(data['yaml_file_path'], 'test_demo_one.find_context_aware_event_service.extract.name', 'xxxxx')
        return res
