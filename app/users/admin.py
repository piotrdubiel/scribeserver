from flask.ext.admin.contrib.mongoengine import ModelView
from app.management.mixins import AdminMixin


class UserView(AdminMixin, ModelView):
    column_filters = ['email']

    column_searchable_list = ('email', 'password')

    form_ajax_refs = {
        'roles': {
            'fields': ('name', 'description')
        }
    }


class RoleView(AdminMixin, ModelView):
    column_filters = ['name']

    column_searchable_list = ('name',)
