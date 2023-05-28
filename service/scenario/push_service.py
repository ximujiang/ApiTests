from service.base.push_base import PushBase


class PushService(PushBase):
    def __init__(self, base_url=None, timeout=None):
        super().__init__(base_url=base_url, timeout=timeout)

    def login_tenant_service(self):
        res = self.login_tenant_base()
        return res

    def find_context_aware_event_service(self, parameters):
        res = self.find_context_aware_event_base(parameters=parameters)
        return res
