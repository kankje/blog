from app.handlers import BaseHandler


class NotFoundHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.set_status(404)
        self.render('notfound.jinja2')
