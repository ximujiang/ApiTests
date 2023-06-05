import requests

from utils.api_base import ApiBase
from utils.common import write_config
from utils.log import log
from config import HEADERS


class LoginApi(ApiBase):
    def __init__(self, session=None):
        super().__init__(session=session)

    def login_tenant(self):
        """
        查看推送列表
        """
        cookies = {
            'Cookie':
                'HttpOnly; siteCode=2B32DC97D4D74484816EB181BE7C67A3; siteThirdLoginUrl=undefined; siteType=1; siteThirdAuthType=undefined; siteTenantId=undefined; ua=admin@d16fa496f47; vk=d7a7b857-4ac0-4928-82db-9c655a547ff2; lang=zh; HWWAFSESID=2b209792a09749b1dd; HWWAFSESTIME=1684773572556; x-wlk-gray=0; SessionID=ec3d46a4-d0d7-4fb4-bc69-463cf20bd30f; ad_sc=; ad_mdm=; ad_cmp=; ad_ctt=; ad_tm=; ad_adp=; cf=Direct; TWO-FACTOR-LOGIN-CODE="+OkGIr1SH4P+nCMsnMwy7Q==/fMoqnfEO0Qzd3Q8Hv0GXKxS9GDdeTVzX9B/wvy6RGQS3Tasn1hDwk1Td+e9wayiEmlvhE5gCv2n4Wkpw8PuHvU="; cdn_token=A732A9AEE6984CFA97D9313C2A2E99A9#1685478541#880910e9d8fd9aa0812bc235264b5e718a692be533e450edf58d0b8dd4edc289; JSESSIONID=C663E6D957F8760D62F39BC19133565D2F1C24A5079C245B; X-XSRF-TOKEN=B50392807D146988DB26C4DD474C9E8E1CA49223CE3D9E9E0B8A527B7236856C6823A00BE3E9FF210082A97106C494E21F8E'
        }
        data = {
            'tenantId': 'A732A9AEE6984CFA97D9313C2A2E99A9',
            'thirdAuthType': 1,
            'userName': 'admin@d16fa496f47',
            'password': 'lkjLKJ+2023',
            'redirect_url': 'redirect_uri=https%3A%2F%2Fwelink.huaweicloud.com%2Fweb%2Fapp%2F%23%2Fathena-tenant%2FrightManaulTrigger%2FdesPage',
            'errorCode': None,
            'sliderUid': None,
            'mobile': '+86-18576797850'
        }
        url = 'https://login.welink.huaweicloud.com/sso/v3/pclogintenant'
        res = self.post(url=url, data=data, cookies=cookies)
        token = res.headers['X-XSRF-TOKEN']
        # header = {"X-XSRF-TOKEN": f"{token}"}
        write_config('Headers', 'TOKEN', token)



class PushApi(ApiBase):
    def __init__(self, session=None):
        super().__init__(session=session)

    def push_service(self):
        url2 = 'https://welink.huaweicloud.com/athenatenant/v1/findapprovalcontextaware'
        datas = {"title": "", "pageNumber": 1, "pageSize": 10}
        params = {"language": "zh"}

        # 发送post请求
        ress = self.post(url=url2, json=datas, params=params)
        print(ress.text)


if __name__ == '__main__':
    session1 = requests.Session()
    api = LoginApi(session=session1)
    print(api.session)
    api.login_tenant()
    # 设置请求url/data等入参

    api2 = PushApi(session=session1)
    print(api2.session)
    print(f'{api2.headers}')
    api2.push_service()
