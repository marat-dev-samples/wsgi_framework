from src.templator import render, j2render
from patterns.creational import *


logger = FileLogger('views', 20)
site = Engine()



new_category = site.create_category('Raspberry pi', 'random')
site.categories.append(new_category)
new_category = site.create_category('Arduino', 'random')
site.categories.append(new_category)



class Index:
    def __call__(self, request):
        return '200 OK', render('base.html', **request)
        #return j2render('index.html', date=request.get('date', None))

class About:
    def __call__(self, request):
        return '200 OK', 'about'

'''
class Content:
    def __call__(self, request):
        return '200 OK', render('content.html', **request)
        #return j2render('index.html', date=request.get('date', None))
'''

class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', **request)
        #return j2render('index.html', date=request.get('date', None))



# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
    
        if request['type'] == 'POST':

            name = request.get('theme_name')
            if name:
                category = 'random'
                new_category = site.create_category(name, category)
                site.categories.append(new_category)

        logger.info('Список категорий')
        return '200 OK', render('categories.html', 
                                objects_list=site.categories, **request)


# List content controller
class ContentList:
    def __call__(self, request):
        data = request.get('data')
        category_id = data.get('category_id')   
        category_name = ""        
        objects_list = []
                 
        # Handle POST request for new content creation 
        if request['type'] == 'POST':
            category_id = data.get('category_id')   
            name = data.get('name')   
            content_type = data.get('type')   
            try: 
                category = site.find_category_by_id(int(category_id))
                new_content = site.create_content(content_type, name, category)
                site.content.append(new_content)
            except Exception as e:
                logger.warning(f'{e}:name {name} category_id {category_id} content_type {content_type}')

        # If category defined - return posts from category or all posts otherways
        category_id = data.get('category_id')   
        if category_id:
            category = site.find_category_by_id(int(category_id))
            objects_list = category.articles      
            category_name = category.name
       
        return '200 OK', render('content_list.html', objects_list=objects_list, 
                                categories_list=site.categories, content_types=site.content_types(),
                                category_name=category_name, **request)
        

