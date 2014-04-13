from unittest import TestCase
from unittest.mock import MagicMock

from lib.session import Session


class TestSession(TestCase):
    def setUp(self):
        self.store_mock = MagicMock()
        self.store_mock.get_session_data.return_value = {}

    def test_get(self):
        self.store_mock.get_session_data.return_value = {
            'key_1': 'a',
            'key_2': 'b'
        }
        session = Session(self.store_mock, 'test_session_id')
        self.assertEquals('a', session['key_1'])
        self.assertEquals('b', session['key_2'])

    def test_set(self):
        session = Session(self.store_mock, 'test_session_id')
        session['key_1'] = 'a'
        session['key_2'] = 'b'
        session.save()
        self.store_mock.save_session_data.assert_called_once_with(
            'test_session_id',
            {
                'key_1': 'a',
                'key_2': 'b'
            }
        )

    def test_destroy(self):
        session = Session(self.store_mock, 'test_session_id')
        session.destroy()
        self.assertEquals({}, session.data)
        self.store_mock.destroy_session.assert_called_once_with('test_session_id')
