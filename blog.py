import os
from flask import Flask, request, g, render_template, redirect, url_for
from flask.ext.assets import Environment, Bundle
from app import config
from app.models import db, Settings
from app.redis import redis
from app.views.regular import regular
from app.views.admin import admin
from lib.session import RedisSessionInterface

app = Flask(
    __name__,
    static_folder='public',
    static_url_path=config.url_prefix + '/public',
    template_folder=os.path.join('app', 'templates')
)
app.debug = config.debug
app.secret_key = config.cookie_secret

# Jinja2 extensions
app.jinja_env.filters['nl2br'] = lambda value: value.replace('\n', '<br>')
app.jinja_env.add_extension('compressinja.html.HtmlCompressor')

# Assets
assets = Environment(app)
assets.url = app.static_url_path
css = Bundle(
    '../assets/style.scss',
    filters=['pyscss', 'cssmin'],
    output='style.css'
)
assets.register('css', css)

# View
app.register_blueprint(regular, url_prefix=config.url_prefix)
app.register_blueprint(admin, url_prefix=config.url_prefix)

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


@app.errorhandler(404)
def not_found(e):
    return render_template('error/404.jinja2'), 404


@app.errorhandler(500)
def not_found(e):
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
