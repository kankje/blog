import os
from passlib.utils.pbkdf2 import pbkdf2


def generate_salt():
    return os.urandom(16)


def hash_password(password, salt):
    return pbkdf2(password.encode('utf-8'), salt, 2000, 32)
