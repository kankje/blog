import os
import binascii
import functools

from tornado.web import RequestHandler, HTTPError

from lib.session import DummySessionStore, Session


class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        RequestHandler.__init__(self, application, request, **kwargs)
        self._session = None

    def prepare(self):
        if self.application.admin_settings is None and not type(self) != 'InstallHandler':
            self.redirect('/install')

    def on_finish(self):
        if self._session:
            self._session.save()

    @property
    def session(self):
        if self._session:
            return self._session
        if self.application.admin_settings is None:
            return Session(DummySessionStore(), None)

        session_id = self.get_secure_cookie('sid')
        if session_id is None:
            session_id = binascii.hexlify(os.urandom(16)).decode('ascii')
            self.set_secure_cookie('sid', session_id)
        else:
            session_id = session_id.decode('ascii')

        self._session = Session(self.application.session_store, session_id)
        return self._session

    def render(self, template_name, **kwargs):
        self.write(
            self.application.renderer.render(
                template_name,
                logged_in=self.session['logged_in'] is not None,
                xsrf_token=self.xsrf_form_html(),
                **kwargs
            )
        )

    def redirect(self, url, permanent=False, status=None):
        RequestHandler.redirect(
            self,
            self.application.config.subdir + url,
            permanent,
            status
        )


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.session['logged_in']:
            if self.request.method in ('GET', 'HEAD'):
                self.redirect(self.get_login_url())
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper
