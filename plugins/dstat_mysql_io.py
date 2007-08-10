global string, select
import string, select

class dstat_mysql(dstat):
    def __init__(self):
        self.name = 'mysql io'
        self.format = ('f', 5, 1024)
        self.vars = ('Bytes_received', 'Bytes_sent')
        self.nick = ('recv', 'sent')
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
            self.stdin.write("show status like 'Bytes_%';\n")
            for line in readpipe(self.stdout):
                l = line.split()
                if len(l) < 2: continue
                if l[0] in self.vars:
                    self.cn2[l[0]] = float(l[1])

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
