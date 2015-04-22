from flask.ext.login import current_user


class AdminMixin():
    def is_accessible(self):
        return current_user.is_authenticated()
