from unittest import TestCase
import binascii

from lib.util import Crypt


class TestCrypt(TestCase):
    def setUp(self):
        self.crypt = Crypt(2000, 32)

    def test_generate_salt(self):
        self.assertEquals(16, len(self.crypt.generate_salt(16)))

    def test_hash_password(self):
        hashed_password = self.crypt.hash_password(
            'password', bytes([0] * 16)
        )
        self.assertEquals(
            b'cae6c57cbde71ad375b2539f7ca174ba9b140f47d1c975dda1c9c955b9a7a0b2',
            binascii.hexlify(hashed_password)
        )
