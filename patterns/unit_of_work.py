from threading import local


class RegistryHolder(type):
    
    registry = []

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        cls.registry.append(new_cls)
        return new_cls 

    @classmethod
    def get_mapper_for(cls, obj_name):
        for item in cls.registry:
            if hasattr(item, 'mapper_for') and obj_name in item.mapper_for:
                return item
        raise Exception(f'No mapper registered for : {obj.__class__}')


# Deprecate this
# архитектурный системный паттерн - Data Mapper
'''
class MapperRegistry:
    mappers = {
        #'student': StudentMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)

'''

class UnitOfWork:
    """Unit of work implementation"""
    
    current = local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    '''
    def set_mapper_registry(self, MapperRegistry):
        self.MapperRegistry = MapperRegistry
    '''

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

        self.new_objects.clear()
        self.dirty_objects.clear()
        self.removed_objects.clear()

    def insert_new(self):
        for obj in self.new_objects:
            mapper = RegistryHolder.get_mapper_for(obj.__class__.__name__) 
            mapper().insert(obj) 
            
    def update_dirty(self):
        for obj in self.dirty_objects:
            mapper = RegistryHolder.get_mapper_for(obj.__class__.__name__) 
            mapper().update(obj) 
            
    def delete_removed(self):
        for obj in self.removed_objects:
            mapper = RegistryHolder.get_mapper_for(obj.__class__.__name__) 
            mapper().delete(obj) 
            
    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)




















