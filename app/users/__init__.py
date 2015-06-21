from flask.ext.security import Security
from .models import *
from .decorators import api_authorize, view_authorize
from .views import blueprint

security = Security()
