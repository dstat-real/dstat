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

            except ValueError:
                continue
            except IOError:
                continue

            if len(l) < 23: continue
            usage = int(l[23]) * pagesize

            ### Is it a new topper ?
            if usage <= self.val['max']: continue

            self.val['max'] = usage
            self.val['name'] = getnamebypid(pid, l[1][1:-1])
            self.val['pid'] = pid

        self.val['memory process'] = '%-*s%s' % (self.width-5, self.val['name'][0:self.width-5], cprint(self.val['max'], 'f', 5, 1024))

        ### Debug (show PID)
#       self.val['memory process'] = '%*s %-*s' % (5, self.val['pid'], self.width-6, self.val['name'])

    def showcsv(self):
        return '%s / %d%%' % (self.val['name'], self.val['max'])

# vim:ts=4:sw=4:et
