import threading
import MySQLdb


class Singleton():
    instance = None
    conn     = None
    host     = None
    user     = None
    passwd   = None
    db       = None
    mutex=threading.Lock()

    def _init__(self):
        pass
    @staticmethod
    def getInstance():
        if(Singleton.instance == None):
            Singleton.mutex.acquire()
            if(Singleton.instance == None):
                Singleton.instance = Singleton()
            Singleton.mutex.release()
        return Singleton.instance
    #获取数据库连接
    def getConnection(self):
        try:
            if (conn == None):
                conn = MySQLdb.connect(self.host, self.user, self.passwd, self.db, 'utf8')
                return conn.cursor()
            else:
                return conn.cursor()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def setConnection(host, user, passwd, db):
        self.host   = host
        self.user   = user
        self.passwd = passwd
        self.db     = db

    def closeConnection(self):
        try:
            if (self.conn != None):
                self.conn.cursor.close()
                self.conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == 'main':
    Singleton.setConnection(localhost, root, 123456, python)