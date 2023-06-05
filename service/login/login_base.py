from platformapi.login_api import LoginApi


class LoginBase(LoginApi):
    def __init__(self, session=None):
        super().__init__(session=session)

    def login_tenant_base(self):
        return self.login_tenant()
