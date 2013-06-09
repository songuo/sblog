import sys
import types

from settings import PROJECT_NAME

# default: PROJECT_NAME = 'sblog'
if PROJECT_NAME not in sys.modules:
    project  = types.ModuleType(PROJECT_NAME)
    project.settings = __import__('settings')
    sys.modules[PROJECT_NAME] = project
    sys.modules[PROJECT_NAME + '.settings'] = project.settings

from main.views import app
from bottle import route, run, default_app

# Create database tables
#from main.models import sync
#sync()

default_app.push(app)

@route('/test')
def haha():
    return '<h2>Hello World!</h2>'

run(host = '127.0.0.1', port = '8000')
# run(app, host = '127.0.0.1', port = '8000')
