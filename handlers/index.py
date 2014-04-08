from math import ceil

from handlers import BaseHandler
from models import Post


class IndexHandler(BaseHandler):
    POSTS_PER_PAGE = 5

    def get(self, page=None, *args, **kwargs):
        page = page if page else 1
        with self.application.db.session() as session:
            posts = session.query(Post).order_by(Post.creation_date).limit(5) \
                .offset((page - 1) * self.POSTS_PER_PAGE)
            page_count = ceil(session.query(Post).count() / self.POSTS_PER_PAGE)
            self.render(
                'index.jinja2',
                posts=posts,
                page=page,
                page_count=page_count
            )
