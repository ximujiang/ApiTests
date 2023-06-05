import pytest
import yaml
from utils.base import Tenant
from utils.log import log


class TestDemo(Tenant):

    def test_demo_one(self, data):
        # pass
        res = self.push_service.find_context_aware_event_service('find_context_aware_event_service', data)
        log.debug(res.text)


