
class Session:
    def __init__(self, store, session_id):
        self.store = store
        self.id = session_id
        self.data = store.get_session_data(session_id)

    def save(self):
        self.store.save_session_data(self.id, self.data)

    def destroy(self):
        self.data = {}
        self.store.destroy_session(self.id)

    def __getitem__(self, item):
        return self.data[item] if item in self.data else None

    def __setitem__(self, key, value):
        self.data[key] = value
