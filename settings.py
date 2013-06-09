# -*- coding: utf-8 -*-

import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

"""If you change the name, you must do 2 things:
1. change the directory name of the blog
2. change main.models, main.utils, main.views import
"""
PROJECT_NAME = 'sblog'
DEBUG = True

if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (
        MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
    )
else:
    # Make `python manage.py syncdb` works happy!
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = '3306'
    MYSQL_USER = 'songuo'
    MYSQL_PASS = 'admin'
    MYSQL_DB   = 'test'

MYSQL = {
    'HOST': MYSQL_HOST,
    'PORT': int(MYSQL_PORT),
    'DBNAME': MYSQL_DB,
    'USER': MYSQL_USER,
    'PASSWORD': MYSQL_PASS,
}

BLOG_TITLE = "Guo Song"
GITHUB_LINK = "https://github.com/songuo"



# Static files, (css, js, image, etc.)
# If your changed static file, then change the value
# due to static file are cached by client browser
STATIC_FILE_VERSION = 1

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = '/static/'

# TIME_DELTA for timezone.
# Example, If server's timezone is ahead your local 5 hours
# set TIME_DELTA = -5

TIME_DELTA = 0

