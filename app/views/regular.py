from math import ceil
from flask import Blueprint, render_template
from app.models import Post


regular = Blueprint('regular', __name__, url_prefix='/')


@regular.route('/page/<page_num>')
def page(page_num):
    posts_per_page = 5
    page_num = max(1, int(page_num)) if page_num else 1
    page_count = max(
        1,
        ceil(Post.query.count() / posts_per_page)
    )
    page_num = min(page_count, page_num)
    posts = Post.query.order_by(Post.creation_date.desc()).limit(5) \
        .offset((page_num - 1) * posts_per_page)
    return render_template(
        'index.jinja2',
        posts=posts,
        page=page,
        page_count=page_count
    )


@regular.route('/')
def index():
    return page(1)


@regular.route('/post/<post_id>/<link_text>')
def post(post_id, link_text=None):
    return render_template('post.jinja2', post=Post.query.filter_by(id=post_id).one())
