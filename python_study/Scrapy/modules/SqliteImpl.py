import sqlite3

class SqliteImpl(object):
    """docstring for SqliteImpl"""
    def __init__(self):
        super(SqliteImpl, self).__init__()
        try:
            self.conn = sqlite3.connect('sqlite.db')
            create_table = '''CREATE TABLE IF NOT EXISTS QIUBAI
                              (ID INT NOT NULL,
                               USERID   TEXT NOT NULL,
                               USERNAME TEXT NOT NULL,
                               FUNNY_NUM INT NOT NULL,
                               CONTENT TEXT,
                               URL TEXT);
                            '''
            self._cursor = self.conn.cursor()
            self._cursor.execute(create_table)
            self.conn.commit()
        except Exception as e:
            raise e
        

    def insert_record(self, infos):
        try:
            sql = 'INSERT INTO QIUBAI(USERID, USERNAME, FUNNY_NUM, CONTENT, URL) VALUES(?, ?, ?, ?, ?)'
           
            #for info in infos:
            self._cursor.executemany(sql, infos)
            self.conn.commit()
            self._cursor.close()
        except Exception as e:
            self.conn.rollback()
            raise e
        

    def delete_record(self):
        pass

    def dump(self):
        try:
            sql = 'SELECT * FROM QIUBAI'
            
            self._cursor.execute(sql)
            self._cursor.close()
            ret = _cursor.fetchall()
            print(len(ret))
        except Exception as e:
            raise e

    def update_record(self):
        pass
