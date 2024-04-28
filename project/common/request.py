# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
#                                 request.py                                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* *-*-*-*-*-*-*-* #
# Description:                                                                                #
#     This script compares two files.                                                         #
#                                                                                             #
# Author     : cl                                                                             #
# Version    : v1.0                                                                           #
# CreTime    : 2024/4/26                                                                      #
# License    : Copyright (c) 2024 by cl, All rights reserved                                  #
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-* #


def get(url, params={}, headers={}, auth=None):
    """Sends a GET request. Returns :class:`Response` object.

    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary of GET Parameters to send with the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to sent with the :class:`Request`.
    :param auth: (optional) AuthObject to enable Basic HTTP Auth.
    """

    r = Request()

    r.method = 'GET'
    r.url = url
    r.params = params
    r.headers = headers
    # r.auth = _detect_auth(url, auth)

    r.send()

    return r.response

class Response:
    pass


class Request(object):
    """The :class:`Request` object. It carries out all functionality of
    Requests. Recommended interface is with the Requests functions.

    """

    _METHODS = ('GET', 'HEAD', 'PUT', 'POST', 'DELETE')

    def __init__(self):
        self.url = None
        self.headers = dict()
        self.method = None
        self.params = {}
        self.data = {}
        self.response = Response()
        self.auth = None
        self.sent = False

    def __repr__(self):
        try:
            repr = '<Request [%s]>' % (self.method)
        except:
            repr = '<Request object>'
        return repr

    def __setattr__(self, name, value):
        if (name == 'method') and (value):
            if not value in self._METHODS:
                raise ValueError('Method is undefined')

        object.__setattr__(self, name, value)


r = Request()
print(r)
r.method = "UHH"
print(r)


from types import MethodType

class Student():
    pass

s = Student()
s1 = Student()


def set_age(self, age):
    self.age = age

# s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
# s.set_age = set_age # 给实例绑定一个方法
# s.set_age(s, 10)

# Student.__setattr__('set_age', set_age)       # 报错

# Student.set_age = MethodType(set_age, Student)  # 给类绑定一个方法
# Student.set_age = set_age                     # 给类绑定一个方法

s.set_age(10)
print(s.age)

