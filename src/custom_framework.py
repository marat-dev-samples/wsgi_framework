# -*- coding: utf-8 -*-

import src.querylib as querylib

from patterns.structural import *


'''
class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
'''

class CustomFramework:

    def __init__(self, routes_obj=None, fronts_obj=None):
        self.routes_lst = routes_obj or {}
        self.fronts_lst = fronts_obj or {}


    def __call__(self, environ, start_response):
        
        # Filter path
        path = environ['PATH_INFO']
        if not path.endswith('/'):
            path = f'{path}/'
        
        # Check query params
        request = {}

        """
        Wsgi environment variables
         'REQUEST_METHOD': 'GET', 
         'QUERY_STRING': 'a=1&b=2', 'RAW_URI': '/?a=1&b=2', 
         'SERVER_PROTOCOL': 'HTTP/1.1', 
         'HTTP_HOST': '127.0.0.1:8000', 
         'RAW_URI': '/?a=1&b=2',
         'HTTP_CONNECTION': 'keep-alive', 
         'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
         'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br',
         'PATH_INFO': '/', 
        """
        request_type = environ.get('REQUEST_METHOD') 
        if request_type == 'GET':
            request['data'] = querylib.retrieve_get_params(environ)
        if request_type  == 'POST':
            request['data'] = querylib.retrieve_post_params(environ)

        




        # Page controller pattern, search for corresponding page 'view' or 404
        #view = self.routes_lst.get(path, PageNotFound404())

        # Front controller pattern handler 
        for front in self.fronts_lst:
            front(request, env=environ)
        
        # Getting response, run page 'view' with passing query params
        #code, body = view(request)
         
        
        


        code, body = AppRouter.route(path, request)
        
        # Redirect response 
        if code in [301, 302, 303]:
            start_response('302 Found', [('Location', body)])
            return [bytes('', 'utf-8')] 
        

        # Return response 
        start_response(code, [('Content-Type', 'text/html')])
        return [bytes(body, 'utf-8')]


    

















