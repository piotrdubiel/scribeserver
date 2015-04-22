from functools import wraps
from flask.ext.security import Security
from flask.ext.security import login_required, auth_token_required, http_auth_required

security = Security()


api_authorize = auth_token_required
http_authorize = http_auth_required
view_authorize = login_required
