import os

from flask import Flask, request, g, render_template, redirect, url_for
from flask.ext.assets import Environment, Bundle

from app import config
from app.models import db, Settings
from app.redis import redis
from app.views.regular import regular
from app.views.admin import admin
from lib.jinja2.htmlcompress import HtmlCompress
from lib.session import RedisSessionInterface


app = Flask(
    __name__,
    static_folder='public',
    template_folder=os.path.join('app', 'templates')
)
app.debug = config.debug
app.secret_key = config.cookie_secret

# Jinja2 plugins
app.jinja_env.add_extension(HtmlCompress)

# Assets
assets = Environment(app)
assets.url = app.static_url_path
css = Bundle(
    '../assets/css/main.scss',
    filters=['pyscss', 'cssmin'],
    output='main.css'
)
assets.register('css', css)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}'.format(
        config.db_user,
        config.db_password,
        config.db_host,
        config.db_port,
        config.db_name
    )
db.init_app(app)

# Sessions
app.session_interface = RedisSessionInterface(redis)

# Views
app.register_blueprint(regular)
app.register_blueprint(admin)


@app.errorhandler(404)
def not_found():
    return render_template('error/404.jinja2'), 404


@app.errorhandler(500)
def not_found():
    return render_template('error/500.jinja2'), 500


@app.before_request
def before_request():
    if request.endpoint == 'static':
        return
    if request.endpoint != 'admin.install':
        if not db.engine.dialect.has_table(db.engine.connect(), 'settings'):
            return redirect(url_for('admin.install'))
        g.settings = Settings.query.one()


if __name__ == '__main__':
    app.run()
