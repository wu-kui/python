#!/usr/bin/python
# coding: utf-8

from pymemcache.client.base import Client
import MySQLdb, time

log = '/var/log/flush_memcache.log'

try:
    db = MySQLdb.connect(host='192.168.1.10', port=3306, user='reader', passwd='reader', db='mybase', charset='gbk')
    cursor = db.cursor()
    cursor.execute('select ip from zdy_ip_zl;')
    data = cursor.fetchall()
    with open(log,'a') as f:
        f.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'  get ip!~~\n')
except:
    with open(log,'a') as f:
        f.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'  connection mysql fail!\n')
finally:
    if db:
        db.close()
    if cursor:
        cursor.close()


try:
    if data:
        mc = Client(('192.168.1.11', 11211))
        mc.flush_all()
        for i in data:
            if i[0][0:2] == 'zh':
                mc.set(i[0],1)
                #print i[0]
            else:
                mc.set('zh'+i[0],1)
                #print 'zh' + i[0]
except:
    with open(log,'a') as f:
        f.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))+'  connection memcache fail!\n')
finally:
    if mc:
        mc.close()
