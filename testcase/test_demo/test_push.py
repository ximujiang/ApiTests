import pytest


# from service.scenario.push_service import PushService


class TestDemo():

    def test_demo_one(self, push_api):
        push_tdata = {
            'name': '',
            'pageNumber': 1,
            'pageSize': 10,
            'startTime': '2023-04-16',
            'endTime': '2023-05-16',
            'n': 0.5998682653328589,
            'language': 'zh'
        }
        res = push_api.find_context_aware_event_service(push_tdata)
        print(res)
