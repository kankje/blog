from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:
    def __init__(self, connection_string):
        self._engine = create_engine(connection_string)
        self._connection = self._engine.connect()
        self._sessionmaker = sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    @property
    def engine(self):
        return self._engine

    @property
    def connection(self):
        return self._connection

    def create_session(self):
        return self._sessionmaker()

    @contextmanager
    def session(self):
        session = self._sessionmaker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
