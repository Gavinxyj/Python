#!/usr/bin/python
# -*- coding:utf-8 -*-
# @author   youjiang xie
# @E-mail   xie_youjiang@163.com
# @time     2017/7/6 0006 13:47
# @project  Python
# @file     test
import cx_Oracle
def OperationToString(operation):
    operations = []
    if operation & cx_Oracle.OPCODE_INSERT:
        operations.append("insert")
    if operation & cx_Oracle.OPCODE_DELETE:
        operations.append("delete")
    if operation & cx_Oracle.OPCODE_UPDATE:
        operations.append("update")
    if operation & cx_Oracle.OPCODE_ALTER:
        operations.append("alter")
    if operation & cx_Oracle.OPCODE_DROP:
        operations.append("drop")
    if operation & cx_Oracle.OPCODE_ALLOPS:
        operations.append("all operations")
    return ", ".join(operations)

def OnChanges(message):
    print "Message received"
    print "    Database Name:", message.dbname
    print "    Tables:"
    for table in message.tables:
        print "        Name:", table.name,
        print "        Operations:",
        print OperationToString(table.operation)
        if table.rows is None \
                or table.operation & cx_Oracle.OPCODE_ALLROWS:
            print "        Rows: all rows"
        else:
            print "        Rows:"
            for row in table.rows:
                print "            Rowid:", row.rowid
                print "            Operation:",
                print OperationToString(row.operation)

connection = cx_Oracle.Connection("IVMS86X0/IVMS86X0@192.168.88.59/ORCL", events=True)
sql = 'select pass_id, crossing_id from TRAFFIC_VEHICLE_PASS'
# subscriptionAll = connection.subscribe(callback=OnChanges)
# subscriptionAll.registerquery(sql)
subscriptionInsertUpdate = \
        connection.subscribe(callback = OnChanges,
        operations = cx_Oracle.OPCODE_INSERT | \
        cx_Oracle.OPCODE_UPDATE, rowids=True)
subscriptionInsertUpdate.registerquery(sql)

raw_input("Hit enter to terminate...\n")
