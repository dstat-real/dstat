global mysql_options
mysql_options = os.getenv('DSTAT_MYSQL')

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'mysql io'
        self.nick = ('recv', 'sent')
        self.vars = ('Bytes_received', 'Bytes_sent')

    def check(self): 
        if not os.access('/usr/bin/mysql', os.X_OK):
            raise Exception('Needs MySQL binary')
        try:
            self.stdin, self.stdout, self.stderr = dpopen('/usr/bin/mysql -n %s' % mysql_options)
        except IOError:
            raise Exception('Cannot interface with MySQL binary')

    def extract(self):
        try:
            self.stdin.write("show status like 'Bytes_%';\n")
            for line in readpipe(self.stdout):
                l = line.split()
                if len(l) < 2: continue
                if l[0] in self.vars:
                    self.set2[l[0]] = float(l[1])

            for name in self.vars:
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

            if step == op.delay:
                self.set1.update(self.set2)

        except IOError as e:
            if op.debug > 1: print('%s: lost pipe to mysql, %s' % (self.filename, e))
            for name in self.vars: self.val[name] = -1

        except Exception as e:
            if op.debug > 1: print('dstat_innodb_buffer: exception', e)
            for name in self.vars: self.val[name] = -1

# vim:ts=4:sw=4:et
