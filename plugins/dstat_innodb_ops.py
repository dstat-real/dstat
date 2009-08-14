global mysql_options
mysql_options = os.getenv('DSTAT_MYSQL')

class dstat_innodb_ops(dstat):
    def __init__(self):
        self.name = 'innodb ops'
        self.format = ('f', 3, 1000)
        self.vars = ('inserted', 'updated', 'deleted', 'read')
        self.nick = ('ins', 'upd', 'del', 'rea')
        self.init(self.vars, 1)

    def check(self): 
        if os.access('/usr/bin/mysql', os.X_OK):
            try:
                self.stdin, self.stdout, self.stderr = dpopen('/usr/bin/mysql -n %s' % mysql_options)
            except IOError:
                raise Exception, 'Cannot interface with MySQL binary'
            return True
        raise Exception, 'Needs MySQL binary'

    def extract(self):
        try:
            self.stdin.write('show engine innodb status\G\n')
            line = greppipe(self.stdout, 'OS file reads ')

            if line:
                l = line.split()
                self.cn2['inserted'] = l[4].rstrip(',')
                self.cn2['updated'] = l[6].rstrip(',')
                self.cn2['deleted'] = l[8].rstrip(',')
                self.cn2['read'] = l[10]

            for name in self.vars:
                self.val[name] = (self.cn2[name] - self.cn1[name]) * 1.0 / tick

            if step == op.delay:
                self.cn1.update(self.cn2)

        except IOError, e:
            if op.debug: print 'dstat_innodb_buffer: lost pipe to mysql,', e
            for name in self.vars: self.val[name] = -1

        except Exception, e:
            if op.debug: print 'dstat_innodb_buffer: exception', e
            for name in self.vars: self.val[name] = -1

# vim:ts=4:sw=4:et
