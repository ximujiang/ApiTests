from utils.api_base import ApiBase


class PushApi(ApiBase):
    def __init__(self, session=None):
        super().__init__(session=session)

    def find_context_aware_event(self, parameters):
        """
        查看推送列表
        """
        path = '/athenatenant/v1/findcontextawareevent'
        res = self.get(url=path, params=parameters)
        return res
