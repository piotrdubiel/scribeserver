from urlparse import urlparse
import os


class MongoConfig(object):
    uri = urlparse(os.environ.get("MONGOLAB_URI"))
    MONGODB_DB = uri.path.lstrip('/')
    MONGODB_USERNAME = uri.username
    MONGODB_PASSWORD = uri.password
    MONGODB_HOST = os.environ.get("MONGOLAB_URI")
    MONGODB_PORT = uri.port
