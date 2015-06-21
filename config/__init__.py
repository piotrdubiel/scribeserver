import os

from config.defaults import *

if os.environ.get("ENV") == 'dev':
    print("==== Loading DEV environment ====")
    from config.local import *
elif os.environ.get("ENV") == 'docker':
    print("==== Loading Docker environment ====")
    from config.docker import *
else:
    print("==== Loading HERKOU environment ====")
    from config.heroku import *
