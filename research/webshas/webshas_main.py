# -*- coding: utf-8 -*-
# import sys
import sys
import os
import django
from sources.local_settings import *


sys.path.insert(0, SEFARIA_PROJECT_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = "sefaria.settings"


django.setup()

from sefaria.model import *

print("worked")