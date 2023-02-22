#from abc import ABCMeta, abstractmethod
from copy import deepcopy
from quopri import decodestring
import os



# User definition
class User:
    pass


class Teacher(User):
    pass


class Author(User):
    pass


class Contributor(User):
    pass


class Admin(User):
    pass


# Fabric method definition
class UserFactory:
    types = {
        'autor': Author,
        'contributor': Contributor
    }
 
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()
    
    @classmethod
    def create_admin(cls): 
        return Admin() 


# Prototype pattern definition
class DataPrototype:
    # Common prototype pattern

    def clone(self):
        return deepcopy(self)


# Content (articles) definition
class Content(DataPrototype):

    def __init__(self, name, category, type_=None):
        self.name = name
        self.category = category
        self.category.articles.append(self)
        self.type = type_

    def articles_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


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
    def create(cls, content_type, name, category):
        return cls.types[content_type](name, category, content_type)


# Categories definition
class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.articles = []

    def articles_count(self):
        result = len(self.articles)
        
        if self.category:
            result += self.category.articles_count()    # ???
        return result


# Main site engine definition
class Engine:
    def __init__(self):
        self.authors = []
        self.contributors = []
        self.content = []
        self.categories = []
    
    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    
    @staticmethod
    def create_admin(type_):
        return UserFactory.create_admin(type_)


    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)


    # ???
    def find_category_by_id(self, id):
        print(self.categories)
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'No category id: {id}')


    @staticmethod
    def create_content(type_, name, category):
        return ContentFactory.create(type_, name, category)


    def get_content(self, name):
        for item in self.courses:
            if item.name == name:
                return item
        return None

    @staticmethod
    def content_types():
        return list(ContentFactory.types.keys())
    


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
    
    def __init__(self, name, log_level=10, **kwargs):
        self.name = name
        self.log_level = log_level 
        self.handlers = []

    def __getattr__(self, attr):
        """Handles calling of logging method (`attr` is `debug` `info` or `warning`)"""
        message_level = self.log_methods.get(attr, None)
        if message_level:
            if message_level >= self.log_level:
                return self.log
            else:
                return self.skip
        # Default behavior
        return self.__getattribute__(attr)

    def log(self, message):
        """Base method for logging - utilize internal mehtods (handlers)"""
        print(message)
        '''
        for method in self.handlers:
            self.method(message)
        '''
        return

    def stream_handler(): 
        return

    def file_handler():
        return

    def skip(self, message):
        return


class FileLogger(BaseLogger):

    def __init__(self, *args, file_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._file_name = file_name or f'{__name__}.log'
        self.log_dir = os.path.dirname(__file__)
        self.log_file = os.path.join(self.log_dir, self._file_name)
        

    def log(self, message):
        print(f'{message}')
        with open(self.log_file, "a") as f:
            f.write(f'{message}\n')
          









