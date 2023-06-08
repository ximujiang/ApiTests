from service.base.push_base import PushBase
from utils.common import get_test_data, extract_response, update_test_data


class PushService(PushBase):
    def __init__(self, session=None):
        super().__init__(session=session)

    def find_context_aware_event_service(self, step_name):
        step_data = get_test_data(step_name)
        print(f'---------------------{step_data}')
        param = step_data.get('request')
        res = self.find_context_aware_event_base(parameters=param)
        extract_result = extract_response(res, {'eventId': '$..eventId'})
        update_test_data(step_name, extract_result)
        return res.text
