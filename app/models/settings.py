from sqlalchemy import Column, Integer, String, Binary, Text

from app.models import Base


class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    username = Column(String(200))
    password = Column(Binary(32))
    salt = Column(Binary(16))
    blog_name = Column(String(200))
    blog_description = Column(Text())
    blog_author = Column(String(200))
