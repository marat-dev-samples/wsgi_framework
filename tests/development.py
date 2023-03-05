# -*- coding: utf-8 -*-
"""Some tests for framework

Run this tests: python -m unittest -v tests.methods 
Notice: `Test_Init_Content` will init database and create test content,
         it may be skipped if not required.

"""
import unittest
import unittest.mock  
from unittest.mock import Mock
from unittest.mock import patch
from collections import OrderedDict, namedtuple

from patterns.creational import *
from patterns.behavioral import *
from patterns.structural import redirect
from patterns.unit_of_work import *
from patterns.mappers import *

site = Engine()


class Test_Logger(unittest.TestCase):

    def setUp(self):
        return

    def test_log_filtering(self, message='test'):                    
        """Checks the count of logger calls depending of current log_level"""
                 
        logger = BaseLogger 
        log = logger('main', 20)
        log.add_handler(StreamHandler())

        TestParams = namedtuple('TestParams', ['name', 'log_level', 'result'])
        test_cases = [                      
            TestParams('DEBUG_LEVEL', 10, 4), 
            TestParams('INFO_LEVEL', 20, 3), 
            TestParams('WARNING_LEVEL', 30, 2), 
            TestParams('CRITICAL_LEVEL', 40, 1), 
        ]
        
        for test in test_cases: 
            log.log_level = test.log_level              # Setup log level
            with patch.object(logger, 'log') as mock:
                log.debug(message)
                log.info(message)
                log.warning(message)
                log.critical(message)
                self.assertEqual(mock.call_count, test.result)
      
    def test_singleton_pattern(self):
        """Checking singleton correct pattern""" 
        logger1 = BaseLogger('log1')
        logger2 = BaseLogger('log2')
        logger3 = BaseLogger('log1')

        assert logger1 is not logger2
        assert logger1 is logger3


class Test_Redirect(unittest.TestCase):

    def setUp(self):
        return

    def test_url_params(self, message='test'):                    
        """Check correct url params concatenation of redirect method"""
        result = redirect('/contacts/')         
        self.assertEqual(result[1], '/contacts/', f'Wrong url result {result[1]}')

        result = redirect('/contacts/', param1=0, param2='alpha method')         
        self.assertEqual(result[1], '/contacts/?param1=0&param2=alpha+method', f'Wrong url result {result[1]}')


#@unittest.skip("This test is skipped temporary")
class Test_Init_Content(unittest.TestCase):


    def setUp(self):
        self.category_name = 'Raspberry Pi'
        self.content_name = 'Wireless module'
        self.author_name = 'Alexander Peers'
        self.author_id = 1
        return


    def test_1_create_user(self):                    
        """Create test content"""
        init_sqlite_database()
        UnitOfWork.new_current()
    
        # Create author 
        user = site.create_author(self.author_name)
        user.mark_new()
       
        # Create contributors
        contributors = ['Muzzy', 'Gonzo Wonzo', 'Crazy Harry', 'Fozzy Bear', 'Kermit the Frog'] 
        for contributor in contributors:
            user = site.create_user(contributor, 'contributor') 
            user.mark_new()
        
        UnitOfWork.get_current().commit()
        users = site.get_users()
        for user in users:
            print(user.name)


    def test_2_category_create(self):                    
        """Create test category"""
        category = site.create_category(self.category_name)
        site.categories.append(category)
        self.assertIsInstance(site.categories[0], Category, 'Wrong object type')
        return

    def test_3_content_create(self, category_id="0"):                    
        """Create test content"""
        
        content_type = 'html' 
        category = site.find_category_by_id(int(category_id))
        author = site.get_user_by_id(self.author_id)
        print(author.name) 

        content = site.create_content(content_type, self.content_name, category, author)
        content.add_observers((PrintNotifier(),))
        
        site.content.append(content)
        self.assertIsInstance(site.content[0], HTMLFormat, 'Wrong object type')
                
    
    def test_4_subscribe_content(self):                    
        """Subscribe content -> notify author"""

        user = site.get_user_by_id(5)
        content = site.get_content_by_name(self.content_name)
        content.contributors.append(user)
        content.notify_author()
      
        user = site.get_user_by_id(4)
        content = site.get_content_by_name(self.content_name)
        content.contributors.append(user)
        content.notify_author()
     
    # Use comment content here
    def test_5_edit_content(self, name='Test content'):                    
        """Edit test content -> notify contributors"""
        content = site.get_content_by_name(self.content_name)
        content.text = 'Edit text'
        content.notify_contributors() 


    def test_6_api_call(self, category_id="0"):
        """Iterator implementation here"""
        category = site.find_category_by_id(int(category_id))
        
        result = [content.as_dict() for content in category]
        print(result)

        return























