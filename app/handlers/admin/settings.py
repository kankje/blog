from app.handlers import BaseHandler, authenticated
from app.forms.admin import SettingsForm
from app.models import Settings


class SettingsHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.form = SettingsForm(self.request.arguments)

    @authenticated
    def get(self, *args, **kwargs):
        with self.application.db.session() as session:
            settings = session.query(Settings).one()
            self.form.blog_name.data = settings.blog_name
            self.form.blog_description.data = settings.blog_description
            self.form.blog_author.data = settings.blog_author
        self.render('admin/settings.jinja2', form=self.form)

    @authenticated
    def post(self, *args, **kwargs):
        if self.form.validate():
            with self.application.db.session() as session:
                settings = session.query(Settings).one()
                settings.blog_name = self.form.blog_name.data
                settings.blog_description = self.form.blog_description.data
                settings.blog_author = self.form.blog_author.data
            self.application.reload_admin_settings()
            self.redirect('/')
            return
        self.get(*args, **kwargs)
