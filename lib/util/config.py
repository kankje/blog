import os
import configparser


class Config:
    def __init__(self, root_path, config_filename):
        self.root_path = root_path
        self.config_filename = config_filename

        parser = configparser.RawConfigParser()
        parser.read_file(open(os.path.join(self.root_path, self.config_filename)))

        self.app_ip = parser.get('app', 'ip', fallback='127.0.0.1')
        self.app_port = parser.get('app', 'port')
        self.debug = parser.getboolean('app', 'debug')
        self.cookie_secret = parser.get('app', 'cookie_secret')
        self.subdir = parser.get('app', 'subdir', fallback='')
        self.subdir = '/' + self.subdir if self.subdir != '' else ''

        self.db_type = parser.get('database', 'type')
        self.db_host = parser.get('database', 'host')
        self.db_port = parser.getint('database', 'port')
        self.db_username = parser.get('database', 'username')
        self.db_password = parser.get('database', 'password')
        self.db_database = parser.get('database', 'database')
