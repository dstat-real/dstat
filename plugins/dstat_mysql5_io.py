### Author: <lefred$inuits,be>

global mysql_user
mysql_user = os.getenv('DSTAT_MYSQL_USER') or os.getenv('USER')

global mysql_pwd
mysql_pwd = os.getenv('DSTAT_MYSQL_PWD')

global mysql_host
mysql_host = os.getenv('DSTAT_MYSQL_HOST')

global mysql_port
mysql_port = os.getenv('DSTAT_MYSQL_PORT')

global mysql_socket
mysql_socket = os.getenv('DSTAT_MYSQL_SOCKET')

class dstat_plugin(dstat):
    """
    Plugin for MySQL 5 I/O.
    """

    def __init__(self):
        self.name = 'mysql5 io'
        self.nick = ('recv', 'sent')
        self.vars = ('Bytes_received', 'Bytes_sent')

    def check(self): 
        global MySQLdb
        import MySQLdb
        try:
            args = {}
            if mysql_user:
                args['user'] = mysql_user
            if mysql_pwd:
                args['passwd'] = mysql_pwd
            if mysql_host:
                args['host'] = mysql_host
            if mysql_port:
                args['port'] = mysql_port
            if mysql_socket:
                args['unix_socket'] = mysql_socket

            self.db = MySQLdb.connect(**args)
        except:
            raise Exception('Cannot interface with MySQL server')

    def extract(self):
        try:
            c = self.db.cursor()
            c.execute("""show global status like 'Bytes_%';""")
            lines = c.fetchall()
            for line in lines:
                if len(line[1]) < 2: continue
                if line[0] in self.vars:
                    if line[0] + 'raw' in self.set2:
                        self.set2[line[0]] = float(line[1]) - self.set2[line[0] + 'raw']
                    self.set2[line[0] + 'raw'] = float(line[1])

            for name in self.vars:
                self.val[name] = self.set2[name] * 1.0 / elapsed

            if step == op.delay:
                self.set1.update(self.set2)

        except Exception as e:
            for name in self.vars:
                self.val[name] = -1

# vim:ts=4:sw=4:et
