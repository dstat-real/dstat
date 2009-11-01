### Dstat most expensive process plugin
### Displays the name of the most expensive process
###
### Authority: dag@wieers.com

class dstat_topmem(dstat):
    def __init__(self):
        self.name = 'most expensive'
        self.type = 's'
        self.width = 16
        self.scale = 0
        self.vars = ('memory process',)
        self.pid = str(os.getpid())

    def extract(self):
        self.val['max'] = 0.0
        for pid in os.listdir('/proc/'):
            try:
                ### Is it a pid ?
                int(pid)

                ### Filter out dstat
                if pid == self.pid: continue

                ### Using dopen() will cause too many open files
                l = open('/proc/%s/stat' % pid).read().split()
                if len(l) < 23: continue
                usage = int(l[23]) * pagesize

                ### Is it a new topper ?
                if usage < self.val['max']: continue

                ### Extract name
                name = l[1][1:-1]

            except ValueError:
                continue
            except IOError:
                continue

            self.val['max'] = usage
            self.val['name'] = name
            self.val['pid'] = pid

        if self.val['max'] == 0.0:
            self.val['process'] = ''
        else:
            self.val['process'] = self.val['name']

#               l = l.reverse()
#               for x in l:
#                   print x
#                   if x[0] != '-':
#                       self.val['name'] = os.path.basename(x)
#                       break

        ### Debug (show PID)
#       self.val['process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

    def show(self):
        return '%s%-*s%s' % (ansi['default'], self.width-5, self.val['process'][0:self.width-5], cprint(self.val['max'], 'f', 5, 1024))

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
