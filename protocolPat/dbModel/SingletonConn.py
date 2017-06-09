import threading
import MySQLdb
from logConfig.LoggingConfig import logger


class Singleton(object):
    _instance = None
    _conn = None
    _host = None
    _user = None
    _passwd = None
    _db = None
    _port = None
    mutex = threading.Lock()

    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        if Singleton._instance is None:
            Singleton.mutex.acquire()
            if Singleton._instance is None:
                Singleton._instance = Singleton()
            Singleton.mutex.release()
        return Singleton._instance

    # get db connection
    def get_connection(self):
        try:
            if self._conn is None:
                self._conn = MySQLdb.connect(host=self._host, port=self._port, user=self._user, passwd=self._passwd, db=self._db, charset='utf8')
                logger.debug(self._conn)
                return self._conn.cursor()
            else:
                return self._conn.cursor()
        except MySQLdb.Error, e:
            logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def set_connection(self, host, port, user, passwd, db):
        self._host = host
        self._user = user
        self._port = port
        self._passwd = passwd
        self._db = db

    def close_connection(self):
        try:
            if self._conn is not None:
                self._conn.cursor.close()
                self._conn.close()
        except MySQLdb.Error, e:
            logger.error("Mysql Error %d: %s" % (e.args[0], e.args[1]))

if __name__ == '__main__':
    # print 'hello world'
    # Singleton.setConnection('localhost', 'root', 123456, 'python')
    obj = Singleton()
    # Singleton.get_instance().set_connection('localhost', 3306, 'root', 'root', 'gjxms')
    # Singleton.get_instance().get_connection()
    obj.set_connection('localhost', 3306, 'root', 'root', 'gjxms')
    obj.get_connection()
