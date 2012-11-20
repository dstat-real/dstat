### Author: <lefred@inuits.be>

global mysql_user
mysql_user = os.getenv('DSTAT_MYSQL_USER') or os.getenv('USER')

global mysql_pwd
mysql_pwd = os.getenv('DSTAT_MYSQL_PWD')

class dstat_plugin(dstat):
    """
    Plugin for MySQL 5 commands.
    """
    def __init__(self):
        self.name = 'mysql5 cmds'
        self.nick = ('sel', 'ins','upd','del')
        self.vars = ('Com_select', 'Com_insert','Com_update','Com_delete')
        self.type = 'd'
        self.width = 5
        self.scale = 1

    def check(self): 
        global MySQLdb
        import MySQLdb
        try:
            self.db = MySQLdb.connect(user=mysql_user, passwd=mysql_pwd)
        except Exception, e:
            raise Exception, 'Cannot interface with MySQL server: %s' % e

    def extract(self):
        try:
            c = self.db.cursor()
            for name in self.vars:
                c.execute("""show global status like '%s';""" % name)
                line = c.fetchone()
                if line[0] in self.vars:
                    if line[0] + 'raw' in self.set2:
                        self.set2[line[0]] = long(line[1]) - self.set2[line[0] + 'raw']
                    self.set2[line[0] + 'raw'] = long(line[1])

            for name in self.vars:
                self.val[name] = self.set2[name] * 1.0 / elapsed

            if step == op.delay:
                self.set1.update(self.set2)

        except Exception, e:
            for name in self.vars:
                self.val[name] = -1

# vim:ts=4:sw=4:et
