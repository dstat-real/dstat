# dstat plugin for MySQL 5 Commands 
# 2007-09-04 - lefred@inuits.be
global MySQLdb
import MySQLdb
global string, select
import string, select

global mysql_user
global mysql_pwd
mysql_user = os.getenv('DSTAT_MYSQL_USER') or os.getenv('USER')
mysql_pwd = os.getenv('DSTAT_MYSQL_PWD')

class dstat_mysql5_com(dstat):
    def __init__(self):
        self.name = 'mysql5 com'
        self.format = ('i', 5, 1)
        self.vars = ('Com_select', 'Com_insert','Com_update','Com_delete')
        self.nick = ('sel', 'ins','upd','del')
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
            for name in self.vars:
              c.execute("""show global status like '%s';""" % name)
              line = c.fetchone()
              if line[0] in self.vars:
                    self.cn2[line[0]] = int(line[1])

            for name in self.vars:
                self.val[name] = self.cn2[name] * 1.0 / tick

            if step == op.delay:
                self.cn1.update(self.cn2)

        except Exception, e:
            for name in self.vars:
                self.val[name] = -1

# vim:ts=4:sw=4:et
