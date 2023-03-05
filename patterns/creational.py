from copy import deepcopy
import os
from patterns.behavioral import Subject
from patterns.unit_of_work import DomainObject, RegistryHolder

# Users definition
class User(DomainObject):
    def __init__(self, id, name, is_author=False):
        self.id = id
        self.name = name
        self.is_author = is_author


class Author(User):
    """The creator of any useful content"""
    def __init__(self, name):
        super().__init__(None, name)
        self.is_author = True


class Contributor(User):
    """The contributor of content"""
    def __init__(self, name):
        super().__init__(None, name)


class UserFactory:
    types = {
        'autor': Author,
        'contributor': Contributor
    }
 
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)
    
    @classmethod
    def create_author(cls, name): 
        return Author(name) 


# Prototype pattern definition
class DataPrototype:
    # Common prototype pattern

    def clone(self):
        return deepcopy(self)


# Content (articles) definition
class Content(DataPrototype, Subject):

    def __init__(self, name, category, type_, author: object):
        self.name = name
        self.author = author     # string - user name 
        self.contributors = []
        self.category = category
        self.category.articles.append(self)
        self.type = type_
        self.text = ''
        super().__init__()


    def articles_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result
    
    def as_dict(self):
        return {
            'name': self.name, 
            'author': self.author.name, 
            'type': self.type, 
            'contributors': [user.name for user in self.contributors]}


class WebinarFormat(Content):
    """Additional dimensions here excepts content
       - data time of beginning
       - url 
    """
    pass


class HTMLFormat(Content):
    pass


class PDFFormat(Content):
    pass


class PrintableVersion(Content):
    pass


class ContentFactory:
    types = {
        'webinar': WebinarFormat,
        'html': HTMLFormat,
        'print': PrintableVersion,
        'pdf': PDFFormat
    }

    @classmethod
    def create(cls, content_type, name, category, author):
        return cls.types[content_type](name, category, content_type, author)


# Categories definition
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category   # Object here ???
        self.articles = []
        self._index = 0            # Itetation index

    def articles_count(self):
        result = len(self.articles)
        
        if self.category:
            result += self.category.articles_count()    # ???
        return result

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self.articles):
            item = self.articles[self._index]
            self._index += 1
            return item
        else:
            raise StopIteration


# Main site engine definition
class Engine:
    def __init__(self):
        #self.users = []
        self.content = []
        self.categories = []
    
    @staticmethod
    def create_user(name, type_):
        return UserFactory.create(type_, name)
    
    @staticmethod
    def create_author(name):
        return UserFactory.create_author(name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    @staticmethod
    def create_content(type_, name, category, author):
        return ContentFactory.create(type_, name, category, author)

    @staticmethod
    def content_types():
        return list(ContentFactory.types.keys())
    
    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'No category id: {id}')

    def get_content_by_name(self, name):
        for item in self.content:
            if item.name == name:
                return item
        return None

    def get_user_by_name(self, name) -> User:
        for item in self.users:
            if item.name == name:
                return item
        raise Exception(f'No user with name: {name}')
    
    def get_user_by_id(self, _id) -> User:
        mapper = RegistryHolder.get_mapper_for('User')  
        return mapper().find_by_id(_id)
           

 
    def get_authors(self):
        mapper = RegistryHolder.get_mapper_for('User')  
        return mapper().find_authors()

    def get_users(self):
        mapper = RegistryHolder.get_mapper_for('User')  
        return mapper().all()
        



    #@staticmethod
    #def decode_value(val):
    #    val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
    #    val_decode_str = decodestring(val_b)
    #    return val_decode_str.decode('UTF-8')


# Singleton pattern definition
# https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
class NamedSingleton(type):
    """Metaclass based singleton pattern"""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        name = args[0] if args else __name__
        if name not in cls._instances:
            cls._instances[name] = super().__call__(*args, **kwargs)
        return cls._instances[name]


class BaseLogger(metaclass=NamedSingleton):

    log_methods = {'debug': 10, 'info': 20, 'warning': 30, 'critical': 40}
    
    def __init__(self, name, log_level=10):
        self.name = name
        self.log_level = log_level 
        self.handlers = []
    
    def __getattr__(self, attr):
        """Handles calling method (`debug`, `info`, `warning` or `critical`)"""
        message_level = self.log_methods.get(attr, None)
        if message_level:
            if message_level >= self.log_level:
                return self.log
            else:
                return self.skip
        # Default behavior
        return self.__getattribute__(attr)

    def add_handler(self, obj):
        self.handlers.append(obj)
  
    def log(self, message):
        """Base method for logging - utilize internal mehtods (handlers)"""
        message = f'[log]: {message}'
        for handler in self.handlers:
            handler(message)
        return
  
    def skip(self, message):
        return


class StreamHandler():
    """Provides strem output of logger message"""
    
    def __init__(self):
        return

    def __call__(self, message):
        print(f'{message}')
        

class FileHandler():
    """Provides file storing of logger messages"""
    
    def __init__(self, file_name=None):
        self._file_name = file_name or f'{__name__}.log'
        self.log_dir = os.path.dirname(__file__)
        self.log_file = os.path.join(self.log_dir, self._file_name)

    def __call__(self, message):
        with open(self.log_file, "a") as f:
            f.write(f'{message}\n')
        









