import threading
import MySQLdb
from logConfig import logger


class Singleton(object):
    instance = None
    conn     = None
    host     = None
    user     = None
    passwd   = None
    db       = None
    port		 = None
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
    #get db connection
    def getConnection(self):
        try:
            if (self.conn == None):
                self.conn = MySQLdb.connect(host=self.host ,port=self.port,user=self.user,passwd=self.passwd,db=self.db,charset='utf8')
                logger.debug(self.conn)
                return self.conn.cursor()
            else:
                return self.conn.cursor()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    def setConnection(self, host, port, user, passwd, db):
        self.host   = host
        self.user   = user
        self.port   = port
        self.passwd = passwd
        self.db     = db

    def closeConnection(self):
        try:
            if (self.conn != None):
                self.conn.cursor.close()
                self.conn.close()
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])

if __name__ == '__main__':
    #print 'hello world'
    #Singleton.setConnection('localhost', 'root', 123456, 'python')
    Singleton.getInstance().setConnection('localhost', 3306, 'root', '123456', 'python')
    Singleton.getInstance().getConnection()
    Singleton.getInstance().getConnection()
