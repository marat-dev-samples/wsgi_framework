from src.templator import render, j2render


class Index:
    def __call__(self, request):
        return '200 OK', render('base.html', **request)
        #return j2render('index.html', date=request.get('date', None))

class About:
    def __call__(self, request):
        return '200 OK', 'about'


class Content:
    def __call__(self, request):
        return '200 OK', render('content.html', **request)
        #return j2render('index.html', date=request.get('date', None))

class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', **request)
        #return j2render('index.html', date=request.get('date', None))
