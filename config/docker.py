import os


class MongoConfig(object):
    MONGODB_DB = 'dev'
    MONGODB_HOST = os.environ.get('MONGO_PORT_27017_TCP_ADDR')
    MONGODB_PORT = os.environ.get('MONGO_PORT_27017_TCP_PORT')
