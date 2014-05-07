from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.Binary(32))
    salt = db.Column(db.Binary(16))
    blog_name = db.Column(db.String(200))
    blog_description = db.Column(db.Text)
    blog_author = db.Column(db.String(200))
    custom_html = db.Column(db.Text)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    link_text = db.Column(db.String(200))
    content = db.Column(db.Text)
    content_html = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
