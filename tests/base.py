from unittest import TestCase


class BaseTest(TestCase):
    def setUp(self):
        self.setup()

    def tearDown(self):
        self.teardown()

    def setup(self):
        pass

    def teardown(self):
        pass
