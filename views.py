from src.templator import render, j2render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None))
        #return j2render('index.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', 'about'

