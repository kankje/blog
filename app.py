import os

import tornado.web
import tornado.ioloop
from sqlalchemy.exc import SQLAlchemyError

from lib.util import Config, Crypt, Canocalizer
from lib.database import Database
from lib.session import DatabaseSessionStore
from lib.web import TemplateRenderer
from app.config import get_routes
from app.models import Settings


class Application(tornado.web.Application):
    def __init__(self):
        # "Global" services
        self.config = Config(
            os.path.dirname(os.path.abspath(__file__)),
            os.path.join('app', 'config', 'app.ini')
        )
        self.crypt = Crypt(2000, 32)
        self.db = Database(
            '{0}://{1}:{2}@{3}:{4}/{5}'.format(
                'postgresql+psycopg2' if self.config.db_type == 'postgresql' else 'mysql+pymysql',
                self.config.db_username,
                self.config.db_password,
                self.config.db_host,
                self.config.db_port,
                self.config.db_database
            )
        )
        self.session_store = DatabaseSessionStore(self.db, 120)
        self.renderer = TemplateRenderer(os.path.join(self.config.root_path, 'app', 'templates'))
        self.renderer.set_globals(
            subdir=self.config.subdir,
            link=lambda *args: self.config.subdir + ''.join(str(arg) for arg in args)
        )
        self.canocalizer = Canocalizer()

        self.admin_settings = None
        self.reload_admin_settings()

        tornado.web.Application.__init__(
            self,
            get_routes(
                self.config.subdir,
                os.path.join(self.config.root_path, 'assets')
            ),
            debug=self.config.debug,
            xsrf_cookies=True,
            cookie_secret=self.config.cookie_secret,
            login_url='/login'
        )

    def reload_admin_settings(self):
        with self.db.session() as session:
            try:
                self.admin_settings = session.query(Settings).one()
                self.renderer.set_globals(
                    blog_name=self.admin_settings.blog_name,
                    blog_description=self.admin_settings.blog_description,
                    blog_author=self.admin_settings.blog_author
                )
            except SQLAlchemyError:
                self.renderer.set_globals(
                    blog_name='blog',
                    blog_description='Installation',
                    blog_author=''
                )


if __name__ == '__main__':
    app = Application()
    app.listen(app.config.app_port, app.config.app_ip)
    print('Application started')
    tornado.ioloop.IOLoop.instance().start()
