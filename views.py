from src.templator import render, j2render
import json
from patterns.creational import *
from patterns.structural import AppRouter, debug, redirect
from patterns.behavioral import PrintNotifier, ApiListView, CreateView
from patterns.unit_of_work import UnitOfWork
from patterns.mappers import *

# Setup logger
logger = BaseLogger('main', 20)
logger.add_handler(FileHandler(file_name='base.log'))
logger.add_handler(StreamHandler())

# Define main site engine
site = Engine()

# Init sample data
new_category = site.create_category('Raspberry pi')
site.categories.append(new_category)
new_category = site.create_category('Arduino')
site.categories.append(new_category)


@AppRouter('/')
class Index:
    @debug
    def __call__(self, request):
        return '200 OK', render('base.html', **request)


@AppRouter('/api/category/')
class ApiCategoryList(ApiListView):
    
    def get_queryset(self):
        data = self.request.get('data')
        category_id = data.get('category_id')   
        category = site.find_category_by_id(int(category_id))
        return [content.as_dict() for content in category]


@AppRouter('/contacts/')
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', **request)


@AppRouter('/categories/')
class CategoryList:

    def __call__(self, request):
        return '200', render('categories.html', 
                            categories_list=site.categories, **request)


@AppRouter('/create-category/')
class CreateCategory(CreateView):
    
    redirect = '/categories/' 

    def create_obj(self):
        data = self.request.get('data')
        name = data.get('theme_name')
        parent_category = data.get('category_name')
        new_category = site.create_category(name, parent_category)
        logger.info(f'> Create new category {new_category}')
        site.categories.append(new_category)


@AppRouter('/content/')
class ContentList:
    
    def __call__(self, request):
        data = request.get('data')
        category_id = data.get('category_id')   
        name = data.get('name')   
        text = data.get('content_text')
        webpush = data.get('webpush')
        category = None 
        content = None                 
       
        # Return list of articles (content) for current category
        category_id = data.get('category_id')   
        if category_id:
            category = site.find_category_by_id(int(category_id))
        
        # If content name is defined - find content by name and return
        if name:
            content = site.get_content_by_name(name)       
       
        return '200 OK', render('content_list.html',  
                                categories_list=site.categories, 
                                content_types=site.content_types(),
                                category=category, content=content,
                                users=site.get_users(), webpush=webpush, **request)


@AppRouter('/edit-content/')
class EditContent:
    
    def __call__(self, request):
        data = request.get('data')
        name = data.get('name')   
        text = data.get('content_text')
        try:
            content = site.get_content_by_name(name)       
            content.text = text
            webpush = 'Notify subscribers' 
        except Exception as e:
            logger.warning(f'Failed to patch content: {name} \n {e}')
            webpush = 'Failed to edit content, see error log for detail'

        return redirect('/content/', name=name, webpush=webpush)


@AppRouter('/create-content/')
class CreateContent:
    
    def __call__(self, request):
        data = request.get('data')
        category_id = data.get('category_id')   
        name = data.get('name')   
        text = data.get('content_text')
        mapper = RegistryHolder.get_mapper_for('User')  
        content_type = data.get('type')   
        try: 
            author = site.get_user_by_id(data.get('author'))
            category = site.find_category_by_id(int(category_id))
            new_content = site.create_content(content_type, name, category, author)
            new_content.add_observers((PrintNotifier(),))
            site.content.append(new_content)
        except Exception as e:
            logger.warning(f'{e}:name {name} category_id {category_id} content_type {content_type}')

        return redirect('/content/', category_id=category_id, webpush='Content created')


@AppRouter('/subscribe-content/')
class SubscribeContent:
    
    def __call__(self, request):
        data = request.get('data')
        user_name = data.get('user_name')   
        content_name = data.get('content_name')   
        text = data.get('content_text')
        mapper = RegistryHolder.get_mapper_for('User')  
            

        # Handle POST request for new content creation 
        content_type = data.get('type')   
        try: 
            user = site.get_user_by_id(data.get('user_name'))
            content = site.get_content_by_name(content_name)
            content.contributors.append(user)
            content.notify_author()
            webpush = 'User subscribed, notify author' 
        except Exception as e:
            logger.warning(f'{e}:name {content_name} category_id {category_id} content_type {content_type}')
            webpush = 'Failed to subscribe user, see log for details' 
        return redirect('/content/', name=content_name, webpush=webpush)


@AppRouter('/users/')
class UsersList:
    
    def __call__(self, request):
        return '200 OK', render('users.html', users=site.get_users(), **request)
        

@AppRouter('/create-user/')
class CreateUser(CreateView):
    
    redirect = '/users/' 

    def create_obj(self):
        data = self.request.get('data')
        name = data.get('name')   
        is_author = data.get('is_author', False)
        if is_author:
            user = site.create_author(name)
        else:  
            user = site.create_user(name, 'contributor') 
        UnitOfWork.new_current()
        user.mark_new()
        UnitOfWork.get_current().commit()
