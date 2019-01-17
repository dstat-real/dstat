### Author: Dag Wieers <dag$wieers,com>

global mysql_options
mysql_options = os.getenv('DSTAT_MYSQL')

class dstat_plugin(dstat):
    def __init__(self):
        self.name = 'innodb pool'
        self.nick = ('crt', 'rea', 'wri')
        self.vars = ('created', 'read', 'written')
        self.type = 'f'
        self.width = 3
        self.scale = 1000

    def check(self): 
        if not os.access('/usr/bin/mysql', os.X_OK):
            raise Exception('Needs MySQL binary')
        try:
            self.stdin, self.stdout, self.stderr = dpopen('/usr/bin/mysql -n %s' % mysql_options)
        except IOError as e:
            raise Exception('Cannot interface with MySQL binary (%s)' % e)

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
                self.val[name] = (self.set2[name] - self.set1[name]) * 1.0 / elapsed

            if step == op.delay:
                self.set1.update(self.set2)

        except IOError as e:
            if op.debug > 1: print('%s: lost pipe to mysql, %s' % (self.filename, e))
            for name in self.vars: self.val[name] = -1

        except Exception as e:
            if op.debug > 1: print('%s: exception: %s' % (self.filename, e))
            for name in self.vars: self.val[name] = -1

# vim:ts=4:sw=4:et
