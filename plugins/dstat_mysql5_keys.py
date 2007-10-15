# dstat plugin for MySQL 5 Keys 
# 2007-09-04 - lefred@inuits.be
global MySQLdb
import MySQLdb
global string, select
import string, select

global mysql_user
global mysql_pwd
mysql_user = os.getenv('DSTAT_MYSQL_USER') or os.getenv('USER')
mysql_pwd = os.getenv('DSTAT_MYSQL_PWD') 

class dstat_mysql5_keys(dstat):
    def __init__(self):
        self.name = 'mysql5 key status'
        self.format = ('f', 4, 1000)
        self.vars = ('Key_blocks_used', 'Key_reads', 'Key_writes', 'Key_read_requests', 'Key_write_requests')
        self.nick = ('used', 'read', 'writ', 'rreq', 'wreq')
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
            c.execute("""show global status like 'Key_%';""")
            lines = c.fetchall()
            for line in lines:
                if len(line[1]) < 2: continue
                if line[0] in self.vars:
                    self.cn2[line[0]] = float(line[1])

            for name in self.vars:
                self.val[name] = self.cn2[name] * 1.0 / tick

            if step == op.delay:
                self.cn1.update(self.cn2)

        except Exception, e:
            for name in self.vars:
                self.val[name] = -1

# vim:ts=4:sw=4:et
