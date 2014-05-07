from datetime import datetime
from flask import Blueprint, request, session, g, render_template, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from markdown import markdown
from app.models import db, Settings, Post
from app.forms.admin import InstallForm, LoginForm, SettingsForm, ComposeForm
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
        settings = Settings.query.one()
        if settings.username == form.username.data:
            password_hash = crypt.hash_password(form.password.data, settings.salt)
            if settings.password == password_hash:
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
    form = SettingsForm()

    settings = Settings.query.one()
    form.blog_name.data = settings.blog_name
    form.blog_description.data = settings.blog_description
    form.blog_author.data = settings.blog_author

    if form.validate_on_submit():
        settings.blog_name = form.blog_name.data
        settings.blog_description = form.blog_description.data
        settings.blog_author = form.blog_author.data
        db.session.commit()
        return redirect(url_for('request.index'))

    return render_template('admin/settings.jinja2', form=form)


@admin.route('/compose', methods=['GET', 'POST'])
@admin.route('/compose/<post_id>', methods=['GET', 'POST'])
def compose(post_id=None):
    form = ComposeForm()

    if post_id:
        post = Post.query.filter_by(id=post_id).one()
        form.id.data = post.id
        form.title.data = post.title
        form.content.data = post.content

    if form.validate_on_submit():
        if form.id.data != '':
            post = Post.query.filter_by(id=form.id.data).one()
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
        Post.filter_by(id=post_id).delete()
        return redirect(url_for('regular.index'))

    return render_template(
        'admin/delete.jinja2',
        post=Post.filter_by(id=post_id).one()
    )
