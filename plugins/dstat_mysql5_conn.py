# dstat plugin for MySQL 5 connections 
# 2007-09-04 - lefred@inuits.be
global MySQLdb
import MySQLdb

global mysql_user
global mysql_pwd
mysql_user = os.getenv('DSTAT_MYSQL_USER') or os.getenv('USER')
mysql_pwd = os.getenv('DSTAT_MYSQL_PWD')

class dstat_mysql5_conn(dstat):
    def __init__(self):
        self.name = 'mysql5 conn'
        self.format = ('f', 4, 1)
        self.vars = ('Threads_connected', 'Threads')
        self.nick = ('ThCon', '%Con')
        self.init(self.vars, 1)

    def check(self): 
            try:
                self.db=MySQLdb.connect(user=mysql_user, passwd=mysql_pwd)
            except:
                raise Exception, 'Cannot interface with MySQL server'
            return True

    def extract(self):
        try:
            c = self.db.cursor()
            c.execute("""show global variables like 'max_connections';""")
            max = c.fetchone()
            c.execute("""show global status like 'Threads_connected';""")
            thread = c.fetchone()
            if thread[0] in self.vars:
                    self.cn2[thread[0]] = float(thread[1])
                    self.cn2['Threads'] = (float(thread[1]) / float(max[1]) * float(100)) 

            for name in self.vars:
                self.val[name] = self.cn2[name] * 1.0 /tick

            if step == op.delay:
                self.cn1.update(self.cn2)

        except Exception, e:
            for name in self.vars:
                self.val[name] = -1

# vim:ts=4:sw=4:et
