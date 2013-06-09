# -*- coding: utf-8 -*-

import os
import datetime
from contextlib import contextmanager
from functools import wraps

from bottle import request
from jinja2 import Environment, FileSystemLoader

from models import Tag, session

from sblog.settings import (BLOG_TITLE,
                            STATIC_FILE_VERSION,
                            GITHUB_LINK,
                           )


__all__ = ['jinja_view', 'key_verified', 'session_context']

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(CURRENT_PATH)
TEMPLATES_PATH = os.path.join(PROJECT_PATH, 'templates')
KEY_PATH = os.path.join(CURRENT_PATH, '_key')

env = Environment(loader = FileSystemLoader(TEMPLATES_PATH))

def format_date(value, f="%b %d, %Y"):
    return datetime.datetime.strftime(value, f)

env.filters['format_date'] = format_date


'''
It provides utilities for common tasks involving the with statement
'''
@contextmanager
def session_context():
    try:
        yield session
    except Exception:
        raise
    finally:
        session.close()



def blog_context():
    data = {
        'blog_title': BLOG_TITLE,
        'title': BLOG_TITLE,
        'ver': STATIC_FILE_VERSION,
        'github_link': GITHUB_LINK
    }
    
    # TODO cache the tags
    with session_context() as session:
        data['tags'] = session.query(Tag).order_by(Tag.name.asc())
    
    return data
    


def jinja_view(tpl, **kwargs):
    _kwargs = kwargs
    
    def deco(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            
            data = blog_context()
            data.update(_kwargs)
            data.update(result)
            
            template = env.get_template(tpl)
            return template.render(**data)
        return wrapper
    return deco        
        

def key_verified(key):
    with open(KEY_PATH, 'r') as f:
        data = f.read()
        
    data = data.strip('\n')
    key = key.strip('\n')
    return key == data


