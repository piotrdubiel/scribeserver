from flask.ext.admin import AdminIndexView, expose
from flask.ext import login
from flask import url_for, redirect


class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not login.current_user.is_authenticated():
            return redirect('/login')
        return super(CustomAdminIndexView, self).index()

#    @expose('/login/', methods=('GET', 'POST'))
#    def login_view(self):
#        # handle user login
#        form = LoginForm(request.form)
#        if helpers.validate_form_on_submit(form):
#            user = form.get_user()
#            login.login_user(user)
#
#        if login.current_user.is_authenticated():
#            return redirect(url_for('.index'))
#        link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
#        self._template_args['form'] = form
#        self._template_args['link'] = link
#        return super(MyAdminIndexView, self).index()
#
#    @expose('/register/', methods=('GET', 'POST'))
#    def register_view(self):
#        form = RegistrationForm(request.form)
#        if helpers.validate_form_on_submit(form):
#            user = User()
#
#            form.populate_obj(user)
#
#            db.session.add(user)
#            db.session.commit()
#
#            login.login_user(user)
#            return redirect(url_for('.index'))
#        link = '<p>Already have an account? <a href="' + url_for('.login_view') + '">Click here to log in.</a></p>'
#        self._template_args['form'] = form
#        self._template_args['link'] = link
#        return super(MyAdminIndexView, self).index()
