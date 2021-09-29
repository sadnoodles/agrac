# Agrac
Another Generic REST API Client


调用类一样调用REST API

python 版本。支持以下功能：

1. 登录
2. 会话
3. 重试
4. 相同的URL前缀，无需反复书写
5. 相同模式汇总
6. CRUD自动化
7. 自动翻页
9. Django REST 开箱即用


规则：

1. 方括号[]用来定义URL，可以无限往下调用
    a. 也可以直接使用路径
2. 圆括号()用来定义参数，get是查询参数，update/post/create是数据
3. 返回是可以用点方法获取的json对象


例子：


```ipython
In [1]: from agrac.client import Client

In [2]: c=Client('https://httpbin.org/')

# patch
# curl -X PATCH "https://httpbin.org/patch" -H "accept: application/json"
In [3]: c['patch'].patch()
Out[3]: 
{'args': {},
 'data': '{}',
 'files': {},
 'form': {},
 'headers': {'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate',
  'Content-Length': '2',
  'Content-Type': 'application/json',
  'Host': 'httpbin.org',
  'User-Agent': 'python-requests/2.25.1',
  'X-Amzn-Trace-Id': 'Root=1-615416db-707c6b6925fdeb3d24cc4333'},
 'json': {},
 'origin': '61.150.12.145',
 'url': 'https://httpbin.org/patch'}


# post with data
# curl -X POST "https://httpbin.org/post" -H "accept: application/json"
In [4]: c['post'].post(a=12,b=23)
Out[4]: 
{'args': {},
 'data': '{"a": 12, "b": 23}',
 'files': {},
 'form': {},
 'headers': {'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate',
  'Content-Length': '18',
  'Content-Type': 'application/json',
  'Host': 'httpbin.org',
  'User-Agent': 'python-requests/2.25.1',
  'X-Amzn-Trace-Id': 'Root=1-615416b9-789490957c7909413dec9465'},
 'json': {'a': 12, 'b': 23},
 'origin': '61.150.12.145',
 'url': 'https://httpbin.org/post'}

# get
# curl -X GET "https://httpbin.org/get" -H "accept: application/json"
In [5]: c['get'].get()
Out[5]: 
{'args': {},
 'headers': {'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate',
  'Host': 'httpbin.org',
  'User-Agent': 'python-requests/2.25.1',
  'X-Amzn-Trace-Id': 'Root=1-61541722-3f0a55ab18ab4d8a7ff9eb13'},
 'origin': '61.150.12.145',
 'url': 'https://httpbin.org/get'}


# path
# curl -X POST "https://httpbin.org/delay/1" -H "accept: application/json"
In [8]: c['/delay/1'].post(a=33) # equal to c['delay']['1'].post(a=33)
Out[8]: 
{'args': {},
 'data': '{"a": 33}',
 'files': {},
 'form': {},
 'headers': {'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate',
  'Content-Length': '9',
  'Content-Type': 'application/json',
  'Host': 'httpbin.org',
  'User-Agent': 'python-requests/2.25.1',
  'X-Amzn-Trace-Id': 'Root=1-6154187b-38ffed93163a8ee9051f3824'},
 'origin': '61.150.12.145',
 'url': 'https://httpbin.org/delay/1'}

# path also can be stored
In [9]: delay = c['/delay']
In [10]: delay[1].post()
Out[10]: 
{'args': {},
 'data': '{}',
 'files': {},
 'form': {},
 'headers': {'Accept': '*/*',
  'Accept-Encoding': 'gzip, deflate',
  'Content-Length': '2',
  'Content-Type': 'application/json',
  'Host': 'httpbin.org',
  'User-Agent': 'python-requests/2.25.1',
  'X-Amzn-Trace-Id': 'Root=1-615418c0-2ecb57be5fe2f2ae5a310790'},
 'origin': '61.150.12.145',
 'url': 'https://httpbin.org/delay/1'}

```