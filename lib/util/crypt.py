import os
from passlib.utils.pbkdf2 import pbkdf2


class Crypt:
    def __init__(self, rounds, keylen):
        self.rounds = rounds
        self.keylen = keylen

    def generate_salt(self, length):
        return os.urandom(length)

    def hash_password(self, password, salt):
        return pbkdf2(password.encode('utf-8'), salt, self.rounds, self.keylen)
