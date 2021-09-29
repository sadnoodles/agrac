import base64
class BasicAuthMixin:

    AUTH_HEAD = 'Authorization'
    def set_auth(self, username, password):
        base64str = base64.urlsafe_b64encode(b'%s:%s'%( username, password))
        self.set_auth_header("Basic %s"%base64str)

    def set_auth_header(self, auth_str):
        self.session.headers[self.AUTH_HEAD] = auth_str

class TokenAuthMixin(BasicAuthMixin):
    def set_auth(self, token):
        self.set_auth_header("Token %s"%token)
    
class LoginMixin:
    
    def login(self, username, password, login_url='login/', **kwargs):
        return self[login_url].post(
            username=username,
            password=password,
            **kwargs
        )
    