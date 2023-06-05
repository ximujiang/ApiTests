from platformapi.push_api import PushApi


class PushBase(PushApi):
    def __init__(self, session=None):
        super().__init__(session=session)

    def find_context_aware_event_base(self, parameters):
        return self.find_context_aware_event(parameters=parameters)
