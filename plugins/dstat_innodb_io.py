global mysql_options
mysql_options = os.getenv('DSTAT_MYSQL')

class dstat_innodb_io(dstat):
    def __init__(self):
        self.name = 'innodb io ops '
        self.type = 'f'
        self.width = 3
        self.scale = 1000
        self.vars = ('rea', 'wri', 'syn')
        self.nick = self.vars
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
                self.cn2['read'] = l[0].rstrip(',')
                self.cn2['write'] = l[4].rstrip(',')
                self.cn2['sync'] = l[8]

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
