# -*- coding: utf-8 -*-

from datetime import date
from views import Index, About, Content, Contacts, CategoryList, ContentList


# front controller
def secret_front(request, **kwargs):
    request['token'] = None


def other_front(request, **kwargs):
    request['type'] = kwargs.get('env', {}).get('REQUEST_METHOD','GET')
    

def user_front(request, **kwargs):
    request['user'] = 'user' # get_user()


def page_front(request, **kwargs):
    request['active_page'] = kwargs.get('env', {}).get('PATH_INFO','/')


fronts = [secret_front, other_front, user_front, page_front]
routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/categories/': CategoryList(),
    '/content/': ContentList(),
    
}
