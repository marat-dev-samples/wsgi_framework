# -*- coding: utf-8 -*-

"""
Gunicorn also provides integration for Django and Paste Deploy applications.
Gunicorn will look for a WSGI callable named application if not specified. 
So for a typical Django project, invoking Gunicorn would look like:
gunicorn custom_framework.wsgi

"""
from urls import routes, fronts
from src.custom_framework import CustomFramework
from urls import routes, fronts

'''
def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World 1!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
'''

def get_wsgi_application():
    app = CustomFramework(routes, fronts)
    return app


def run():
    app = CustomFramework(routes, fronts)
    return app


application = get_wsgi_application()

