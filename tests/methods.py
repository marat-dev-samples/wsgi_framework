# -*- coding: utf-8 -*-
"""Some tests for framework

Run this tests: python -m unittest -v tests.methods

"""
import unittest
import unittest.mock  
from unittest.mock import Mock
from unittest.mock import patch
from collections import OrderedDict, namedtuple

from patterns.creational import *


#@unittest.skip("Logger test is skipped temporary")
class Test_Custom_Logger(unittest.TestCase):

    def setUp(self):
        return

    def test_log_filtering(self, message='test'):                    
        """Checks a number of log method calls depending of current log_level"""
        
        logger = FileLogger #BaseLogger
        log = logger('log1', log_level=10)
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






