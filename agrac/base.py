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
