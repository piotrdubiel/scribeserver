from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.security import MongoEngineUserDatastore
from flask.ext.admin import Admin
from tornado.wsgi import WSGIContainer
from tornado.web import Application, FallbackHandler
from admin import CustomAdminIndexView

from .users import User, Role, blueprint as users_module, security
from .users.admin import UserView
from .recognition import Prediction, blueprint as recognition_module
from .recognition.admin import PredictionView

app = Flask(__name__)
app.config.from_object("config.MongoConfig")
app.config.from_object("config.SecurityConfig")
app.config["SECRET_KEY"] = "567633992e92e96c8a61f5e1ec62ba5550a9e95b4e2899a00112ebcd7585b1a9"

app.register_blueprint(users_module)
app.register_blueprint(recognition_module)

db = MongoEngine(app)
user_store = MongoEngineUserDatastore(db, User, Role)
security.init_app(app, user_store)

admin = Admin(app, index_view=CustomAdminIndexView())
admin.add_view(UserView(User))
admin.add_view(PredictionView(Prediction))

from recognition import ws

container = WSGIContainer(app)
server = Application([
    (r'/ws/recognize', ws.SocketHandler),
    (r'.*', FallbackHandler, dict(fallback=container))
])
