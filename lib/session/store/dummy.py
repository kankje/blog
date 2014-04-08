
class DummySessionStore:
    def __init__(self):
        pass

    def get_session_data(self, session_id):
        return {}

    def save_session_data(self, session_id, data):
        pass

    def destroy_session(self, session_id):
        pass
