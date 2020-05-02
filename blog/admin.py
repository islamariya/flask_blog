from blog_app import app, session

from flask import redirect, request, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

import models


class AdminMixin():
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login", next=request.url))


class MyModelView(AdminMixin, ModelView):
    pass


class MyAdminIndexView(AdminMixin, AdminIndexView):
    pass


admin = Admin(app, "Админ панель", url="/", index_view=MyAdminIndexView())

admin.add_view(MyModelView(models.PostsCategory, session))
admin.add_view(MyModelView(models.Posts, session))
admin.add_view(MyModelView(models.Tags, session))
admin.add_view(MyModelView(models.User, session))
