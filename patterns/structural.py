import time
import urllib.parse


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class AppRouter():
    """Experimental application hash router"""

    routes = {} 

    def __init__(self, *args):
        self.url = args[0] if args else '/' 
    
    def __call__(self, cls):
        self.routes[self.url] = cls()

    @classmethod
    def route(cls, url, request):
        """Calling of url specified handler"""
        inst = cls.routes.get(url, PageNotFound404())
        return inst(request)


def debug(func):                                                           
    def wrapper_debug(*args, **kwargs):
        """Debug decorator, simple print func name in console"""
        start = time.time() 
        result = func(*args, **kwargs) 
        t = "{0:f}".format(time.time() - start)
        print(f'[DEBUG] {func} timeit: {t}s')
        return result     
    return wrapper_debug


def redirect(url, **kwargs):
    if kwargs:
       url = f'{url}?{urllib.parse.urlencode(kwargs)}' 
    return 302, url


