from unittest import TestCase

from lib import canocalize


class TestCanocalize(TestCase):
    def test_canocalization(self):
        self.assertEquals(
            'this-is-a-title',
            canocalize('This is a -- title')
        )
