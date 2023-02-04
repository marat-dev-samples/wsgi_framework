# -*- coding: utf-8 -*-

from datetime import date
from views import Index, About


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'

def user_front(request):
    request['user'] = 'user' # get_user()


fronts = [secret_front, other_front, user_front]
routes = {
    '/': Index(),
    '/about/': About(),
}
