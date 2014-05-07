from unittest import TestCase
from lib.canocalize import canocalize


class TestCanocalize(TestCase):
    def test_canocalization(self):
        self.assertEquals('this-is-a-title-bam', canocalize('This is -- a_title - bam!'))
