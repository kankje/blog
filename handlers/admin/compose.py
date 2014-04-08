from datetime import datetime

from markdown import markdown

from handlers import BaseHandler, authenticated
from forms.admin import ComposeForm
from models import Post


class ComposeHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        BaseHandler.__init__(self, application, request, **kwargs)
        self.form = ComposeForm(self.request.arguments)

    @authenticated
    def get(self, post_id=None, *args, **kwargs):
        if post_id:
            with self.application.db.session() as session:
                post = session.query(Post).filter_by(id=post_id).one()
                self.form.id.data = post.id
                self.form.title.data = post.title
                self.form.link_text.data = post.link_text
                self.form.content.data = post.content
        self.render(
            'admin/compose.jinja2',
            form=self.form
        )

    @authenticated
    def post(self, *args, **kwargs):
        if self.form.validate():
            with self.application.db.session() as session:
                if self.form.id.data != '':
                    post = session.query(Post).filter_by(id=self.form.id.data).one()
                    post.title = self.form.title.data
                    post.link_text = self.form.link_text.data
                    post.content = self.form.content.data
                    post.content_html = markdown(self.form.content.data)
                else:
                    post = Post(
                        title=self.form.title.data,
                        link_text=self.form.link_text.data,
                        content=self.form.content.data,
                        content_html=markdown(self.form.content.data),
                        creation_date=datetime.now()
                    )
                    session.add(post)
            self.redirect('/post/' + str(post.id) + '/' + post.link_text)
            return
        self.get(*args, **kwargs)
