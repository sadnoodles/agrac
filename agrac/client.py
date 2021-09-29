from .base import BaseClient
from .auth import *

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
