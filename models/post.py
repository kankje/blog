from sqlalchemy import Column, Integer, String, Text, DateTime

from models import Base


class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    link_text = Column(String(200))
    content = Column(Text)
    content_html = Column(Text)
    creation_date = Column(DateTime)
