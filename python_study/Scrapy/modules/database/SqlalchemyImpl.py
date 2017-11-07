from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
from .TableDef import Base, Qiubai

class SqlalchemyImpl(object):
    """docstring for SqlalchemyImpl"""
    def __init__(self):
        engine = create_engine('sqlite:///qiubai.db', convert_unicode=True, echo=False)   
        #engine = create_engine('mysql+pymysql://root:root@localhost/test?charset=utf8', convert_unicode=True, echo=True)   

        self.db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
        # Base.session = self.db_session
        Base.metadata.create_all(engine)

    def insert_record(self, items):
        session = self.db_session()
        try:
            for item in items:
                #obj = Qiubai(item[0], item[1], item[2], item[3], item[4])
                obj = Qiubai(items)
                #list_record.append(obj)
                session.add(obj)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e

    def delete_record(self):
        try:
            session = self.db_session()
            session.delete(Qiubai)
            session.commit()
        except Exception as e:
            raise e

    def dump_record(self):
        try:
            session = self.db_session()
            ret = session.query(Qiubai).all()
            print(ret)
        except Exception as e:
            raise e

    def update_reocrd(self):
        try:
            session = self.db_session()
            session.query(Qiubai).filter(Qiubai.userid=='/users/33096359/').update({Qiubai.funny_num:500})
            session.commit()
        except Exception as e:
            raise e