import pymysql


class MySQLImpl(object):
    """docstring for MySQLImpl"""
    def __init__(self):
        super(MySQLImpl, self).__init__()
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='test', charset='utf8')
        
        try:
            create_table = '''CREATE TABLE IF NOT EXISTS QIUBAI
                              (ID   INT(11) NOT NULL AUTO_INCREMENT,
                               USERID   VARCHAR(20) NOT NULL,
                               USERNAME VARCHAR(20) NOT NULL,
                               FUNNY_NUM INT NOT NULL,
                               CONTENT VARCHAR(1024),
                               URL VARCHAR(256),
                               PRIMARY KEY (ID))ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
                               AUTO_INCREMENT=1;
                            '''
                            
            self._cursor = self.conn.cursor()
            self._cursor.execute(create_table)
            self.conn.commit()


        except Exception as e:
            raise e

    def insert_record(self, infos):
        try:
            sql = 'INSERT INTO QIUBAI(USERID, USERNAME, FUNNY_NUM, CONTENT, URL) VALUES(%s, %s, %s, %s, %s)'
            self._cursor = self.conn.cursor()
            # for info in infos:
            self._cursor.executemany(sql, infos)
            self.conn.commit()
            self._cursor.close()
        except Exception as e:
            # self.conn.rollback()
            raise e
        

    def delete_record(self):
        pass

    def dump(self):
        try:
            self._cursor = self.conn.cursor()
            sql = 'SELECT * FROM QIUBAI'
            self._cursor.execute(sql)
            self._cursor.close()
            ret = self._cursor.fetchall()
            print(len(ret))
        except Exception as e:
            raise e

    def update_record(self):
        pass