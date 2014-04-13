from unittest import TestCase

from lib.util import Canocalizer


class TestCanocalizer(TestCase):
    def test_canocalize(self):
        canocalizer = Canocalizer()
        self.assertEquals(
            'the-story-about-100-cats',
            canocalizer.canocalize('The story about 100 cats')
        )
