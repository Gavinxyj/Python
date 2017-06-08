import threading
import MySQLdb
from logConfig.LoggingConfig import logger

class Singleton(object):
    instance = None
    conn = None
    host = None
    user = None
    passwd = None
    db = None
    port = None
    mutex = threading.Lock()

    def _init__(self):
        pass

    @staticmethod
    def get_instance():
        if Singleton.instance is None:
            Singleton.mutex.acquire()
            if Singleton.instance is None:
                Singleton.instance = Singleton()
            Singleton.mutex.release()
        return Singleton.instance

    # get db connection
    def get_connection(self):
        try:
            if self.conn is None:
                self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd, db=self.db, charset='utf8')
                logger.debug(self.conn)
                return self.conn.cursor()
            else:
                return self.conn.cursor()
        except MySQLdb.Error, e:
            logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def set_connection(self, host, port, user, passwd, db):
        self.host = host
        self.user = user
        self.port = port
        self.passwd = passwd
        self.db = db

    def close_connection(self):
        try:
            if self.conn is not None:
                self.conn.cursor.close()
                self.conn.close()
        except MySQLdb.Error, e:
            logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

if __name__ == '__main__':
    Singleton.get_instance().set_connection('localhost', 3306, 'root', '123456', 'python')
    Singleton.get_instance().get_connection()
