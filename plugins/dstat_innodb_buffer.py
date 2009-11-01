global mysql_options
mysql_options = os.getenv('DSTAT_MYSQL')

class dstat_innodb_buffer(dstat):
    def __init__(self):
        self.name = 'innodb pool'
        self.type = 'f'
        self.width = 3
        self.scale = 1000
        self.vars = ('created', 'read', 'written')
        self.nick = ('crt', 'rea', 'wri')

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
            line = greppipe(self.stdout, 'Pages read ')

            if line:
                l = line.split()
                self.set2['read'] = int(l[2].rstrip(','))
                self.set2['created'] = int(l[4].rstrip(','))
                self.set2['written'] = int(l[6])

            for name in self.vars:
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / tick

            if step == op.delay:
                self.set1.update(self.set2)

        except IOError, e:
            if op.debug: print 'dstat_innodb_buffer: lost pipe to mysql,', e
            for name in self.vars: self.val[name] = -1

        except Exception, e:
            if op.debug: print 'dstat_innodb_buffer: exception', e
            for name in self.vars: self.val[name] = -1

# vim:ts=4:sw=4:et
