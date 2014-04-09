from app.handlers import BaseHandler
from app.models import Settings
from app.forms.admin import LoginForm


class LoginHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.login_failed = False
        self.form = LoginForm(self.request.arguments)

    def get(self, *args, **kwargs):
        if self.session['logged_in']:
            self.redirect('/')
            return
        self.render(
            'admin/login.jinja2',
            form=self.form,
            login_failed=self.login_failed
        )

    def post(self, *args, **kwargs):
        if self.form.validate():
            with self.application.db.session() as session:
                settings = session.query(Settings).one()
                if settings.username != self.form.username.data:
                    self.login_failed = True

                if not self.login_failed:
                    password_hash = self.application.crypt.hash_password(
                        self.form.password.data,
                        settings.salt
                    )
                    if settings.password != password_hash:
                        self.login_failed = True

                if not self.login_failed:
                    self.session['logged_in'] = True
                    self.redirect('/')
                    return

        self.get(*args, **kwargs)
