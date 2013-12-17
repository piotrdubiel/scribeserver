import os

from config.defaults import *

if os.environ.get("ENV") == 'dev':
    print("==== Loading DEV environment ====")
    from config.local import *
else:
    print("==== Loading HERKOU environment ====")
    from config.heroku import *
