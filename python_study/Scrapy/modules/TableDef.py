from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Qiubai(Base):
    __tablename__ = 'qiubai'
    id = Column(Integer, primary_key=True)
    userid = Column(String(20), nullable=False)
    username = Column(String(20), nullable=False)
    funny_num = Column(Integer, nullable=False)
    content = Column(String(1024), nullable=True)
    url = Column(String(1024), nullable=True)

    def __init__(self, userid, username, funny_num, content, url):
        self.userid = userid
        self.username = username
        self.funny_num = funny_num
        self.content = content
        self.url = url