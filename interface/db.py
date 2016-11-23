#-*-coding=utf-8 -*-

import MySQLdb  

def connectmysql(host,sql):
    if host == str(59):
        host = '192.168.60.59'
        port = 5200
        user = 'root'
        password = ''
        db = 'lsh_ofc'
    if host == str(48):
        host = '192.168.60.48'
        port = 5201
        user = 'root'
        password = 'root123'
        db = 'lsh_oms'
    
    connect = MySQLdb.connect(host=host, port=port, user=user, passwd=password, db=db, charset="utf8")
    Cursor = connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    Cursor.execute(sql)
    data = Cursor.fetchall()
    return data     
if __name__ == '__main__':
    sql = "select b.order_code as result from order_head b where b.order_status in('91','93') and b.order_code not in (select order_code from order_aftersales ) limit 1;"
    data = connectmysql('48',sql)
    for i in data:
        print i['result']
    