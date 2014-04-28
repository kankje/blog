from unittest import TestCase
from binascii import hexlify

from lib.crypt import generate_salt, hash_password


class TestCrypt(TestCase):
    def test_generate_salt(self):
        self.assertEquals(16, len(generate_salt()))

    def test_hash_password(self):
        hashed_password = hash_password('password', bytes([0] * 16))
        self.assertEquals(
            b'cae6c57cbde71ad375b2539f7ca174ba9b140f47d1c975dda1c9c955b9a7a0b2',
            hexlify(hashed_password)
        )
