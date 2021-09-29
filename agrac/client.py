import base64
import requests
import urllib.parse

class BaseClient(object):
    def __init__(self, base_url='', session=None, params=None):
        self.base_url = base_url
        self.session = session or requests.Session()
        self.params = params or {}

    def add_slash(self, path):
        return path.strip('/') + '/'

    def path_for(self, part):
        return urllib.parse.urljoin(self.add_slash(self.base_url), str(part))

    def __getitem__(self, part):
        clone = self.clone(base_url=self.path_for(part))
        return clone

    def filter(self, **params):
        clone = self.clone(params=params)
        return clone

    def clone(self, **kwargs):
        initials = self.__dict__.copy()
        initials.update(kwargs)
        clone = self.__class__(**initials)
        return clone

    def get(self, **params):
        params.update(self.params)
        return self.handle_resp(self.session.get(self.base_url, params=params))

    def post(self, **data):
        return self.handle_resp(self.session.post(self.base_url, json=data, params=self.params))
    
    def patch(self, **data):
        return self.handle_resp(self.session.patch(self.base_url, json=data, params=self.params))

    def put(self, **data):
        return self.handle_resp(self.session.put(self.base_url, json=data, params=self._params))

    def delete(self, **params):
        return self.handle_resp(self.session.delete(self.base_url, params=params))

    def handle_resp(self, resp):
        return resp


    __call__ = get
    retrieve = get
    create = post
    update = post

class BasicAuthMixin:

    AUTH_HEAD = 'Authorization'
    def set_auth(self, username, password):
        base64str = base64.urlsafe_b64encode(('%s:%s'%( username, password)).encode())
        self.set_auth_header("Basic %s"%base64str.decode())

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
    

class PageIterMinxin:

    PAGE_SIZE_PARAM = 'size'
    PAGE_NUM_PARAM = 'page'
    PAGE_COUNT_PARAM = 'count'
    PAGE_NEXT_PARAM = 'next'
    PAGE_RESULT_PARAM = 'results'

    def iter_pages(self, max_page=None, **kwargs):
        _kw = self.params.copy()
        _kw.update(kwargs)
        page = kwargs.get(self.PAGE_NUM_PARAM, 1)
        page_size = kwargs.get(self.PAGE_SIZE_PARAM, 10)

        class PageIter(object):
            def __init__(self, page_num, parent, page_size=page_size):
                self.ret = None
                self.parent = parent
                self.page_num = page_num
                self.page_size = page_size

            @property
            def count(self):
                return self.ret[self.parent.PAGE_COUNT_PARAM]

            @property
            def page_count(self):
                return int(self.ret[self.parent.PAGE_COUNT_PARAM] / self.page_size) + 1

            def __iter__(self):

                while self.ret is None or self.ret[self.parent.PAGE_NEXT_PARAM]:
                    kwargs[self.parent.PAGE_NUM_PARAM] = self.page_num
                    if self.page_num > max_page:
                        break
                    self.ret = self.parent.get(**kwargs).json()
                    for i in self.ret[self.parent.PAGE_RESULT_PARAM]:
                        yield i

                    self.page_num += 1


            def __str__(self):
                return "<generator object PageIter at %d >" % id(self)

        return PageIter(page, self, page_size)


class JsonBaseClient(PageIterMinxin, BaseClient):

    def handle_resp(self, resp):
        return resp.json()

class Client(LoginMixin, BasicAuthMixin, JsonBaseClient):
    pass

class TokenAuthClient(TokenAuthMixin, JsonBaseClient):
    pass

class BasicAuthClient(BasicAuthMixin, JsonBaseClient):
    pass
