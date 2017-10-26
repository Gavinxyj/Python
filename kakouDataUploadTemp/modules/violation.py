import cx_Oracle
import logging
from database.Connection import Connection
logger = logging.getLogger("kakou.modules")

class Violation(object):
	
    _querySql = "select hpzl, filepath1, filepath1, filepath2 from fndj.veh_violation where  sbbh like '147%' and jgsj > to_date('2017-09-07 06:00:00', 'yyyy-mm-dd hh24:mi:ss') and jgsj < to_date('2017-09-08 14:00:00', 'yyyy-mm-dd hh24:mi:ss')"

    @staticmethod
    def get_all_record():
        try:
            conn = Connection.get_conn('yushi')
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(Violation._querySql)
                result = cursor.fetchall()
                cursor.close()
                return result
        except cx_Oracle.Error, e:
            conn.close()
            logger.error('Oracle Error: %d %s' % (e.args[0], e.args[1]))