from urlparse import urlparse
import os

class MongoConfig(object):
    MONGO_URI = os.environ.get("MONGOLAB_URI")
