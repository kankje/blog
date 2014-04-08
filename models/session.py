from sqlalchemy import Column, String, Binary, DateTime

from models import Base


class Session(Base):
    __tablename__ = 'session'

    id = Column(String(32), primary_key=True)
    data = Column(Binary)
    expiration_date = Column(DateTime)
