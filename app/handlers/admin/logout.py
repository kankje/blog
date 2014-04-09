from app.handlers import BaseHandler, authenticated


class LogoutHandler(BaseHandler):
    @authenticated
    def get(self, *args, **kwargs):
        self.session.destroy()
        self.redirect('/')
