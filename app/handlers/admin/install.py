from app.handlers import BaseHandler
from app.forms.admin import InstallForm
from app.models import Base, Settings


class InstallHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.form = InstallForm(self.request.arguments)
        self.install_error = None

    def get(self, *args, **kwargs):
        self.render(
            'admin/install.jinja2',
            form=self.form,
            install_error=self.install_error
        )

    def post(self, *args, **kwargs):
        if self.form.validate():
            try:
                with self.application.db.session() as session:
                    Base.metadata.create_all(self.application.db.engine)

                    salt = self.application.crypt.generate_salt(16)
                    session.add(Settings(
                        username=self.form.username.data,
                        password=self.application.crypt.hash_password(
                            self.form.password.data,
                            salt
                        ),
                        salt=salt,
                        blog_name=self.form.blog_name.data,
                        blog_description=self.form.blog_description.data,
                        blog_author=self.form.blog_author.data
                    ))

                self.application.reload_admin_settings()
                self.redirect('/')
                return
            except Exception as exc:
                self.install_error = str(exc)

        self.get(*args, **kwargs)
