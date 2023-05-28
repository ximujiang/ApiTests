from utils.api_base import ApiBase


class PushApi(ApiBase):
    def __init__(self, base_url, timeout=10):
        super().__init__(base_url, timeout)

    def login_tenant(self):
        """
        查看推送列表
        """
        cookies = {
            'Cookie':
                'HttpOnly; siteCode=2B32DC97D4D74484816EB181BE7C67A3; siteThirdLoginUrl=undefined; siteType=1; siteThirdAuthType=undefined; siteTenantId=undefined; TWO-FACTOR-LOGIN-CODE="t4ErCtlLJM7wN12PqQPc6w==Gq53Z88d6Kk1MeAsfkI5sYMw8f9/PQNahE4a2tYaqJnDaN+vyck1njbzhDtw+hDuHaCtA+jwyU+pax6gC00JmlM="; ua=admin@d16fa496f47; vk=d7a7b857-4ac0-4928-82db-9c655a547ff2; lang=zh; HWWAFSESID=2b209792a09749b1dd; HWWAFSESTIME=1684773572556; cdn_token=A732A9AEE6984CFA97D9313C2A2E99A9#1684816785#89ea656c4695a2d0a6780e274cb1ec2c7ebc27a6924e0b18cca9db8f8f85685c; x-wlk-gray=0; SessionID=ec3d46a4-d0d7-4fb4-bc69-463cf20bd30f; ad_sc=; ad_mdm=; ad_cmp=; ad_ctt=; ad_tm=; ad_adp=; cf=Direct; X-XSRF-TOKEN=9005EFD0ECA79E34013AC548C956553261E91A8C19E62B4B41ED6AED8571121331C261B766BC18B6EF3BDE943B7B9061770F; JSESSIONID=78F2B6D91AC30B5AF0F985725429804EF16AE73A0A7705E1'
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
