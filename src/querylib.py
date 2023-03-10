# -*- coding: utf-8 -*-

"""
Collection of methods for dealing with wsgi requests 

"""
import urllib
import json

from patterns.creational import BaseLogger


log = BaseLogger('main', 20)


def retrieve_post_params(environ):
    content = int(environ.get('CONTENT_LENGTH', 0))        
    if content == 0:
        return {}
        
    query = environ.get('wsgi.input').read()     # This action will empty input
    query_str = query.decode(encoding='utf-8')
        
    # Decode param values
    params = urllib.parse.parse_qs(query_str)
    result = {key: val[0] for key, val in params.items()}

    # Support of PUT, PATCH, DELETE for standard html forms
    if "_method" in result:
        result['type'] = result.get("_method").upper() 

    """
    Additional param handlers here...
    """    
    

    log.info(f'[>] POST params: {json.dumps(result, ensure_ascii=False, indent=4)}')
    return result


def retrieve_get_params(environ):
    query_str = environ.get('QUERY_STRING')
    params = urllib.parse.parse_qs(query_str)
    result = {key: val[0] for key, val in params.items()}
   
    """
    Implement additional params handler here
    """
    #log.info(f'[>] GET params: {json.dumps(result, ensure_ascii=False, indent=4)}')
    





    return result


def parse_query_string(query_str): 
    """Deprecated"""
    return dict(param.split('=') for param in query_str.split('&') if param)
