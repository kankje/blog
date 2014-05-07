from datetime import datetime
from flask import Blueprint, request, session, g, render_template, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from markdown import markdown
from app.models import db, Settings, Post
from app.forms.admin import InstallForm, LoginForm, BlogSettingsForm, \
    UserSettingsForm, ComposeForm
from lib import crypt
from lib.canocalize import canocalize

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.before_request
def before_request():
    if 'logged_in' not in session and request.endpoint != 'admin.login' \
            and request.endpoint != 'admin.install':
        return redirect(url_for('admin.login'))


@admin.route('/install', methods=['GET', 'POST'])
def install():
    if db.engine.dialect.has_table(db.engine.connect(), 'settings'):
        return redirect(url_for('regular.index'))

    g.settings = {
        'blog_name': 'Installation',
        'blog_description': ''
    }
    form = InstallForm()
    error = None

    if form.validate_on_submit():
        try:
            db.create_all()

            salt = crypt.generate_salt()
            db.session.add(Settings(
                username=form.username.data,
                password=crypt.hash_password(form.password.data, salt),
                salt=salt,
                blog_name=form.blog_name.data,
                blog_description=form.blog_description.data,
                blog_author=form.blog_author.data
            ))
            db.session.commit()

            return redirect(url_for('regular.index'))
        except SQLAlchemyError as exc:
            db.session.rollback()
            error = str(exc)

    return render_template('admin/install.jinja2', form=form, error=error)


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('regular.index'))

    login_failed = False
    form = LoginForm()
    if form.validate_on_submit():
        login_failed = True
        s = Settings.query.one()
        if s.username == form.username.data:
            password_hash = crypt.hash_password(form.password.data, s.salt)
            if s.password == password_hash:
                session['logged_in'] = True
                return redirect(url_for('regular.index'))

    return render_template(
        'admin/login.jinja2',
        form=form,
        login_failed=login_failed
    )


@admin.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('regular.index'))


@admin.route('/settings', methods=['GET', 'POST'])
def settings():
    s = Settings.query.one()
    saved = False

    blog_form = BlogSettingsForm(prefix='blog')
    blog_form.blog_name.data = s.blog_name
    blog_form.blog_description.data = s.blog_description
    blog_form.blog_author.data = s.blog_author
    blog_form.custom_html.data = s.custom_html

    user_form = UserSettingsForm(prefix='user')
    user_form.username.data = s.username

    if 'blog-submit' in request.form and blog_form.validate_on_submit():
        s.blog_name = blog_form.blog_name.data
        s.blog_description = blog_form.blog_description.data
        s.blog_author = blog_form.blog_author.data
        s.custom_html = blog_form.custom_html.data
        db.session.commit()
        saved = True

    if 'user-submit' in request.form and user_form.validate_on_submit():
        salt = crypt.generate_salt()
        s.username = user_form.username.data
        s.password = crypt.hash_password(user_form.password.data, salt)
        s.salt = salt
        db.session.commit()
        saved = True

    return render_template(
        'admin/settings.jinja2',
        blog_form=blog_form,
        user_form=user_form,
        saved=saved
    )


@admin.route('/compose', methods=['GET', 'POST'])
@admin.route('/compose/<post_id>', methods=['GET', 'POST'])
def compose(post_id=None):
    post = None
    if post_id:
        post = Post.query.get_or_404(post_id)
    form = ComposeForm(obj=post)

    if form.validate_on_submit():
        if post:
            post.title = form.title.data
            post.link_text = canocalize(
                form.title.data
            )
            post.content = form.content.data
            post.content_html = markdown(form.content.data)
        else:
            post = Post(
                title=form.title.data,
                link_text=canocalize(form.title.data),
                content=form.content.data,
                content_html=markdown(form.content.data),
                creation_date=datetime.now()
            )
            db.session.add(post)
        db.session.commit()
        return redirect(url_for(
            'regular.post',
            post_id=post.id,
            link_text=post.link_text
        ))

    return render_template('admin/compose.jinja2', form=form)


@admin.route('/delete/<post_id>')
@admin.route('/delete/<post_id>/confirm/<confirm>')
def delete(post_id, confirm=None):
    if confirm == 'yes':
        Post.query.filter_by(id=post_id).delete()
        return redirect(url_for('regular.index'))

    return render_template(
        'admin/delete.jinja2',
        post=Post.query.get_or_404(post_id)
    )
