global string, select
import string, select

class dstat_innodb_buffer(dstat):
    def __init__(self):
        self.name = 'innodb pool'
        self.format = ('f', 3, 1000)
        self.vars = ('read', 'created', 'written')
        self.nick = ('crt', 'rea', 'wri')
        self.init(self.vars, 1)

    def check(self): 
        if os.access('/usr/bin/mysql', os.X_OK):
            try:
                self.stdin, self.stdout, self.stderr = dpopen('/usr/bin/mysql -n')
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
                self.cn2['read'] = int(l[2].rstrip(','))
                self.cn2['created'] = int(l[4].rstrip(','))
                self.cn2['written'] = int(l[6])

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
