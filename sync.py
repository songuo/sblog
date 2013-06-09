#! /usr/bin/env python

import sys, types
from settings import PROJECT_NAME

# default: PROJECT_NAME = 'sblog'
if PROJECT_NAME not in sys.modules:
    project  = types.ModuleType(PROJECT_NAME)
    project.settings = __import__('settings')
    sys.modules[PROJECT_NAME] = project
    sys.modules[PROJECT_NAME + '.settings'] = project.settings

from main.models import sync

sync()
