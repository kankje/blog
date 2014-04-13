from app.handlers import BaseHandler, authenticated
from app.models import Post


class DeleteHandler(BaseHandler):
    @authenticated
    def get(self, post_id, confirm=None, *args, **kwargs):
        with self.application.db.session() as session:
            post = session.query(Post).filter_by(id=post_id).one()
            if confirm == 'yes':
                session.query(Post).filter_by(id=post_id).delete()
                self.redirect('/')
                return
        self.render(
            'admin/delete.jinja2',
            post=post
        )
