from platformapi.push_api import PushApi


class PushBase(object):
    def __init__(self):
        self.api = PushApi()

    def login_tenant_base(self):
        return self.api.login_tenant()

    def find_context_aware_event_base(self, parameters):
        return self.api.find_context_aware_event(parameters=parameters)
