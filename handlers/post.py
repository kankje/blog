from handlers import BaseHandler
from models import Post


class PostHandler(BaseHandler):
    def get(self, post_id, link_text=None, *args, **kwargs):
        with self.application.db.session() as session:
            post = session.query(Post).filter_by(id=post_id).one()
        self.render('post.jinja2', post=post)
