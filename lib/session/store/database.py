import datetime
import pickle

from sqlalchemy.orm.exc import NoResultFound

from models import Session


class DatabaseSessionStore:
    def __init__(self, db, session_lifetime):
        self.db = db
        self.session_lifetime = session_lifetime

    def get_session_data(self, session_id):
        with self.db.session() as db_session:
            try:
                session = db_session.query(Session).filter_by(id=session_id).one()
                if session.expiration_date < datetime.datetime.now():
                    db_session.delete(session)
                    return {}
                return pickle.loads(session.data)
            except NoResultFound:
                return {}

    def save_session_data(self, session_id, session_data):
        pickled_data = pickle.dumps(session_data if session_data else {})
        new_expiration_date = datetime.datetime.now() + datetime.timedelta(minutes=self.session_lifetime)
        with self.db.session() as db_session:
            rows_updated = db_session.query(Session).filter_by(id=session_id).update({
                'data': pickled_data,
                'expiration_date': new_expiration_date
            })
            if rows_updated == 0:
                db_session.add(Session(
                    id=session_id,
                    data=pickled_data,
                    expiration_date=new_expiration_date
                ))

    def destroy_session(self, session_id):
        with self.db.session() as db_session:
            db_session.query(Session).filter_by(id=session_id).delete()
