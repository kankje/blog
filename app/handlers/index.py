from math import ceil

from app.handlers import BaseHandler
from app.models import Post


class IndexHandler(BaseHandler):
    POSTS_PER_PAGE = 5

    def get(self, page=None, *args, **kwargs):
        page = max(1, int(page)) if page else 1
        with self.application.db.session() as session:
            page_count = max(
                1,
                ceil(session.query(Post).count() / self.POSTS_PER_PAGE)
            )
            page = min(page_count, page)
            posts = session.query(Post).order_by(Post.creation_date.desc()).limit(5) \
                .offset((page - 1) * self.POSTS_PER_PAGE)
            self.render(
                'index.jinja2',
                posts=posts,
                page=page,
                page_count=page_count
            )