from utils.api_base import ApiBase


class PushApi(ApiBase):
    def __init__(self):
        super().__init__()

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
        headers = {"X-XSRF-TOKEN": f"{token}",
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
        self.session.headers.update(headers)
        return self.session.headers

    def find_context_aware_event(self, parameters):
        """
        查看推送列表
        """
        path = '/athenatenant/v1/findcontextawareevent'
        res = self.get(url=path, params=parameters)
        return res


if __name__ == '__main__':
    push_api = PushApi(base_url='https://welink.huaweicloud.com')
    response = push_api.login_tenant()
    # print(push_api.session.headers)
    print(response)
# {'User-Agent': 'python-requests/2.30.0',
#  'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive','X-XSRF-TOKEN':
#  '6E14167AC5372073558640C1694DE62B0260B10B536D805DBA5634371A149EB1D50ECFB7B26E78250B5DA03BA2115FBBFB3F'}
# {'X-XSRF-TOKEN':
# '6E14167AC5372073558640C1694DE62B0260B10B536D805DBA5634371A149EB1D50ECFB7B26E78250B5DA03BA2115FBBFB3F'}
