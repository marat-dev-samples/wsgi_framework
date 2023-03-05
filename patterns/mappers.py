import sqlite3
from patterns.unit_of_work import RegistryHolder
from patterns.creational import User, Contributor, BaseLogger

logger = BaseLogger('main', 20)
DB_CONFIG = {'db_name': 'framework.db'}        


def init_sqlite_database():
    """Creates if not exists data table for quote symbol""" 
    conn = sqlite3.connect(DB_CONFIG['db_name'])
    cursor = conn.cursor()
    
    # Clear users table
    str_sql = "DROP TABLE users"
    cursor.execute(str_sql)

    # Create users table     
    str_sql = '''create table if not exists users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
                    name VARCHAR (32),
                    is_author BOOLEAN);'''
    cursor.execute(str_sql)
    
    conn.commit()
    cursor.close() 
    conn.close()


class UserMapper(metaclass=RegistryHolder):

    mapper_for = ['User', 'Contributor', 'Author']
    
    def __init__(self):
        self.db = DB_CONFIG.get('db_name')
        self.connection = sqlite3.connect(self.db)
        self.cursor = self.connection.cursor()
        self.tablename = 'users'

    def all(self):
        statement = f'SELECT id, name, is_author from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            user = User(*item)
            result.append(user)
        return result

    def find_authors(self, id):
        statement = f'SELECT id, name, is_author from {self.tablename} WHERE is_author=true'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            user = User(*item)
            result.append(user)
        return result 


    def find_by_id(self, id):
        statement = f"SELECT id, name, is_author FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return User(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name, is_author) VALUES(?, ?)"
        self.cursor.execute(statement, (obj.name, obj.is_author))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)
        logger.info(f'> Insert user: {obj.name}')

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

