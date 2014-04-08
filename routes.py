from tornado.web import StaticFileHandler

from handlers import IndexHandler, PostHandler, NotFoundHandler
from handlers.admin import InstallHandler, LoginHandler, LogoutHandler, \
    SettingsHandler, ComposeHandler


def get_routes(asset_path):
    return [
        (r'/', IndexHandler),
        (r'/page/(\d+)', IndexHandler),
        (r'^/post/(\d+)(/+[a-zA-Z0-9-]*)?$', PostHandler),

        # Admin
        (r'/login', LoginHandler),
        (r'/logout', LogoutHandler),
        (r'/settings', SettingsHandler),
        (r'/compose', ComposeHandler),
        (r'/compose/(\d+)', ComposeHandler),
        (r'/install', InstallHandler),

        # Static file serving through the app is supported, but not recommended
        (r'/assets/(.*)', StaticFileHandler, {'path': asset_path}),

        # A catch-all 404 handler
        (r'/(.*)', NotFoundHandler)
    ]
